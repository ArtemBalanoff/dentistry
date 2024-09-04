from datetime import date
from dentistry.constants import SLOT_DURATION
from datetime import timedelta
from rest_framework import serializers
from .models import Appointment, TimeSlot
from schedule.models import DoctorSchedule, ExceptionCase
from users.models import DoctorProfile
from services.models import Service
from .exceptions import BusyDayException
from .validators import date_validator, services_validator
from .utils import (
    check_doctor_working_day,
    time_add_timedelta,
    necessary_timeslots_count_from_services)


class TimeSlotSerializer(serializers.Serializer):
    start_time = serializers.TimeField()


class AvaliableTimeSlotsSerializer(serializers.Serializer):
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
        try:
            check_doctor_working_day(data.get('date'),
                                     data.get('doctor'),
                                     data.get('services'))
        except BusyDayException:
            raise serializers.ValidationError('В этот день врач не работает')
        return data

    def to_representation(self, instance):
        data = self.validated_data
        doctor = data.get('doctor')
        date = data.get('date')
        current_doctor_schedule = doctor.schedule.get(
            week_day=date.weekday()
        )
        start_time = current_doctor_schedule.start_time
        end_time = current_doctor_schedule.end_time
        timeslots = []
        busy_timeslots = doctor.timeslots.filter(
            date=date
        ).values('start_time')
        while start_time != end_time:
            is_free = False if start_time in busy_timeslots else True
            timeslots.append(
                {'time': start_time, 'is_free': is_free}
            )
            start_time = time_add_timedelta(
                start_time, timedelta(minutes=SLOT_DURATION))
        return {'timeslots': timeslots}


class AvaliableDaysSerializer(serializers.Serializer):
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

    def to_representation(self, instance):
        data = self.validated_data
        period = data.get('period')
        doctors = data.get('doctors')
        services = data.get('services')
        today = date.today()
        dates = [today + timedelta(days=day_idx) for day_idx in range(period)]
        days = [{'date': date, 'is_free': False} for date in dates]
        for doctor in doctors:
            for day_idx in range(len(dates)):
                try:
                    check_doctor_working_day(dates[day_idx], doctor, services)
                except BusyDayException:
                    continue
                else:
                    days[day_idx]['is_free'] = True
        return {'days': days}


class AppointmentSerializer(serializers.ModelSerializer):
    timeslots = TimeSlotSerializer(many=True, required=True)
    services = serializers.SlugRelatedField(queryset=Service.objects.all(),
                                            slug_field='id', many=True)

    class Meta:
        model = Appointment
        fields = ('patient', 'doctor', 'services',
                  'options', 'date', 'timeslots')

    def validate_date(self, date: date):
        return date_validator(date)

    def validate_timeslots(self, timeslots: list):
        # Проверка на последовательность слотов
        timeslots.sort()
        end_time = None
        for time_slot in timeslots:
            if end_time and time_slot.start_time != end_time:
                raise serializers.ValidationError(
                    'Временные слоты не последовательны'
                )
            end_time = time_slot.start_time + timedelta(minutes=SLOT_DURATION)
        # Проверка на доступность слотов
        occupied_slots = TimeSlot.objects.filter(date='date')
        occupied_slots_start_times = occupied_slots.values_list(
            'start_time', flat=True
        )
        if set(occupied_slots_start_times) & set(timeslots):
            raise serializers.ValidationError(
                'Один или несколько слотов уже заняты'
            )

    def validate(self, data):
        timeslots = data.get('timeslots')
        slots_start_time = timeslots[0]
        slots_end_time = timeslots[-1] + timedelta(minutes=30)
        options = data.get('options')
        doctor = data.get('doctor')
        date = data.get('date')
        # Проверка на продолжительность услуг и слотов
        services = options.values_list('service', flat=True)
        if necessary_timeslots_count_from_services(services) != len(timeslots):
            raise serializers.ValidationError(
                'Выбранного времени недостаточно, '
                'либо слишком много для выбранных услуг'
            )
        # Проверка на доступность доктора по основному расписанию
        if not DoctorSchedule.objects.filter(
            doctor=doctor,
            week_day=date.weekday(),
            is_open=True,
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
        for option in options:
            if specialization != option.specialization:
                raise serializers.ValidationError(
                    'Не все выбранные услуги может оказать этот доктор'
                )
        return super().validate(data)
