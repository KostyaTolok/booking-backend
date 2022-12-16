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
        child=serializers.ImageField(use_url=True),
        required=False,
        allow_empty=True,
        write_only=True,
    )
    images = serializers.SerializerMethodField(read_only=True)
    rating = serializers.DecimalField(min_value=0, max_value=10, max_digits=3, decimal_places=1)
    city_name = serializers.CharField(read_only=True)

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
        extra_kwargs = {"city": {"write_only": True}}
        read_only_fields = ("owner",)

    def get_images(self, obj):
        images = HotelImage.objects.raw(
            """
            SELECT
                image.id, image.image_key, image.hotel_id
            FROM
                hotels_hotelimage as image
            WHERE
                image.hotel_id = %s
            ORDER BY
                image.id ASC
            """,
            [obj.id],
        )
        serializer = HotelImageSerializer(images, many=True)
        return serializer.data


class HotelListSerializer(serializers.ModelSerializer):
    min_price = serializers.DecimalField(allow_null=True, read_only=True, max_digits=6, decimal_places=2)
    first_image = serializers.SerializerMethodField(allow_null=True, read_only=True)
    city_name = serializers.CharField(read_only=True)

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
            "first_image",
            "description",
            "rating",
            "min_price",
            "city_name",
        )

    def get_first_image(self, obj):
        images = HotelImage.objects.raw(
            """
            SELECT
                image.id, image.image_key
            FROM
                hotels_hotelimage as image
            WHERE
                image.hotel_id = %s
            ORDER BY
                image.id
            ASC LIMIT 1
            """,
            [obj.id],
        )
        return images[0].image_key.url if images else None


class HotelViewSerializer(serializers.ModelSerializer):
    hotel = HotelListSerializer()

    class Meta:
        model = HotelView
        fields = ("id", "hotel", "date")
