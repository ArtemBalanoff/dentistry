from datetime import date
from schedule.models import BaseSchedule, ExceptionCase
from rest_framework import serializers
from services.models import Service


def date_validator(date: date):
    # Проверка на доступность клиники в базовом расписании
    if BaseSchedule.objects.filter(week_day=date.weekday(),
                                   is_open=False).exists():
        raise serializers.ValidationError(
            'В этот день стоматология не работает'
        )
    # Проверка на доступность клиники во внеплановом расписании
    exception_case = ExceptionCase.objects.filter(
        date=date, doctor=None
    ).first()
    if exception_case:
        raise serializers.ValidationError(
            'В этот день стоматология не работает'
            f'Причина: {exception_case.reason}'
        )
    return date


def services_validator(services: Service):
    if not services:
        raise serializers.ValidationError(
            'Услуга - обязательное поле'
        )
    specialization = None
    for service in services:
        if specialization and service.specialization != specialization:
            raise serializers.ValidationError(
                'За один прием можно выбрать услуги только '
                'одного специалиста'
            )
        specialization = service.specialization
    return services
