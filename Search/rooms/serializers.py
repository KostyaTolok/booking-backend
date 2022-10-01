from rest_framework import serializers

from rooms.models import Room


class RoomSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(use_url=True), required=False, allow_empty=True, write_only=True
    )
    price = serializers.DecimalField(min_value=0, max_value=10000, max_digits=6, decimal_places=2)
    beds_number = serializers.IntegerField(min_value=0, max_value=10)

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "images",
            "description",
            "price",
            "beds_number",
            "equipment_state",
            "has_washing_machine",
            "has_kitchen",
            "hotel",
        )


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "images", "price", "hotel")
