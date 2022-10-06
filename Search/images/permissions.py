from django.shortcuts import get_object_or_404

from common.permissions import JWTBasePermission
from hotels.models import Hotel
from rooms.models import Room


class IsAllowedToCreateHotelImage(JWTBasePermission):
    def has_permission(self, request, view):
        user_id = self.get_user_id(request)
        hotel_id = request.data.get("hotel")
        hotel = get_object_or_404(Hotel, id=hotel_id)
        return user_id == hotel.owner


class IsImageHotelOwner(JWTBasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = self.get_user_id(request)
        return user_id == obj.owner


class IsAllowedToCreateRoomImage(JWTBasePermission):
    def has_permission(self, request, view):
        user_id = self.get_user_id(request)
        room_id = request.data.get("room")
        room = get_object_or_404(Room, id=room_id)
        return user_id == room.hotel.owner


class IsImageRoomOwner(JWTBasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = self.get_user_id(request)
        return user_id == obj.hotel.owner
