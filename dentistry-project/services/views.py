from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Option, Service
from .serializers import OptionSerializer, ServiceSerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('specialization',)
    search_fields = ('name',)


class OptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('service',)
    filterset_fields = ('specialization',)
    search_fields = ('name',)
