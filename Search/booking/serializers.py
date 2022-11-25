from rest_framework import serializers

from booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(source="room.id", read_only=True)
    room_name = serializers.CharField(source="room.name", read_only=True)
    hotel_id = serializers.IntegerField(source="room.hotel.id", read_only=True)
    hotel_name = serializers.CharField(source="room.hotel.name", read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "start_date",
            "end_date",
            "room_id",
            "room_name",
            "hotel_id",
            "hotel_name",
            "succeeded_at",
        )
