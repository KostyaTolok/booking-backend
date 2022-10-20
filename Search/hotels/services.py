from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from hotels.models import HotelImage, Hotel
from search_requests.utils import search_request_params


def add_hotel_image(hotel_id, image_file):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if not image_file:
        raise ValidationError("Image file is not provided")
    image = HotelImage.objects.create(image_key=image_file, hotel=hotel)
    return image


def extract_request_params(request):
    params = {}

    for key, value in request.GET.items():
        if key in search_request_params and value != "":
            params[key] = value

    return params
