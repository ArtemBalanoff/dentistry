from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from dentistry.permissions import DoctorsOnly
from .models import BaseSchedule, DoctorSchedule, ExceptionCase
from .serializers import (BaseScheduleSerializer, DoctorScheduleSerializer,
                          ExceptionCaseSerializer)


class BaseScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BaseSchedule.objects.all()
    serializer_class = BaseScheduleSerializer
    pagination_class = None


class DoctorScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('doctor', 'weekday', 'is_working')


class ExceptionCaseViewSet(viewsets.ModelViewSet):
    queryset = ExceptionCase.objects.all()
    serializer_class = ExceptionCaseSerializer
    permission_classes = (IsAuthenticated & DoctorsOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('doctor', 'weekday')
