from django.contrib import admin
from .models import Service, Option


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    pass


@admin.register(Option)
class ServiceOptionsAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    pass
