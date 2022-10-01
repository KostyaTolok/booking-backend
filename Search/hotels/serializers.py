from rest_framework import serializers

from hotels.models import Hotel
from rooms.serializers import RoomSerializer


class HotelSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(use_url=True), required=False, allow_empty=True, write_only=True
    )
    rating = serializers.DecimalField(min_value=0, max_value=5, max_digits=2, decimal_places=1)

    class Meta:
        model = Hotel
        fields = ("id", "name", "images", "description", "address", "rating", "has_parking", "has_wifi", "owner")


class HotelListSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)

    class Meta:
        model = Hotel
        fields = ("id", "name", "images", "rating", "rooms")
