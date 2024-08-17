from django.db import models
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from services.models import Service

User = get_user_model()


class Entrie(models.Model):
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
    # date = models.DateTimeField()
    time_slots = models.IntegerField(null=True)
    service = models.ManyToManyField(
        Service,
        # through='EntrieService'
    )

    class Meta:
        verbose_name = 'прием'
        verbose_name_plural = 'Приемы'


# class EntrieService(models.Model):
#     entrie = models.ForeignKey(
#         Entrie,
#         verbose_name='Запись',
#         related_name='services',
#         on_delete=models.CASCADE,
#     )
#     service = models.ForeignKey(
#         Service,
#         verbose_name='Услуга',
#         related_name='entries',
#         on_delete=models.CASCADE,
#     )
