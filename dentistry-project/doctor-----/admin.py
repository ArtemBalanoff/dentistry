from django.contrib import admin
from .models import Doctor, Specialization
from schedule.admin import DoctorSchedule


class DoctorScheduleInLine(admin.TabularInline):
    model = DoctorSchedule
    extra = 1


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    inlines = (DoctorScheduleInLine,)
    list_display = ('name', 'specialization', 'stage')


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass
