import datetime as dt
from schedule.models import BaseSchedule, DoctorSchedule, ExceptionCase
from rest_framework import serializers
from services.models import Service
from appointments.models import TimeSlot
from .utils import necessary_timeslots_count_from_services, time_add_timedelta
from dentistry.constants import SLOT_DURATION
from users.models import DoctorProfile


def date_validator(date: dt.date):
    '''Проверка даты на доступность по базовому расписанию клиники и внеплановому.'''
    if not BaseSchedule.objects.get(weekday=date.weekday()).is_open:
        raise serializers.ValidationError(
            'В этот день стоматология не работает.'
        )
    exception_case = ExceptionCase.objects.filter(
        date=date, doctor=None).first()
    if exception_case:
        raise serializers.ValidationError(
            'В этот день стоматология не работает. '
            f'Причина: {exception_case.reason}'
        )
    return date


def services_validator(services: Service):
    '''Проверка услуг на присутствие и принадлежность к одинаковой специальности.'''
    if not services:
        raise serializers.ValidationError(
            'Это поле не может быть пустым.'
        )
    specialization = None
    for service in services:
        if specialization and service.specialization != specialization:
            raise serializers.ValidationError(
                'За один прием можно выбрать услуги только '
                'одного специалиста.'
            )
        specialization = service.specialization
    return services


def timeslots_validator(timeslots: list[TimeSlot]):
    '''Проверка временных слотов на последовательность.'''
    timeslots.sort()
    end_time = None
    for time_slot in timeslots:
        if end_time and time_slot != end_time:
            raise serializers.ValidationError(
                'Временные слоты не последовательны.'
            )
        end_time = time_add_timedelta(time_slot, dt.timedelta(
            minutes=SLOT_DURATION))
    return timeslots


def timeslots_freedom_validator(doctor: DoctorProfile, timeslots: list[TimeSlot], date: dt.date):
    '''Проверка, не заняты ли временные слоты.'''
    occupied_slots = TimeSlot.objects.filter(date=date, doctor=doctor)
    occupied_slots_start_times = occupied_slots.values_list(
        'start_time', flat=True
    )
    if set(occupied_slots_start_times) & set(timeslots):
        raise serializers.ValidationError(
            'Один или несколько слотов уже заняты.'
        )


def timeslots_correct_duration_validator(timeslots: list[TimeSlot], services: list[Service]):
    '''Проверка на соответствие продолжительности услуг и слотов.'''
    nec_timeslots_count = necessary_timeslots_count_from_services(services)
    nec_timeslots_count_in_hours = nec_timeslots_count * SLOT_DURATION / 60
    if nec_timeslots_count > len(timeslots):
        raise serializers.ValidationError(
            'Выбранного времени недостаточно, '
            f'требуется {nec_timeslots_count_in_hours} ч.'
        )
    if nec_timeslots_count < len(timeslots):
        raise serializers.ValidationError(
            'Выбранного времени слишком много, '
            f'требуется {nec_timeslots_count_in_hours} ч.'
        )


def doctor_schedule_freedom_validator(timeslots: list[TimeSlot], doctor: DoctorProfile, date: dt.date):
    '''Проверка временных слотов на доступность по расписанию врача.'''
    slots_start_time = timeslots[0]
    slots_end_time = time_add_timedelta(
        timeslots[-1], dt.timedelta(minutes=SLOT_DURATION))
    doctor_schedule: DoctorSchedule = doctor.schedule.get(weekday=date.weekday())
    if not doctor_schedule.is_working:
        raise serializers.ValidationError(
            'Доктор по расписанию не '
            'работает в этот день.'
        )
    if not (doctor_schedule.start_time <= slots_start_time
            and doctor_schedule.end_time >= slots_end_time):
        raise serializers.ValidationError(
            'Доктор по расписанию не '
            'работает в это время.'
        )


def doctor_exc_schedule_freedom_validator(timeslots: list[TimeSlot], doctor: DoctorProfile, date: dt.date):
    '''Проверка временных слотов на доступность по внеплановому расписанию врача.'''
    slots_start_time = timeslots[0]
    slots_end_time = time_add_timedelta(
        timeslots[-1], dt.timedelta(minutes=SLOT_DURATION))
    exception_case = ExceptionCase.objects.filter(doctor=doctor,
                                                  date=date).first()
    if (exception_case and not (
        exception_case.start_time >= slots_end_time
        or exception_case.end_time <= slots_start_time
    )):
        raise serializers.ValidationError(
            'В это время врач не может вас принять. '
            f'Причина: {exception_case.reason}'
        )


def doctor_spec_correspondence_to_services(doctor: DoctorProfile, services: list[Service]):
    '''Провека услуг на соответствие специальности доктора.'''
    if doctor.specialization != services[0].specialization:
        raise serializers.ValidationError(
            'Выбранные услуги оказывает врач другой специальности.'
        )
