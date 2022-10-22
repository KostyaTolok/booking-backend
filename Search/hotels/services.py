from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from hotels.models import HotelImage, Hotel


def add_hotel_image(hotel_id, image_file):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if not image_file:
        raise ValidationError("Image file is not provided")
    image = HotelImage.objects.create(image_key=image_file, hotel=hotel)
    return image
