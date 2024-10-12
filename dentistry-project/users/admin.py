from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (DoctorUser, PatientUser,
                     DoctorProfile, PatientProfile, Specialization)
from services.models import Service
from .utils import format_phone


class RequiredInlineModelFormset(BaseInlineFormSet):
    '''
    Кастомный Formset с модифицированной валидацией для избежания случаев
    создания админом пользователя без профиля.
    '''
    def clean(self):
        super().clean()
        cleaned_data = getattr(self, 'cleaned_data', None)
        if cleaned_data is not None:
            if not cleaned_data:
                raise ValidationError('Профиль пользователя - обязателен.')


class ServiceInline(admin.StackedInline):
    model = Service
    extra = 0
    verbose_name = 'Услуга'
    verbose_name_plural = 'услуги'


class DoctorProfileInline(admin.StackedInline):
    formset = RequiredInlineModelFormset
    model = DoctorProfile
    extra = 0
    can_delete = False
    verbose_name = 'Профиль Доктора'
    verbose_name_plural = 'профили докторов'


class PatientProfileInline(admin.StackedInline):
    formset = RequiredInlineModelFormset
    model = PatientProfile
    can_delete = False
    verbose_name = 'Профиль Пациента'
    verbose_name_plural = 'профили пациентов'


@admin.register(DoctorUser)
class DoctorAdmin(admin.ModelAdmin):
    inlines = (DoctorProfileInline,)
    list_display = (
        'last_name', 'first_name', 'surname', 'get_doctor_specialization',
        'get_doctor_stage', 'get_phone_number')
    fields = ('phone_number', 'last_name', 'first_name', 'surname',
              'password', 'birth_day')
    list_filter = ('doctor_profile__specialization',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            doctor_profile__isnull=False)

    @admin.display(description='Специальность')
    def get_doctor_specialization(self, obj):
        return obj.doctor_profile.specialization

    @admin.display(description='Стаж')
    def get_doctor_stage(self, obj):
        return f'{obj.doctor_profile.stage} лет (год(а))'

    @admin.display(description='Номер телефона')
    def get_phone_number(self, obj):
        return format_phone(obj.phone_number)


@admin.register(PatientUser)
class PatientAdmin(admin.ModelAdmin):
    inlines = (PatientProfileInline,)
    list_display = ('last_name', 'first_name', 'surname', 'get_age',
                    'get_appointments_count', 'get_phone_number')
    fields = ('phone_number', 'last_name', 'first_name', 'surname',
              'password', 'birth_day')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            patient_profile__isnull=False)

    @admin.display(description='Возраст')
    def get_age(self, obj):
        return obj.age

    @admin.display(description='История приемов')
    def get_appointments_count(self, obj):
        return obj.patient_profile.appointments_count

    @admin.display(description='Номер телефона')
    def get_phone_number(self, obj):
        return format_phone(obj.phone_number)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        if not hasattr(obj, 'patient_profile'):
            PatientProfile.objects.create(user=obj)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    inlines = (ServiceInline,)
    list_display = ('name',)


admin.site.unregister(Group)
