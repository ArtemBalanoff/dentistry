from dentistry.permissions import DoctorsOnly
from .models import BaseSchedule, DoctorSchedule, ExceptionCase
from rest_framework import viewsets
from .serializers import (BaseScheduleSerializer, DoctorScheduleSerializer,
                          ExceptionCaseSerializer)
from rest_framework.permissions import IsAuthenticated


class BaseScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BaseSchedule.objects.all()
    serializer_class = BaseScheduleSerializer


class DoctorScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer


class ExceptionCaseViewSet(viewsets.ModelViewSet):
    queryset = ExceptionCase.objects.all()
    serializer_class = ExceptionCaseSerializer
    permission_classes = (IsAuthenticated & DoctorsOnly,)
