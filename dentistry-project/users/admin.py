from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser, DoctorProfile, PatientProfile, Specialization


class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = True
    extra = 0
    max_num = 1
    verbose_name_plural = 'Профиль Доктора'


class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = True
    extra = 0
    max_num = 1
    verbose_name_plural = 'Профиль Пациента'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (DoctorProfileInline, PatientProfileInline,)
    fields = ('username', 'first_name', 'last_name',
              'password', 'is_doctor')


@admin.register(DoctorProfile)
class DoctorAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    pass


@admin.register(PatientProfile)
class PatientAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    pass


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
