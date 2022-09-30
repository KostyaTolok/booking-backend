from rest_framework.permissions import BasePermission

from common.utils import decode_token
from common.choices import Roles


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        jwt_token = request.headers.get("Authorization", None)

        if not jwt_token:
            return False
        else:
            decode_token(jwt_token)
            return True


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        jwt_token = request.headers.get("Authorization", None)

        if not jwt_token:
            return False

        payload = decode_token(jwt_token)

        role = payload.get("role", None)

        return role == Roles.ADMIN.value
