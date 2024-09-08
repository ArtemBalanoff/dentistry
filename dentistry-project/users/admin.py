from typing import Any
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http import HttpRequest

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
    list_display = ('first_name', 'last_name', 'get_doctor_specialization')
    fields = ('username', 'first_name',
              'last_name', 'password')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(doctor_profile__isnull=False)

    @admin.display(description='Специальность')
    def get_doctor_specialization(self, obj):
        return obj.doctor_profile.specialization


@admin.register(PatientUser)
class PatientAdmin(admin.ModelAdmin):
    inlines = (PatientProfileInline,)
    list_display = ('first_name', 'last_name', 'get_patient_age')
    fields = ('username', 'first_name',
              'last_name', 'password')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(patient_profile__isnull=False)

    @admin.display(description='Возраст')
    def get_patient_age(self, obj):
        return obj.patient_profile.age


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
