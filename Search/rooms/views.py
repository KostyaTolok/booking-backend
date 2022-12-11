from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAuthenticated, IsAdmin
from rooms.filters import RoomFilter
from rooms.models import Room, RoomImage
from rooms.permissions import IsRoomOwner
from rooms.serializers import RoomListSerializer, RoomSerializer, RoomImageSerializer


class RoomsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        "list": RoomListSerializer,
        "retrieve": RoomSerializer,
        "default": RoomSerializer,
    }
    permission_classes = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "default": (IsAuthenticated,),
    }

    def get_queryset(self):
        return Room.objects.raw(
            """
            SELECT
                id, name, description,
                price, hotel_id
            FROM
                rooms_room AS room
            """
        )

    def get_object(self):
        rooms = Room.objects.raw(
            """
            SELECT
                id, name, description,
                price, beds_number, rooms_number,
                equipment_state, has_washing_machine,
                has_kitchen, hotel_id
            FROM
                rooms_room
            WHERE
                id = %s
            """,
            [self.kwargs[self.lookup_field]],
        )
        if rooms:
            return rooms[0]
        else:
            raise Http404("Not found")


class RoomImagesViewSet(
    mixins.ListModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        "default": RoomImageSerializer,
    }
    permission_classes = {
        "list": (AllowAny,),
        "default": (IsAdmin,),
    }

    def get_queryset(self):
        return RoomImage.objects.raw(
            """
            SELECT
                image.id, image.image_key, image.room_id
            FROM
                rooms_roomimage as image
            JOIN
                rooms_room as room
            ON
                image.room_id = room.id
            WHERE
                room.id = %s
            """,
            [self.kwargs.get("room_pk")],
        )
