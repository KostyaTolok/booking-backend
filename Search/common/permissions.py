from rest_framework.permissions import BasePermission

from common.choices import Roles


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user is not None


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user is not None and request.user.get("role") == Roles.ADMIN.value
        )
