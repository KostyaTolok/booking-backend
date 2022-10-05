from rest_framework import mixins, viewsets

from common.mixins import SerializerPermissionsMixin
from images.models import HotelImage, RoomImage
from images.permissions import IsImageHotelOwner, IsImageRoomOwner
from images.serializers import HotelImageSerializer, RoomImageSerializer
from common.permissions import IsAdmin


class HotelImagesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {'default': HotelImageSerializer}
    permission_classes = {
        'create': (IsImageHotelOwner,),
        'update': (IsImageHotelOwner,),
        'delete': (IsImageHotelOwner,),
        'default': (IsAdmin,),
    }
    queryset = HotelImage.objects.all()


class RoomImagesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {'default': RoomImageSerializer}
    permission_classes = {
        'create': (IsImageRoomOwner,),
        'update': (IsImageRoomOwner,),
        'delete': (IsImageRoomOwner,),
        'default': (IsAdmin,),
    }
    queryset = RoomImage.objects.all()
