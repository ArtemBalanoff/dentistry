from datetime import datetime, time, timedelta
from dentistry.constants import SLOT_DURATION
from schedule.models import DoctorSchedule, ExceptionCase
from .exceptions import BusyDayException, DayHaveNecessaryTimeSlotsCount
from users.models import DoctorProfile
from services.models import Service
import datetime as dt
from django.db.models import QuerySet
from rest_framework.serializers import ValidationError


def timeslots_list(doctor: DoctorProfile, date, doctor_schedule):
    busy_timeslots: QuerySet = doctor.timeslots.filter(date=date)
    busy_timeslots_values = busy_timeslots.values_list('start_time', flat=True)
    timeslots = []
    start_time: dt.time = doctor_schedule.start_time
    end_time: dt.time = doctor_schedule.end_time
    current_time = dt.datetime.now().time()
    while start_time != end_time:
        is_free = False if (
            start_time in busy_timeslots_values
            or start_time < current_time) else True
        timeslots.append(
            {'time': start_time, 'is_free': is_free}
        )
        start_time = time_add_timedelta(
            start_time, timedelta(minutes=SLOT_DURATION))
    return timeslots


def time_add_timedelta(time: time, timedelta: timedelta):
    return (datetime.combine(datetime.today(), time) + timedelta).time()


def necessary_timeslots_count_from_services(services: Service):
    services_durations = [service.duration for service in services]
    return sum(services_durations) // SLOT_DURATION


def check_doctor_working_day(
        date: dt.date,
        doctor: DoctorProfile,
        services: Service):
    week_day: int = date.weekday()
    doctor_schedule: DoctorSchedule = doctor.schedule.filter(
        week_day=week_day).first()
    if not doctor_schedule:
        raise ValidationError('В этот день доктор не работает по расписанию')
    current_date_exception_cases = (
        ExceptionCase.objects.filter(date=date).all())
    if current_date_exception_cases.filter(doctor=None).exists():
        raise ValidationError(
            'В этот день клиника не работает из-за обстоятельств')
    if current_date_exception_cases.filter(doctor=doctor).exists():
        raise ValidationError(
            'В этот день доктор не работает из-за обстоятельств')
    timeslots = timeslots_list(doctor, date, doctor_schedule)
    necessary_timelots_count = necessary_timeslots_count_from_services(
        services)
    try:
        free_time_slots_count = 0
        for timeslot in timeslots:
            if timeslot['is_free']:
                free_time_slots_count += 1
            else:
                free_time_slots_count = 0
            if free_time_slots_count == necessary_timelots_count:
                raise DayHaveNecessaryTimeSlotsCount
    except DayHaveNecessaryTimeSlotsCount:
        pass
    else:
        raise ValidationError(
            'В этот день у доктора нет необходимого кол-ва свободного времени')
