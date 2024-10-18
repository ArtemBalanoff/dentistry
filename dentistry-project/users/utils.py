import re
from typing import Type

from django.contrib.auth import get_user_model

User: Type = get_user_model()


def get_profile_id_from_user(instance):
    if hasattr(instance, 'doctor_profile'):
        return instance.doctor_profile.id
    if hasattr(instance, 'patient_profile'):
        return instance.patient_profile.id


def format_phone(phone_number):
    formatted_number = re.sub(r'^(8|\+7)(\d{3})(\d{3})(\d{2})(\d{2})$',
                              r'\1 (\2) \3-\4-\5', phone_number)

    return formatted_number
