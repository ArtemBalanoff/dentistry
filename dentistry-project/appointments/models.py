from django.db import models
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from services.models import Service

User = get_user_model()


class Appointment(models.Model):
    patient = models.ForeignKey(
        User,
        verbose_name='Пациент',
        related_name='entrie',
        on_delete=models.CASCADE
    )
    price = models.IntegerField()
    doctor = models.ForeignKey(
        Doctor,
        verbose_name='Доктор',
        related_name='entrie',
        on_delete=models.CASCADE
    )
    service = models.ManyToManyField(
        Service,
    )

    class Meta:
        verbose_name = 'прием'
        verbose_name_plural = 'Приемы'


class TimeSlot(models.Model):
    start_time = models.DateTimeField('Время начала слота')
    entrie = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, verbose_name='time_slots'
    )
