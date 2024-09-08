from datetime import time
from django.db import models
from users.models import DoctorProfile
from dentistry.constants import REASON_MAX_LENGTH
from django.core.exceptions import ValidationError


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
                f'Расписания докторов {", ".join([str(doctor) for doctor in doctors_too_early])} '
                f'в {self.get_weekday_display().lower()} начинались слишком рано для только что внесенных изменений. '
                f'Теперь их расписания начинаются с {self.start_time.strftime("%H:00")}')
            doctors_too_early.update(start_time=self.start_time)

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
    is_working = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('weekday', 'doctor'),
            name='weekday_doctor_unique'
        )]
        verbose_name = 'расписание дня доктора'
        verbose_name_plural = 'Расписание доктора'
        ordering = ('doctor', 'weekday')

    def __str__(self):
        return str(self.doctor)

    def clean(self):
        if not self.start_time < self.end_time:
            raise ValidationError(
                'Время начала работы должно быть меньше времени конца работы')
        base_schedule = BaseSchedule.objects.get(
            weekday=self.weekday)
        if self.start_time < base_schedule.start_time:
            self.start_time = base_schedule.start_time
            self._message_too_early = (
                f'В {self.get_weekday_display().lower()} клиника работает '
                f'с {base_schedule.start_time.strftime("%H:00")}. Время '
                f'начала работы врача {self.doctor} изменено на '
                f'{base_schedule.start_time.strftime("%H:00")}.')
        if self.end_time > base_schedule.end_time:
            self.end_time = base_schedule.end_time
            self._message_too_late = (
                f'В {self.get_weekday_display().lower()} клиника работает '
                f'до {base_schedule.end_time.strftime("%H:00")}. Время '
                f'начала работы врача {self.doctor} изменено на '
                f'{base_schedule.end_time.strftime("%H:00")}.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ExceptionCase(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile, related_name='exception_cases', verbose_name='Доктор',
        on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField('Дата')
    reason = models.TextField('Причина', max_length=REASON_MAX_LENGTH,
                              default='Не указано')

    class Meta:
        verbose_name = 'исключение'
        verbose_name_plural = 'Исключения'

    def __str__(self):
        return str(self.date)
