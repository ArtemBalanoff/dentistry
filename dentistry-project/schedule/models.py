from datetime import time
from django.db import models
from users.models import DoctorProfile
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


class BaseSchedule(models.Model):
    weekday = models.PositiveSmallIntegerField(
        'День недели',
        choices=WEEKDAY_CHOICES,
        unique=True
    )
    start_time = models.TimeField(
        'Начало рабочего дня',
        choices=HOUR_CHOICES,
        default=HOUR_CHOICES[0][0]
    )
    end_time = models.TimeField(
        'Конец рабочего дня',
        choices=HOUR_CHOICES,
        default=HOUR_CHOICES[-1][0]
    )
    is_open = models.BooleanField('Открыто', default=True)

    def clean(self):
        from .utils import (check_if_docs_working,
                            compare_base_schedule_to_doctors,
                            start_end_time_validator)
        start_end_time_validator(self)
        compare_base_schedule_to_doctors(self)
        if not self.is_open:
            check_if_docs_working(self)

    class Meta:
        verbose_name = 'расписание дня клиники'
        verbose_name_plural = 'Расписание клиники'
        ordering = ('weekday',)

    def __str__(self):
        return self.get_weekday_display()


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE,
                               related_name='schedule', verbose_name='Доктор')
    weekday = models.PositiveBigIntegerField(
        'День недели', choices=WEEKDAY_CHOICES)
    start_time = models.TimeField('Начало рабочего дня', choices=HOUR_CHOICES,
                                  default=HOUR_CHOICES[0][0])
    end_time = models.TimeField('Конец рабочего дня', choices=HOUR_CHOICES,
                                default=HOUR_CHOICES[-1][0])
    is_working = models.BooleanField('Работает', default=False)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('weekday', 'doctor'),
            name='weekday_doctor_unique'
        )]
        verbose_name = 'расписание дня доктора'
        verbose_name_plural = 'Расписание докторов'
        ordering = ('doctor', 'weekday')

    def __str__(self):
        return str(self.doctor)

    def clean(self):
        from .utils import (start_end_time_validator,
                            compare_doctors_schedule_to_base,
                            check_if_clinic_closed)
        start_end_time_validator(self)
        compare_doctors_schedule_to_base(self)
        if self.is_working:
            check_if_clinic_closed(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ExceptionCase(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile, related_name='exception_cases', verbose_name='Доктор',
        on_delete=models.CASCADE, null=True, blank=True,
        help_text='Оставьте поле пустым, если исключение для всей клиники')
    date = models.DateField('Дата')
    reason = models.TextField('Причина', max_length=REASON_MAX_LENGTH,
                              default='Не указано')

    class Meta:
        verbose_name = 'исключение'
        verbose_name_plural = 'Исключения'
        ordering = ('date',)

    def __str__(self):
        return str(self.date)
