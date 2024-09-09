from django.core.exceptions import ValidationError


def phone_number_validator(phone_number: str):
    if not phone_number.startswith('+7978'):
        raise ValidationError('')
