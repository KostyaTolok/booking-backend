from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from common.utils import get_user_id


class IsRoomOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        jwt_token = request.headers.get("Authorization", None)

        try:
            user_id = get_user_id(jwt_token)
        except AuthenticationFailed:
            return False

        return user_id == obj.hotel.owner
