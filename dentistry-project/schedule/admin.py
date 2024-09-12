from django.contrib import admin
from .models import BaseSchedule, DoctorSchedule, ExceptionCase
from django.contrib import messages


@admin.register(BaseSchedule)
class BaseScheduleAdmin(admin.ModelAdmin):
    list_display = ('weekday', 'is_open', 'start_time', 'end_time')
    list_editable = ('start_time', 'end_time', 'is_open')

    def save_model(self, request, obj, form, change):
        if hasattr(obj, '_message_doctors_too_early'):
            messages.warning(request, obj._message_doctors_too_early)
            del obj._message_doctors_too_early
        if hasattr(obj, '_message_doctors_too_late'):
            messages.warning(request, obj._message_doctors_too_late)
            del obj._message_doctors_too_late
        if hasattr(obj, '_message_doc_sch_working'):
            messages.warning(request, obj._message_doc_sch_working)
            del obj._message_doc_sch_working
        obj.save()


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'weekday', 'is_working',
                    'start_time', 'end_time')
    list_editable = ('start_time', 'end_time', 'is_working')
    list_filter = ('doctor', 'weekday')

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
