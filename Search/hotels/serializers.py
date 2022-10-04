from django.db.models import Min
from rest_framework import serializers

from cities.serializer import CitySerializer
from hotels.models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(use_url=True), required=False, allow_empty=True, write_only=True
    )
    rating = serializers.DecimalField(min_value=0, max_value=5, max_digits=2, decimal_places=1)
    city = serializers.CharField(source="city.name", read_only=True)

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
        extra_kwargs = {"city": {'write_only': True}}


class HotelListSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Hotel
        fields = ("id", "name", "images", "rating", "min_price")

    def get_min_price(self, obj):
        query = obj.rooms.all().values_list('price', flat=True).aggregate(Min('price'))

        return query.get('price__min')
