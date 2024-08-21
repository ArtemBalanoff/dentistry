from django.contrib import admin
from .models import Service, Option


class OptionInLine(admin.TabularInline):
    model = Option
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = (OptionInLine,)
    list_display = ('name', 'specialization', 'duration')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price')
    list_editable = ('price',)
