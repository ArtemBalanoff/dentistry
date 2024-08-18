from datetime import time
from django.db import models
from doctors.models import Doctor
from dentistry.constants import REASON_MAX_LENGTH


WEEKDAY_CHOICES = (
    (0, 'Понедельник'),
    (1, 'Вторник'),
    (2, 'Среда'),
    (3, 'Четверг'),
    (4, 'Пятница'),
    (5, 'Суббота'),
    (6, 'Воскресенье'),
)
HOUR_CHOICES = [(time(hour=hour), f'{hour}:00') for hour in range(24)]


class WeekDaySchedule(models.Model):
    week_day = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES,
                                                unique=True)
    start_time = models.TimeField(choices=HOUR_CHOICES, null=True, blank=True)
    end_time = models.TimeField(choices=HOUR_CHOICES, null=True, blank=True)
    is_open = models.BooleanField(default=True)


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               related_name='doctor_schedule')
    week_day = models.PositiveBigIntegerField(choices=WEEKDAY_CHOICES)
    busy_start_time = models.TimeField(
        choices=HOUR_CHOICES, default=HOUR_CHOICES[0], null=True, blank=True
    )
    busy_end_time = models.TimeField(
        choices=HOUR_CHOICES, default=HOUR_CHOICES[-1], null=True, blank=True
    )
    is_working = models.BooleanField(default=True)

    class Meta:
        constraints = models.UniqueConstraint(
            fields=('week_day', 'doctor'),
            name='week_day_doctor_unique'
        )


class ExceptionalCase(models.Model):
    day = models.DateField()
    time_from = models.TimeField()
    time_until = models.TimeField()
    doctor = models.ForeignKey(Doctor, related_name='exceptional_cases',
                               on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField(max_length=REASON_MAX_LENGTH)
