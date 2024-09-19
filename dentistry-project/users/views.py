from rest_framework import filters
from dentistry.permissions import DoctorsOnly
from rest_framework import viewsets
from .models import DoctorProfile, PatientProfile, Specialization
from .serializers import (
    DoctorSerializer, PatientSerializer, SpecializationSerializer)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('specialization',)
    search_fields = ('user__first_name', 'user__last_name')


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated & DoctorsOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__first_name', 'user__last_name',
                     'user__phone_number')


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
