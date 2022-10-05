from django.db.models import Min
from rest_framework import serializers

from common.utils import create_images
from hotels.models import Hotel
from images.serializers import HotelImageSerializer


class HotelSerializer(serializers.ModelSerializer):
    image_files = serializers.ListField(
        child=serializers.ImageField(use_url=True), required=False, allow_empty=True, write_only=True
    )
    images = HotelImageSerializer(many=True, read_only=True)
    rating = serializers.DecimalField(min_value=0, max_value=5, max_digits=2, decimal_places=1)
    city_name = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = Hotel

        fields = (
            "id",
            "name",
            "image_files",
            "images",
            "description",
            "address",
            "city",
            "city_name",
            "rating",
            "has_parking",
            "has_wifi",
            "owner",
        )
        extra_kwargs = {"city": {'write_only': True}}

    def create(self, validated_data):
        image_files = validated_data.pop("image_files", None)
        hotel = Hotel.objects.create(**validated_data)
        create_images(image_files, hotel)
        hotel.save()
        return hotel

    def update(self, instance, validated_data):
        image_files = validated_data.pop("image_files", None)
        for image in instance.images.all():
            image.delete()
        create_images(image_files, instance)
        instance.save()
        return super().update(instance, validated_data)


class HotelListSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Hotel
        fields = ("id", "name", "images", "rating", "min_price")

    def get_min_price(self, obj):
        query = obj.rooms.all().values_list('price', flat=True).aggregate(Min('price'))

        return query.get('price__min')
