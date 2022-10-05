from rest_framework import serializers

from images.models import HotelImage, RoomImage


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ("id", "image_key", "hotel")


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ("id", "image_key", "room")
