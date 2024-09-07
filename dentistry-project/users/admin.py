from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (DoctorUser, PatientUser,
                     DoctorProfile, PatientProfile, Specialization)


class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False
    verbose_name_plural = 'Профиль Доктора'


class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False
    verbose_name_plural = 'Профиль Пациента'


@admin.register(DoctorUser)
class DoctorAdmin(admin.ModelAdmin):
    inlines = (DoctorProfileInline,)
    fields = ('username', 'first_name',
              'last_name', 'password')


@admin.register(PatientUser)
class PatientAdmin(admin.ModelAdmin):
    inlines = (PatientProfileInline,)
    fields = ('username', 'first_name',
              'last_name', 'password')


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
