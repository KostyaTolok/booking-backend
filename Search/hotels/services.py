from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from hotels.models import HotelImage


def add_hotel_image(hotel, image_file):
    if not image_file:
        raise ValidationError("Image file is not provided")
    HotelImage.objects.create(image_key=image_file, hotel=hotel)
    hotel.save()


def delete_hotel_image(image_id):
    if not image_id:
        raise ValidationError("Image id is not provided")
    image = get_object_or_404(HotelImage, id=image_id)
    image.delete()
