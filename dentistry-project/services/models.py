from django.db import models
from dentistry.constants import NAME_MAX_LENGTH
from users.models import Specialization

DURATION_CHOICES = (
    (30, '30 минут'),
    (60, '1 час'),
    (120, '2 часа'),
)


class Service(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    description = models.TextField('Описание')
    duration = models.PositiveSmallIntegerField(
        'Продолжительность (в мин.)', choices=DURATION_CHOICES
    )
    specialization = models.ForeignKey(
        Specialization,
        verbose_name='Специализация',
        related_name='services',
        on_delete=models.CASCADE,
    )
    slug = models.SlugField('Слаг')

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'Услуги'
        ordering = ('specialization',)

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(
        'Название', max_length=NAME_MAX_LENGTH
    )
    price = models.IntegerField('Цена')
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                related_name='options')

    class Meta:
        verbose_name = 'опция услуги'
        verbose_name_plural = 'Опции услуги'
        ordering = ('service', 'price')

    def __str__(self):
        return self.name


# class AdditionalService(models.Model):
#     option_name = models.CharField(
#         'Название', max_length=NAME_MAX_LENGTH
#     )
#     price = models.IntegerField('Цена')
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     is_active = models.BooleanField('Действительно', default=True)

#     class Meta:
#         verbose_name = 'доп. услуга'
#         verbose_name_plural = 'Доп услуги'
