from django.contrib import admin
from .models import Service, AdditionalService, ServiceOptions


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    pass


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    pass


@admin.register(ServiceOptions)
class ServiceOptionsAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    pass
