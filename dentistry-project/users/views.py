from rest_framework import viewsets
from .models import DoctorProfile, PatientProfile
from .serializers import DoctorSerializer, PatientSerializer


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorSerializer


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
