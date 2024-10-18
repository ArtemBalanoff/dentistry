import datetime as dt

from appointments.models import Appointment, TimeSlot
from rest_framework.serializers import ValidationError
from schedule.models import BaseSchedule, DoctorSchedule, ExceptionCase
from services.models import Service

from dentistry.constants import SLOT_DURATION
from users.models import DoctorProfile
from .utils import (get_necessary_timeslots_count_from_services,
                    time_add_timedelta)


def date_validator(date: dt.date) -> dt.date:
    """
    Проверка даты на доступность по базовому расписанию клиники и внеплановому.
    """
    if not BaseSchedule.objects.get(weekday=date.weekday()).is_open:
        raise ValidationError(
            'В этот день стоматология не работает.'
        )
    exception_case = ExceptionCase.objects.filter(
        date=date, doctor=None).first()
    if exception_case:
        raise ValidationError(
            'В этот день стоматология не работает. '
            f'Причина: {exception_case.reason}'
        )
    return date


def services_validator(services: list[Service]) -> list[Service]:
    """
    Проверка услуг на присутствие и принадлежность к одинаковой специальности.
    """
    if not services:
        raise ValidationError(
            'Это поле не может быть пустым.'
        )
    specialization = None
    for service in services:
        if specialization and service.specialization != specialization:
            raise ValidationError(
                'За один прием можно выбрать услуги только '
                'одного специалиста.'
            )
        specialization = service.specialization
    return services


def timeslots_validator(timeslots: list[dt.time]) -> list[dt.time]:
    """
    Проверка временных слотов на последовательность.
    """
    timeslots.sort()
    end_time = None
    for time_slot in timeslots:
        if end_time and time_slot != end_time:
            raise ValidationError(
                'Временные слоты не последовательны.'
            )
        end_time = time_add_timedelta(time_slot, dt.timedelta(
            minutes=SLOT_DURATION))
    return timeslots


def doctors_validator(doctors: list[DoctorProfile]):
    """
    Проверка на то, что все доктора относятся к одинаковой специальности.
    """
    doctors_specs = [doctor.specialization for doctor in doctors]
    if len(set(doctors_specs)) > 1:
        raise ValidationError(
            'Все выбранные доктора должны относиться к одной специальности'
        )
    return doctors


def timeslots_freedom_validator(
        doctor: DoctorProfile, timeslots: list[TimeSlot],
        date: dt.date, instance: Appointment | None) -> None:
    """
    Проверка, не заняты ли временные слоты.
    """
    occupied_slots = TimeSlot.objects.filter(
        date=date, doctor=doctor).exclude(appointment=instance)
    occupied_slots_start_times = occupied_slots.values_list(
        'start_time', flat=True
    )
    if set(occupied_slots_start_times) & set(timeslots):
        raise ValidationError(
            'Один или несколько слотов уже заняты.'
        )


def timeslots_correct_duration_validator(
        timeslots: list[TimeSlot], services: list[Service]) -> None:
    """
    Проверка на соответствие продолжительности услуг и слотов.
    """
    nec_timeslots_count = get_necessary_timeslots_count_from_services(services)
    nec_timeslots_count_in_hours = nec_timeslots_count * SLOT_DURATION / 60
    if nec_timeslots_count > len(timeslots):
        raise ValidationError(
            'Выбранного времени недостаточно, '
            f'требуется {nec_timeslots_count_in_hours} ч.'
        )
    if nec_timeslots_count < len(timeslots):
        raise ValidationError(
            'Выбранного времени слишком много, '
            f'требуется {nec_timeslots_count_in_hours} ч.'
        )


def doctor_schedule_freedom_validator(
        timeslots: list[TimeSlot], doctor: DoctorProfile,
        date: dt.date) -> None:
    """
    Проверка временных слотов на доступность по расписанию врача.
    """
    slots_start_time = timeslots[0]
    slots_end_time = time_add_timedelta(
        timeslots[-1], dt.timedelta(minutes=SLOT_DURATION))
    doctor_schedule: DoctorSchedule = doctor.schedule.get(
        weekday=date.weekday())
    if not doctor_schedule.is_working:
        raise ValidationError(
            'Доктор по расписанию не '
            'работает в этот день.'
        )
    if not (doctor_schedule.start_time <= slots_start_time
            and doctor_schedule.end_time >= slots_end_time):
        raise ValidationError(
            'Доктор по расписанию не '
            'работает в это время.'
        )


def doctor_exc_schedule_freedom_validator(doctor: DoctorProfile,
                                          date: dt.date) -> None:
    """
    Проверка временных слотов на доступность
    по внеплановому расписанию врача.
    """
    exception_case = ExceptionCase.objects.filter(
        doctor=doctor, date=date).first()
    if exception_case:
        raise ValidationError(
            'В этот день врач не может вас принять. '
            f'Причина: {exception_case.reason}'
        )


def doctor_spec_correspondence_to_services(
        doctor: DoctorProfile, services: list[Service]) -> None:
    """
    Провека услуг на соответствие специальности доктора.
    """
    if doctor.specialization != services[0].specialization:
        raise ValidationError(
            'Выбранные услуги оказывает врач другой специальности.'
        )


def options_relate_to_same_services(instance, new_options) -> None:
    """
    Проверяет, соответствуют ли опции услугам, которые были до изменения.
    """
    options_services = {option.service for option in instance.options.all()}
    new_options_services = {option.service for option in new_options}
    if options_services != new_options_services:
        raise ValidationError(
            'Выбранные опции относятся к иному от прошлого множеству услуг'
        )
