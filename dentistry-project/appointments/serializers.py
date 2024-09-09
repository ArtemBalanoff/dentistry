import datetime as dt
from typing import Any, Optional as Opt
from datetime import timedelta
from rest_framework import serializers
from .models import Appointment, AppointmentOption, TimeSlot
from schedule.models import DoctorSchedule
from users.models import DoctorProfile, PatientProfile
from services.models import Option, Service
from .validators import (
    date_validator,
    doctor_exc_schedule_freedom_validator,
    doctor_schedule_freedom_validator,
    doctor_spec_correspondence_to_services,
    services_validator,
    timeslots_correct_duration_validator,
    timeslots_freedom_validator,
    timeslots_validator)
from .utils import check_doctor_working_day, get_timeslots_list


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('date', 'start_time')


class AvailableTimeSlotsSerializer(serializers.Serializer):
    doctor = serializers.SlugRelatedField(
        queryset=DoctorProfile.objects.all(), slug_field='id')
    services = serializers.SlugRelatedField(
        queryset=Service.objects.all(), slug_field='id', many=True)
    date = serializers.DateField()

    def validate_date(self, date):
        return date_validator(date)

    def validate_services(self, services):
        return services_validator(services)

    def validate(self, data):
        check_doctor_working_day(data.get('date'),
                                 data.get('doctor'),
                                 data.get('services'))
        return data

    def to_representation(self, instance: Any):
        data: dict = self.validated_data
        doctor: Opt[DoctorProfile] = data.get('doctor')
        date: Opt[dt.date] = data.get('date')
        doctor_schedule: Opt[DoctorSchedule] = (
            doctor.schedule.get(weekday=date.weekday()))
        timeslots = get_timeslots_list(doctor, date, doctor_schedule)
        return {'timeslots': timeslots}


class AvailableDaysSerializer(serializers.Serializer):
    doctors = serializers.SlugRelatedField(
        queryset=DoctorProfile.objects.all(), slug_field='id', many=True)
    services = serializers.SlugRelatedField(
        queryset=Service.objects.all(), slug_field='id', many=True)
    period = serializers.IntegerField()

    def validate_services(self, services):
        return services_validator(services)

    def validate(self, data):
        doctors = data.get('doctors')
        services = data.get('services')
        if not doctors:
            data['doctors'] = services[0].specialization.doctors.all()
        return data

    def to_representation(self, instance: Any):
        data = self.validated_data
        period: Opt[int] = data.get('period')
        doctors: Opt[list[DoctorProfile]] = data.get('doctors')
        services: Opt[list[Service]] = data.get('services')
        today = dt.date.today()
        dates = [today + timedelta(days=day_idx) for day_idx in range(period)]
        days_dict = [{'date': date, 'is_free': False, 'doctors': []} for date in dates]
        for doctor in doctors:
            for day_idx in range(len(dates)):
                try:
                    check_doctor_working_day(dates[day_idx], doctor, services)
                except serializers.ValidationError:
                    continue
                else:
                    days_dict[day_idx]['is_free'] = True
                    days_dict[day_idx]['doctors'].append(doctor.id)
        return {'days': days_dict}


class AppointmentsSerializer_1(serializers.ModelSerializer):
    timeslots = serializers.ListField(child=serializers.TimeField(),
                                      required=True, write_only=True)
    options = serializers.PrimaryKeyRelatedField(
        queryset=Option.objects.all(), many=True, required=False)

    class Meta:
        model = Appointment
        fields = ('patient', 'doctor', 'date', 'timeslots', 'options')

    def validate_date(self, date: dt.date):
        return date_validator(date)

    def validate_timeslots(self, timeslots: list[TimeSlot]):
        return timeslots_validator(timeslots)


class AppointmentSerializer(serializers.ModelSerializer):
    timeslots = serializers.ListField(child=serializers.TimeField(),
                                      required=True, write_only=True)
    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), many=True,
        write_only=True)
    # options = serializers.PrimaryKeyRelatedField(
    #     queryset=Option.objects.all(), many=True, required=False)

    class Meta:
        model = Appointment
        fields = ('patient', 'doctor', 'services',
                  'date', 'timeslots', 'options')

    def validate_date(self, date: dt.date):
        return date_validator(date)

    def validate_timeslots(self, timeslots: list[TimeSlot]):
        return timeslots_validator(timeslots)

    def validate_services(self, services: list[Service]):
        return services_validator(services)

    # def validate_options(self, options: list[Option]):
    #     if self.context.get('view').action == 'create':
    #         return None
    #     return options

    def validate(self, data: dict[str, Any]):
        timeslots: Opt[list[dt.time]] = data.get('timeslots')
        date: Opt[dt.date] = data.get('date')
        doctor: Opt[DoctorProfile] = data.get('doctor')
        services: Opt[list[Service]] = data.get('services')
        timeslots_freedom_validator(doctor, timeslots, date)
        timeslots_correct_duration_validator(timeslots, services)
        doctor_schedule_freedom_validator(timeslots, doctor, date)
        doctor_exc_schedule_freedom_validator(timeslots, doctor, date)
        doctor_spec_correspondence_to_services(doctor, services)
        return data

    def update(self, instance, validated_data):
        options = instance.appointment_options.values('option')
        return super().update(instance, validated_data)

    def create(self, validated_data: dict):
        validated_data.get('services')
        date: Opt[dt.date] = validated_data.get('date')
        timeslots: Opt[TimeSlot] = validated_data.get('timeslots')
        patient: Opt[PatientProfile] = validated_data.get('patient')
        doctor: Opt[DoctorProfile] = validated_data.get('doctor')
        services: Opt[list[Service]] = validated_data.get('services')
        options = [service.options.first() for service in services]
        appointment: Appointment = Appointment.objects.create(
            patient=patient, doctor=doctor, date=date)
        options_objects = [AppointmentOption(
            appointment=appointment, option=option) for option in options]
        timeslots_objects = [
            TimeSlot(start_time=timeslot,
                     doctor=doctor,
                     date=date,
                     appointment=appointment
                     ) for timeslot in timeslots]
        AppointmentOption.objects.bulk_create(options_objects)
        TimeSlot.objects.bulk_create(timeslots_objects)
        return appointment

    def to_representation(self, instance: Appointment):
        repr_dict: dict = super().to_representation(instance)
        repr_dict['price'] = instance.price
        repr_dict['services'] = [
            service.id for service in self.validated_data.get('services')]
        timeslots: list = []
        for timeslot in instance.timeslots.all():
            timeslots.append(TimeSlotSerializer(timeslot).data)
        repr_dict['timeslots'] = timeslots
        return repr_dict
