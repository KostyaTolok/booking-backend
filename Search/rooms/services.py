from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from rooms.models import RoomImage, Room
