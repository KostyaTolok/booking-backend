from rest_framework import serializers

from cities.serializer import CitySerializer
from hotels.models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(use_url=True),
                                   required=False,
                                   allow_empty=True,
                                   write_only=True)
    rating = serializers.DecimalField(min_value=0, max_value=5, max_digits=2, decimal_places=1)

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
            "images",
            "description",
            "address",
            "city",
            "rating",
            "has_parking",
            "has_wifi",
            "owner"
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        serializer = CitySerializer(instance.city)
        representation["city"] = serializer.data
        return representation


class HotelListSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Hotel
        fields = ("id", "name", "images", "rating", "min_price")

    def get_min_price(self, obj):
        prices = obj.rooms.all().values_list('price', flat=True)
        min_price = min(prices) if len(prices) != 0 else None
        return min_price
