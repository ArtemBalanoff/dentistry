from django.core.exceptions import ValidationError


def phone_number_validator(phone_number: str):
    if not (phone_number.startswith('+7978') and len(phone_number) == 12):
        raise ValidationError('Введите корректный номер телефона')
