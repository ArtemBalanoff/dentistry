from appointments.permissions import DoctorOnly
from rest_framework import viewsets
from .models import DoctorProfile, PatientProfile, Specialization
from .serializers import (
    DoctorSerializer, PatientSerializer, SpecializationSerializer)


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorSerializer


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (DoctorOnly,)


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
