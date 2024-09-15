from rest_framework import permissions


class DoctorsOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor or request.user.is_staff


class CurrentDoctorOnly(DoctorsOnly):
    def has_object_permission(self, request, view, obj):
        return request.user.doctor_profile == obj.doctor
