from django.db import models

from dentistry.constants import NAME_MAX_LENGTH, DURATION_MAX_LENGTH


class Service(models.Model):
    name = models.CharField('Название услуги', max_length=NAME_MAX_LENGTH)
    description = models.TextField('Описание услуги')
    duration = models.CharField(
        'Продолжительность процедуры', max_length=DURATION_MAX_LENGTH
    )


class AdditionalService(models.Model):
    option_name = models.CharField(
        'Название дополнительной услуги', max_length=NAME_MAX_LENGTH
    )
    price = models.IntegerField('Цена дополнительной услуги')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class ServiceOptions(models.Model):
    option_name = models.CharField(
        'Название варианта услуги', max_length=NAME_MAX_LENGTH
    )
    price = models.IntegerField('Цена конкретного варианта услуги')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
