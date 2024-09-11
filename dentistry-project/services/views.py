from rest_framework import viewsets
from .models import Option, Service
from .serializers import OptionSerializer, ServiceSerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class OptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
