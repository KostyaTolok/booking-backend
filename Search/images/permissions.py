from django.shortcuts import get_object_or_404

from common.permissions import JWTBasePermission
from hotels.models import Hotel
from rooms.models import Room


class IsImageHotelOwner(JWTBasePermission):
    def has_permission(self, request, view):
        user_id = self.get_user_id(request)
        hotel_id = request.data.get("hotel")
        hotel = get_object_or_404(Hotel, id=hotel_id)
        return user_id == hotel.owner


class IsImageRoomOwner(JWTBasePermission):
    def has_permission(self, request, view):
        user_id = self.get_user_id(request)
        room_id = request.data.get("room")
        room = get_object_or_404(Room, id=room_id)
        return user_id == room.hotel.owner
