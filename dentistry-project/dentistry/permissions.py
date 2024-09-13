from rest_framework import permissions


class DoctorsOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_doctor


class CurrentDoctorOnly(DoctorsOnly):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.doctor_profile == obj.doctor)
