from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    """
    Allows access only to users with the Doctor role.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Doctor')
