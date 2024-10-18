# import pytest
from django.urls import reverse
from schemas import doctor_list_schema, doctor_schema
from utils import validate_schema


def test_doctor_detail(anon_client, doctors):
    url = reverse('doctor-detail', args=(1,))
    response = anon_client.get(url)
    assert response.status_code == 200
    validate_schema(response.data, doctor_schema)


def test_doctor_list(anon_client, doctors):
    url = reverse('doctor-list')
    response = anon_client.get(url)
    assert response.status_code == 200
    validate_schema(response.data, doctor_list_schema)
