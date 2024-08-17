from django.db import models
from dentistry.constants import NAME_MAX_LENGTH
from doctors.models import Specialization

DURATION_CHOICES = (
    (30, 'Half an hour'),
    (60, 'An hour'),
)


class Service(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    description = models.TextField('Описание')
    duration = models.IntegerField(
        'Продолжительность (в мин.)', choices=DURATION_CHOICES
    )
    is_active = models.BooleanField('Действительно', default=True)
    specialization = models.ForeignKey(
        Specialization,
        verbose_name='Специализация',
        related_name='services',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'Услуги'


class AdditionalService(models.Model):
    option_name = models.CharField(
        'Название', max_length=NAME_MAX_LENGTH
    )
    price = models.IntegerField('Цена')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_active = models.BooleanField('Действительно', default=True)

    class Meta:
        verbose_name = 'доп. услуга'
        verbose_name_plural = 'Доп услуги'


class ServiceOptions(models.Model):
    option_name = models.CharField(
        'Название', max_length=NAME_MAX_LENGTH
    )
    price = models.IntegerField('Цена')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_active = models.BooleanField('Действительно', default=True)

    class Meta:
        verbose_name = 'опция услуги'
        verbose_name_plural = 'Опции услуги'
