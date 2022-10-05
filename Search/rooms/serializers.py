from rest_framework import serializers

from common.utils import create_images
from images.models import RoomImage
from images.serializers import RoomImageSerializer
from rooms.models import Room


class RoomSerializer(serializers.ModelSerializer):
    image_files = serializers.ListField(
        child=serializers.ImageField(use_url=True), required=False, allow_empty=True, write_only=True
    )
    images = RoomImageSerializer(many=True, read_only=True)

    price = serializers.DecimalField(min_value=0, max_value=10000, max_digits=6, decimal_places=2)
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
            "equipment_state",
            "has_washing_machine",
            "has_kitchen",
            "hotel",
        )

    def create(self, validated_data):
        image_files = validated_data.pop("image_files", None)
        room = Room.objects.create(**validated_data)
        create_images(image_files, room)
        room.save()
        return room

    def update(self, instance, validated_data):
        image_files = validated_data.pop("image_files", None)
        for image in instance.images.all():
            image.delete()
        create_images(image_files, instance)
        instance.save()
        return super().update(instance, validated_data)


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "images", "price", "hotel")
