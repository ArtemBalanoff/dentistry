from django.contrib import admin
from .models import BaseSchedule, DoctorSchedule, ExceptionCase
from django.contrib import messages


@admin.register(BaseSchedule)
class BaseScheduleAdmin(admin.ModelAdmin):
    list_display = ('week_day', 'start_time', 'end_time', 'is_open')
    list_editable = ('start_time', 'end_time', 'is_open')


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'week_day', 'start_time', 'end_time')
    list_editable = ('start_time', 'end_time')
    list_filter = ('doctor', 'week_day')

    def save_model(self, request, obj, form, change):
        if hasattr(obj, '_message_too_early'):
            messages.warning(request, obj._message_too_early)
            del obj._message_too_early
        if hasattr(obj, '_message_too_late'):
            messages.warning(request, obj._message_too_late)
            del obj._message_too_late
        obj.save()


@admin.register(ExceptionCase)
class ExceptionCaseAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'reason')
