from django.db.models import Min
from rest_framework import serializers

from hotels.models import Hotel, HotelImage, HotelView


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
    rating = serializers.DecimalField(min_value=0, max_value=10, max_digits=3, decimal_places=1)
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
            "latitude",
            "longitude",
            "owner",
        )
        extra_kwargs = {"city": {'write_only': True}}
        read_only_fields = ("owner",)

    def create(self, validated_data):
        image_files = validated_data.pop("image_files", [])
        request = self.context.get("request")
        user_id = request.user.get("user_id")
        hotel = Hotel.objects.create(**validated_data, owner=user_id)
        HotelImage.objects.bulk_create((HotelImage(image_key=image_file, hotel=hotel) for image_file in image_files))
        return hotel


class HotelListSerializer(serializers.ModelSerializer):
    min_price = serializers.DecimalField(allow_null=True, read_only=True, max_digits=6, decimal_places=2)
    first_image = serializers.SerializerMethodField(allow_null=True)
    city_name = serializers.CharField(source="city.name")

    class Meta:
        model = Hotel
        fields = ("id", "name", "first_image", "description", "rating", "min_price", "city_name")

    def get_first_image(self, obj):
        image = obj.images.first()
        return image.image_key.url if image else None


class HotelViewSerializer(serializers.ModelSerializer):
    hotel = HotelListSerializer()

    class Meta:
        model = HotelView
        fields = ("id", "hotel")
