from rest_framework import serializers

from rooms.models import Room, RoomImage


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ("id", "image_key", "room")
        read_only_fields = ("id", "image_key", "room")


class RoomSerializer(serializers.ModelSerializer):
    image_files = serializers.ListField(
        child=serializers.ImageField(use_url=True),
        required=False,
        allow_empty=True,
        write_only=True,
    )
    images = serializers.SerializerMethodField(read_only=True)

    price = serializers.DecimalField(min_value=0, max_value=1000, max_digits=6, decimal_places=2)
    beds_number = serializers.IntegerField(min_value=0, max_value=10)

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "images",
            "image_files",
            "description",
            "price",
            "beds_number",
            "rooms_number",
            "equipment_state",
            "has_washing_machine",
            "has_kitchen",
            "hotel",
        )

    def create(self, validated_data):
        image_files = validated_data.pop("image_files", [])
        room = Room.objects.create(**validated_data)
        RoomImage.objects.bulk_create((RoomImage(image_key=image_file, room=room) for image_file in image_files))
        return room

    def get_images(self, obj):
        images = RoomImage.objects.raw(
            """
            SELECT
                image.id, image.image_key, image.room_id
            FROM
                rooms_roomimage as image
            WHERE
                image.room_id = %s
            ORDER BY
                image.id ASC
            """,
            [obj.id],
        )
        serializer = RoomImageSerializer(images, many=True)
        return serializer.data


class RoomListSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Room
        fields = ("id", "name", "first_image", "description", "price", "hotel")

    def get_first_image(self, obj):
        images = RoomImage.objects.raw(
            """
            SELECT
                image.id, image.image_key
            FROM
                rooms_roomimage as image
            WHERE
                image.room_id = %s
            ORDER BY
                image.id
            ASC LIMIT 1
            """,
            [obj.id],
        )
        return images[0].image_key.url if images else None
