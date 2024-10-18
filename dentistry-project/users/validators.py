import re

from django.core.exceptions import ValidationError


def phone_number_validator(phone_number: str):
    phone_regex = r'^(\+7|8)\d{10}$'
    phone_number = re.match(phone_regex, phone_number)
    if phone_number:
        return phone_number.group(0)
    raise ValidationError('Введите корректный номер телефона')
