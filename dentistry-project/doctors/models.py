from django.db import models
from dentistry.constants import NAME_MAX_LENGTH


class Doctor(models.Model):
    name = models.CharField('ФИО Врача', max_length=NAME_MAX_LENGTH)
    carier_start = models.DateField('Дата отсчета стажа')
    specialization = models.ForeignKey(
        'Specialization',
        on_delete=models.CASCADE,
        verbose_name='Специализация',
        related_name='doctors'
    )

    class Meta:
        verbose_name = 'врач'
        verbose_name_plural = 'Врачи'


class Specialization(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)

    class Meta:
        verbose_name = 'специализация'
        verbose_name_plural = 'Специализации'
