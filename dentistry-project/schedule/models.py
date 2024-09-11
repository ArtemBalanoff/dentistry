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
        null=True,
        blank=True
    )
    end_time = models.TimeField(
        'Конец рабочего дня',
        choices=HOUR_CHOICES,
        null=True,
        blank=True
    )
    is_open = models.BooleanField('Открыто', default=True)

    def clean(self):
        if not self.is_open:
            return None
        doctors_too_early = DoctorSchedule.objects.filter(
            weekday=self.weekday, start_time__lt=self.start_time)
        if doctors_too_early:
            self._message_doctors_too_early = (
                'Расписания докторов '
                f'{", ".join([str(doctor) for doctor in doctors_too_early])} '
                f'в {self.get_weekday_display().lower()} начинались слишком '
                'рано для только что внесенных изменений. Теперь их '
                f'расписания начинаются с {self.start_time.strftime("%H:00")}')
            doctors_too_early.update(start_time=self.start_time)
        doctors_too_late = DoctorSchedule.objects.filter(
            weekday=self.weekday, end_time__gt=self.end_time)
        if doctors_too_late:
            self._message_doctors_too_late = (
                'Расписания докторов '
                f'{", ".join([str(doctor) for doctor in doctors_too_late])} '
                f'в {self.get_weekday_display().lower()} заканчивались '
                'слишком поздно для только что внесенных изменений. Теперь их '
                'расписания заканчиваются в '
                f'{self.start_time.strftime("%H:00")}')
            doctors_too_late.update(start_time=self.end_time)

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
                                  null=True, blank=True)
    end_time = models.TimeField('Конец рабочего дня', choices=HOUR_CHOICES,
                                null=True, blank=True)
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
        from .validators import (
            start_end_time_validator, compare_doctors_schedule_to_base)
        if self.is_working:
            start_end_time_validator(self)
            compare_doctors_schedule_to_base(self)

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

    def __str__(self):
        return str(self.date)
