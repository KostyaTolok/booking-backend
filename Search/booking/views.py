from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from booking.models import Booking
from booking.serializers import BookingSerializer
from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAdmin, IsAuthenticated


class BookingsViewSet(SerializerPermissionsMixin, viewsets.GenericViewSet):
    serializer_classes = {
        "default": BookingSerializer,
    }
    permission_classes = {
        "get_my_bookings": (IsAuthenticated,),
        "default": (IsAdmin,),
    }

    @action(detail=False, url_path="me", methods=["GET"])
    def get_my_bookings(self, request):
        user_id = request.user.get("user_id")
        bookings = Booking.objects.raw(
            """
            SELECT
                booking.id, booking.start_date, booking.end_date,
                booking.room_id, room.name as room_name,
                room.hotel_id, hotel.name as hotel_name,
                booking.succeeded_at
            FROM
                booking_booking as booking
            JOIN
                rooms_room AS room
            ON
                booking.room_id = room.id
            JOIN
                hotels_hotel as hotel
            ON
                room.hotel_id = hotel.id
            WHERE
                booking.user = %s
            AND
                booking.start_date >= %s
            """,
            [user_id, datetime.now()],
        )
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
