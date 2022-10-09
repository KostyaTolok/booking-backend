from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from rooms.models import RoomImage, Room


def add_room_image(room_id, image_file):
    room = get_object_or_404(Room, id=room_id)
    if not image_file:
        raise ValidationError("Image file is not provided")
    image = RoomImage.objects.create(image_key=image_file, room=room)
    return image
