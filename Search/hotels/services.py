from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.db import connection

from hotels.models import HotelImage, Hotel
