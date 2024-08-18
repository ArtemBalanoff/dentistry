from datetime import date
from dentistry.constants import SLOT_DURATION
from datetime import timedelta
from functools import reduce
from rest_framework import serializers
from .models import Appointment, TimeSlot
from schedule.models import WeekDaySchedule, DoctorSchedule, ExceptionalCase


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('start_time',)


class AppointmentSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True, required=True)

    class Meta:
        model = Appointment
        fields = ('patient', 'doctor', 'options', 'date', 'time_slots')

    def validate_date(self, date: date):
        # Проверка на доступность в базовом расписании
        if WeekDaySchedule.objects.filter(week_day=date.weekday(),
                                          is_open=False).exists():
            raise serializers.ValidationError(
                'В этот день стоматология не работает'
            )
        # Проверка на доступность в расписании исключений
        exceptional_case = ExceptionalCase.objects.filter(
            date=date, doctor=None
        )
        if exceptional_case:
            raise serializers.ValidationError(
                'В этот день стоматология не работает'
                f'Причина: {exceptional_case.reason}'
            )
        return date

    def validate_timeslots(self, time_slots: list):
        # Проверка на последовательность слотов
        time_slots.sort()
        end_time = None
        for time_slot in time_slots:
            if end_time and time_slot.start_time != end_time:
                raise serializers.ValidationError(
                    'Временные слоты не последовательны'
                )
            end_time = time_slot.start_time + timedelta(minutes=SLOT_DURATION)
        occupied_slots = TimeSlot.objects.filter(date='date')
        occupied_slots_start_times = occupied_slots.values_list(
            'start_time', flat=True
        )
        # Проверка на доступность слотов
        if set(occupied_slots_start_times) & set(time_slots):
            raise serializers.ValidationError(
                'Один или несколько слотов уже заняты'
            )

    def validate(self, data):
        # Проверка на продолжительность услуг и слотов
        services_durations = tuple(
            data.get['options'].values_list('service__duration', flat=True)
        )
        appointment_duration_min = sum(services_durations)
        if appointment_duration_min != len(data.get('time_slots')) * 30:
            raise serializers.ValidationError(
                'Выбранного времени недостаточно'
                'Либо слишком много для выбранных услуг'
            )
        if DoctorSchedule.objects.filter(
            
        )
        return super().validate(data)
