from rest_framework import permissions


class RolePermission(permissions.BasePermission):
    """Base permission class for role-based access control."""
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in self.allowed_roles
        )


class IsAdmin(RolePermission):
    """Allows access only to admin users."""
    allowed_roles = ['Admin']


class IsDoctor(RolePermission):
    """Allows access only to doctor users."""
    allowed_roles = ['Doctor']


class IsStaff(RolePermission):
    """Allows access only to staff users."""
    allowed_roles = ['Staff']


class IsPatient(RolePermission):
    """Allows access only to patient users."""
    allowed_roles = ['Patient']


class IsDoctorOrAdmin(RolePermission):
    """Allows access to doctors and admins."""
    allowed_roles = ['Doctor', 'Admin']


class IsPatientOrAdmin(RolePermission):
    """Allows access to patients and admins."""
    allowed_roles = ['Patient', 'Admin']