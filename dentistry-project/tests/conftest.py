import datetime as dt

import pytest
from constants import (DEFAULT_PASSWORD, EACH_SPEC_DOCTOR_COUNT,
                       PATIENTS_COUNT, TEST_SPECS)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from services.models import Specialization
from utils import generate_phone_number

from users.models import DoctorProfile, PatientProfile

User = get_user_model()
phone_gen = generate_phone_number()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope='session')
def anon_client():
    return APIClient()


@pytest.fixture
def create_patient():
    def _create_patient(client, phone_number, password=DEFAULT_PASSWORD):
        url = reverse('customuser-list')
        data = {
            'phone_number': phone_number,
            'password': password}
        response = client.post(url, data, format='json')
        assert response.status_code == 201, (
            f'Не удалось создать пользователя через Djoser: {response.data}')
        return response.data
    return _create_patient


@pytest.fixture
def create_jwt():
    def _create_jwt(client, phone_number, password=DEFAULT_PASSWORD):
        url = reverse('jwt-create')
        data = {
            'phone_number': phone_number,
            'password': password}
        response = client.post(url, data, format='json')
        assert response.status_code == 200, (
            f'Не удалось получить JWT токен: {response.data}')
        return response.data['access']
    return _create_jwt


@pytest.fixture()
def patients(create_patient, create_jwt):
    patients = []
    for _ in range(PATIENTS_COUNT):
        phone_number = next(phone_gen)
        client = APIClient()
        patient_data = create_patient(client, phone_number)
        patient_profile = PatientProfile.objects.get(pk=patient_data['id'])
        token = create_jwt(client, phone_number)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        patients.append((patient_profile, client))
    return patients


@pytest.fixture(scope='function')
def specializations():
    return Specialization.objects.bulk_create(
        Specialization(name=spec_name) for spec_name in TEST_SPECS)


@pytest.fixture(scope='function')
def doctors(specializations, create_jwt):
    doctors_spec_dict = {}
    for spec in specializations:
        current_spec_doctors = []
        for _ in range(EACH_SPEC_DOCTOR_COUNT):
            phone_number = next(phone_gen)
            client = APIClient()
            doc_user = User.objects.create_user(
                phone_number=phone_number, password=DEFAULT_PASSWORD)
            token = create_jwt(client, phone_number)
            client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
            doc_profile = DoctorProfile.objects.create(
                user=doc_user, specialization=spec,
                carier_start=dt.date.today())
            current_spec_doctors.append((doc_profile, client))
        doctors_spec_dict[str(spec)] = current_spec_doctors
    return doctors_spec_dict
