from rest_framework import viewsets
from .models import Option, Service
from .serializers import OptionSerializer, ServiceSerializer
from rest_framework.pagination import PageNumberPagination


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = PageNumberPagination


class OptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    pagination_class = PageNumberPagination
