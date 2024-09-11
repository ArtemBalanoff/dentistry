import datetime as dt
from http import HTTPStatus
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from .models import Appointment
from .serializers import (
    AppointmentCloseSerializer, AppointmentSerializer,
    AvailableTimeSlotsSerializer, AvailableDaysSerializer
)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @action(('PATCH',), detail=True)
    def close(self, request: Request, pk: int):
        instance = get_object_or_404(Appointment, pk=pk)
        serializer = AppointmentCloseSerializer(instance=instance,
                                                data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


# class TimeSlotViewSet(ListViewSet):
#     queryset = TimeSlot.objects.all()
#     serializer_class = TimeSlotSerializer


@api_view(('GET',))
def avaliable_days(request: Request, *args, **kwargs):
    services = request.query_params.get('services', [])
    doctors = request.query_params.get('doctors', [])
    period = request.query_params.get('period', 7)
    services = services and services.split(',')
    doctors = doctors and doctors.split(',')
    serializer = AvailableDaysSerializer(
        data={'services': services,
              'doctors': doctors,
              'period': period})
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@api_view(('GET',))
def avaliable_timeslots(request: Request, *args, **kwargs):
    services = request.query_params.get('services', [])
    services = services and services.split(',')
    doctor = request.query_params.get('doctor')
    date = request.query_params.get('date', dt.date.today())
    serializer = AvailableTimeSlotsSerializer(
        data={'services': services,
              'doctor': doctor,
              'date': date}
    )
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
