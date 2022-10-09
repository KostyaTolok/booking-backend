from django.db.models import Min
from rest_framework import serializers

from hotels.models import Hotel, HotelImage


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ("id", "image_key", "hotel")
        read_only_fields = ("id", "image_key", "hotel")


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
        if image_files:
            for image_file in image_files:
                HotelImage.objects.create(image_key=image_file, hotel=hotel)
        return hotel


class HotelListSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField(allow_null=True)
    first_image = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Hotel
        fields = ("id", "name", "first_image", "rating", "min_price")

    def get_min_price(self, obj):
        query = obj.rooms.all().values_list('price', flat=True).aggregate(Min('price'))

        return query.get('price__min')

    def get_first_image(self, obj):
        image = obj.images.first()
        return image.image_key.url if image else None
