from common.permissions import JWTBasePermission


class IsRoomOwner(JWTBasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = self.get_user_id(request)
        return user_id == obj.hotel.owner
