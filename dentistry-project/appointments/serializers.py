import datetime as dt
from typing import Any, Optional as Opt
from dentistry.constants import SLOT_DURATION
from datetime import timedelta
from rest_framework import serializers
from .models import Appointment, AppointmentOption, TimeSlot
from schedule.models import DoctorSchedule, ExceptionCase
from users.models import DoctorProfile, PatientProfile
from services.models import Option, Service
from .exceptions import BusyDayException
from .validators import date_validator, services_validator
from .utils import (
    check_doctor_working_day,
    time_add_timedelta,
    necessary_timeslots_count_from_services)
from django.db.models import QuerySet


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
        current_doctor_schedule: Opt[DoctorSchedule] = (
            doctor.schedule.get(week_day=date.weekday()))
        start_time: dt.time = current_doctor_schedule.start_time
        end_time: dt.time = current_doctor_schedule.end_time
        current_time = dt.datetime.now().time()
        timeslots = []
        busy_timeslots: QuerySet = doctor.timeslots.filter(date=date)
        busy_timeslots_values = busy_timeslots.values_list('start_time', flat=True)
        while start_time != end_time:
            is_free = False if (
                start_time in busy_timeslots_values
                or start_time < current_time) else True
            timeslots.append(
                {'time': start_time, 'is_free': is_free}
            )
            start_time = time_add_timedelta(
                start_time, timedelta(minutes=SLOT_DURATION))
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
        # Если не указан конкретный доктор,
        # рассматриваем всех нужной специальности
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
        days = [{'date': date, 'is_free': False, 'doctors': []} for date in dates]
        for doctor in doctors:
            for day_idx in range(len(dates)):
                try:
                    check_doctor_working_day(dates[day_idx], doctor, services)
                except serializers.ValidationError:
                    continue
                else:
                    days[day_idx]['is_free'] = True
                    days[day_idx]['doctors'].append(doctor.id)
        return {'days': days}


class AppointmentSerializer(serializers.ModelSerializer):
    timeslots = serializers.ListField(child=serializers.TimeField(),
                                      required=True, write_only=True)
    services = serializers.SlugRelatedField(
        queryset=Service.objects.all(),
        slug_field='id', many=True,
        write_only=True)
    options = serializers.PrimaryKeyRelatedField(
        # queryset=Option.objects.all(),
        many=True, read_only=True)
    # date = serializers.DateField(write_only=True)

    class Meta:
        model = Appointment
        fields = ('patient', 'doctor', 'services',
                  'date', 'timeslots', 'options')

    def validate_date(self, date: dt.date):
        return date_validator(date)

    def validate(self, data: dict[str, Any]):
        timeslots: Opt[list[dt.time]] = data.get('timeslots')
        date: Opt[dt.date] = data.get('date')
        doctor: Opt[DoctorProfile] = data.get('doctor')
        services: Opt[list[Service]] = data.get('services')
        # options = [service.options.first() for service in services]
        # Проверка на последовательность слотов
        timeslots.sort()
        end_time = None
        for time_slot in timeslots:
            if end_time and time_slot != end_time:
                raise serializers.ValidationError(
                    'Временные слоты не последовательны'
                )
            end_time = time_add_timedelta(time_slot, timedelta(
                minutes=SLOT_DURATION))
        # Проверка на доступность слотов
        occupied_slots = TimeSlot.objects.filter(date=date, doctor=doctor)
        occupied_slots_start_times = occupied_slots.values_list(
            'start_time', flat=True
        )
        if set(occupied_slots_start_times) & set(timeslots):
            raise serializers.ValidationError(
                'Один или несколько слотов уже заняты'
            )
        slots_start_time = timeslots[0]
        slots_end_time = time_add_timedelta(
            timeslots[-1], timedelta(minutes=SLOT_DURATION))
        # Проверка на продолжительность услуг и слотов
        # services = [option.service for option in options]
        if necessary_timeslots_count_from_services(services) != len(timeslots):
            raise serializers.ValidationError(
                'Выбранного времени недостаточно, '
                'либо слишком много для выбранных услуг'
            )
        # Проверка на доступность доктора по основному расписанию
        if not DoctorSchedule.objects.filter(
            doctor=doctor,
            week_day=date.weekday(),
            start_time__lte=slots_start_time,
            end_time__gte=slots_end_time,
        ):
            raise serializers.ValidationError(
                'Доктор по расписанию не '
                'работает в это время'
            )
        # Проверка на доступность доктора по внеплановому расписанию
        exception_case = ExceptionCase.objects.filter(doctor=doctor,
                                                      date=date).first()
        if (exception_case and not (
            exception_case.start_time >= slots_end_time
            or exception_case.end_time <= slots_start_time
        )):
            raise serializers.ValidationError(
                'В это время врач не может вас принять'
                f'Причина: {exception_case.reason}'
            )
        # Проверка на специализацию доктора и выбранных услуг
        specialization = doctor.specialization
        for service in services:
            if specialization != service.specialization:
                raise serializers.ValidationError(
                    'Не все выбранные услуги может оказать этот доктор'
                )
        return super().validate(data)

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
        app_options = [AppointmentOption(
            appointment=appointment, option=option) for option in options]
        AppointmentOption.objects.bulk_create(app_options)
        timeslots_obj = [
            TimeSlot(start_time=timeslot,
                     doctor=doctor,
                     date=date,
                     appointment=appointment
                     ) for timeslot in timeslots]
        TimeSlot.objects.bulk_create(timeslots_obj)
        return appointment
        # return super().create(validated_data)

    def to_representation(self, instance: Appointment):
        resp_dict: dict = super().to_representation(instance)
        resp_dict['price'] = instance.price
        timeslots: list = []
        for timeslot in instance.timeslots.all():
            timeslots.append(TimeSlotSerializer(timeslot).data)
        resp_dict['timeslots'] = timeslots
        return resp_dict
