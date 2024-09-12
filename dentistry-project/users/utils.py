from typing import Type
from django.contrib.auth import get_user_model

User: Type = get_user_model()


def get_profile_id_from_user(instance):
    if hasattr(instance, 'doctor_profile'):
        return instance.doctor_profile.id
    if hasattr(instance, 'patient_profile'):
        return instance.patient_profile.id


def format_phone(phone_number):
    return (
        f'{phone_number[:2]} ({phone_number[2:5]}) {phone_number[5:8]}-'
        f'{phone_number[8:10]}-{phone_number[10:12]}')
