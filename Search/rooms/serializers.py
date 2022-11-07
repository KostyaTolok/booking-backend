from rest_framework import serializers

from rooms.models import Room, RoomImage


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ("id", "image_key", "room")
        read_only_fields = ("id", "image_key", "room")


class RoomSerializer(serializers.ModelSerializer):
    image_files = serializers.ListField(
        child=serializers.ImageField(use_url=True), required=False, allow_empty=True, write_only=True
    )
    images = RoomImageSerializer(many=True, read_only=True)

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


class RoomListSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Room
        fields = ("id", "name", "first_image", "description", "price", "hotel")

    def get_first_image(self, obj):
        image = obj.images.first()
        return image.image_key.url if image else None
