from functools import partial

from django.db import models

from images.utils import path_and_rename


class HotelImage(models.Model):
    image_key = models.ImageField(
        verbose_name="Image key", blank=False, upload_to=partial(path_and_rename, path="hotels")
    )
    hotel = models.ForeignKey('hotels.Hotel', verbose_name="Hotel", on_delete=models.CASCADE, related_name="images")


class RoomImage(models.Model):
    image_key = models.ImageField(
        verbose_name="Image key", blank=False, upload_to=partial(path_and_rename, path="rooms")
    )
    room = models.ForeignKey('rooms.Room', verbose_name="Room image", on_delete=models.CASCADE, related_name="images")
