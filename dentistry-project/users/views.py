from dentistry.permissions import DoctorsOnly
from rest_framework import viewsets
from .models import DoctorProfile, PatientProfile, Specialization
from .serializers import (
    DoctorSerializer, PatientSerializer, SpecializationSerializer)
from rest_framework.permissions import IsAuthenticated


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorSerializer


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated & DoctorsOnly,)


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
