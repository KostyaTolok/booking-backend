from rest_framework.permissions import BasePermission

from common.utils import decode_token


class IsHotelOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        jwt_token = request.headers.get("Authorization", None)

        if not jwt_token:
            return False

        payload = decode_token(jwt_token)
        user_id = payload.get("sub", None)

        if not user_id.isdigit():
            return False

        user_id = int(user_id)

        return user_id == obj.owner
