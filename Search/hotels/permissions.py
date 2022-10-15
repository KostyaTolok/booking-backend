from rest_framework.permissions import BasePermission


class IsHotelOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user is not None and request.user.get("user_id") == obj.owner
