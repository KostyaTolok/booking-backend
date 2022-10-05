from hotels.models import Hotel
from images.models import HotelImage, RoomImage
from rooms.models import Room


def create_images(image_files, instance):
    assert isinstance(instance, Hotel) or isinstance(instance, Room), 'Incorrect instance type to create images'
    if not image_files:
        return
    for image_file in image_files:
        if isinstance(instance, Hotel):
            image = HotelImage.objects.create(image_key=image_file, hotel=instance)
        else:
            image = RoomImage.objects.create(image_key=image_file, room=instance)

        image.save()
