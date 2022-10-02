from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAuthenticated, IsAdmin
from rooms.filters import RoomFilter
from rooms.models import Room
from rooms.permissions import IsRoomOwner
from rooms.serializers import RoomListSerializer, RoomSerializer


class RoomsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet
):
    serializer_classes = {
        'list': RoomListSerializer,
        'retrieve': RoomSerializer,
        'create': RoomSerializer,
        'update': RoomSerializer,
        'destroy': RoomSerializer,
        'default': RoomSerializer
    }
    permission_classes = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAdmin,),
        'update': (IsAdmin, IsRoomOwner,),
        'destroy': (IsAdmin, IsRoomOwner,),
        'default': (IsAuthenticated,)
    }
    queryset = Room.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RoomFilter

