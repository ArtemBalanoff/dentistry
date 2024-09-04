from datetime import date
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

    def __str__(self):
        return self.name

    @property
    def stage(self):
        stage = int((date.today() - self.carier_start).total_seconds()
                    // (60 * 60 * 24 * 30 * 12))
        return f'{stage} лет (год)'


class Specialization(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)

    class Meta:
        verbose_name = 'специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.name
