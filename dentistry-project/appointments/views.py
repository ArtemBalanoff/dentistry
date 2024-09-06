from http import HTTPStatus
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Appointment
from .serializers import (
    AppointmentSerializer, AvailableTimeSlotsSerializer,
    AvailableDaysSerializer
)
# from .mixins import ListViewSet
from rest_framework.request import Request


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


# class TimeSlotViewSet(ListViewSet):
#     queryset = TimeSlot.objects.all()
#     serializer_class = TimeSlotSerializer


@api_view(('GET',))
def avaliable_days(request: Request, *args, **kwargs):
    services = request.query_params.get('services')
    services = [int(service_id) for service_id in services.split(',')]
    doctors = request.query_params.get('doctors')
    if doctors:
        doctors = [int(doctors_id) for doctors_id in doctors.split(',')]
    else:
        doctors = []
    period = int(request.query_params.get('period', 7))
    serializer = AvailableDaysSerializer(
        data={'services': services,
              'doctors': doctors,
              'period': period})
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@api_view(('GET',))
def avaliable_timeslots(request: Request, *args, **kwargs):
    date = request.query_params.get('date')
    services = request.query_params.get('services')
    services = [int(service_id) for service_id in services.split(',')]
    doctor = int(request.query_params.get('doctor'))
    serializer = AvailableTimeSlotsSerializer(
        data={'services': services,
              'doctor': doctor,
              'date': date}
    )
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
