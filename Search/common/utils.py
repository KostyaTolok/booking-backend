import os
from uuid import uuid4


def create_images(image_files, instance):
    from hotels.models import Hotel, HotelImage
    from rooms.models import Room, RoomImage

    assert isinstance(instance, Hotel) or isinstance(instance, Room), 'Incorrect instance type to create images'
    if not image_files:
        return
    for image_file in image_files:
        if isinstance(instance, Hotel):
            image = HotelImage.objects.create(image_key=image_file, hotel=instance)
        else:
            image = RoomImage.objects.create(image_key=image_file, room=instance)

        image.save()


def path_and_rename(instance, filename, path):
    _, extension = os.path.splitext(filename)
    filename = f'{uuid4().hex}{extension}'
    return os.path.join(path, filename)
