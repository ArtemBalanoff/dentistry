from rest_framework import permissions


class DoctorOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return (request.user and request.user.is_doctor
                or super().has_permission(request, view))
