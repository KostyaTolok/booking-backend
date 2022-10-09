from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAuthenticated, IsAdmin
from rooms.filters import RoomFilter
from rooms.models import Room, RoomImage
from rooms.permissions import IsRoomOwner
from rooms.serializers import RoomListSerializer, RoomSerializer, RoomImageSerializer
from rooms.services import add_room_image


class RoomsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        'list': RoomListSerializer,
        'retrieve': RoomSerializer,
        'create': RoomSerializer,
        'update': RoomSerializer,
        'destroy': RoomSerializer,
        'default': RoomSerializer,
    }
    permission_classes = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAdmin,),
        'update': (IsAdmin | IsRoomOwner,),
        'destroy': (IsAdmin | IsRoomOwner,),
        'add_room_image': (IsAdmin | IsRoomOwner,),
        'delete_room_image': (IsAdmin | IsRoomOwner,),
        'default': (IsAuthenticated,),
    }
    queryset = Room.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RoomFilter


class RoomImagesViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, SerializerPermissionsMixin, viewsets.GenericViewSet
):
    serializer_classes = {
        "default": RoomImageSerializer,
    }
    permission_classes = {
        "create": (IsAdmin | IsRoomOwner,),
        "destroy": (IsAdmin | IsRoomOwner,),
        'default': (IsAdmin,),
    }

    def get_queryset(self):
        room_id = self.kwargs.get("room_pk")
        room = get_object_or_404(Room, id=room_id)
        return RoomImage.objects.filter(room=room)

    def create(self, request, *args, **kwargs):
        room_image = request.FILES.get("image_file")
        room_id = kwargs.get("room_pk")
        image = add_room_image(room_id, room_image)
        serializer = RoomImageSerializer(image)
        return Response(serializer.data, status.HTTP_201_CREATED)
