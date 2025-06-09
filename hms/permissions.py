from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Allows access only to admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'

class IsDoctor(permissions.BasePermission):
    """Allows access only to doctor users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Doctor'

class IsStaff(permissions.BasePermission):
    """Allows access only to staff users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Staff'

class IsPatient(permissions.BasePermission):
    """Allows access only to patient users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Patient'

class IsDoctorOrAdmin(permissions.BasePermission):
    """Allows access to doctors and admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Doctor', 'Admin']

class IsPatientOrAdmin(permissions.BasePermission):
    """Allows access to patients and admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Patient', 'Admin']