from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins

from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAdmin, IsAuthenticated
from hotels.filters import HotelFilter
from hotels.models import Hotel
from hotels.permissions import IsHotelOwner
from hotels.serializers import HotelSerializer, HotelListSerializer


class HotelsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet
):
    serializer_classes = {
        'list': HotelListSerializer,
        'retrieve': HotelSerializer,
        'create': HotelSerializer,
        'update': HotelSerializer,
        'destroy': HotelSerializer,
        'default': HotelSerializer
    }
    permission_classes = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAdmin,),
        'update': (IsAdmin, IsHotelOwner,),
        'destroy': (IsAdmin, IsHotelOwner,),
        'default': (IsAuthenticated,)
    }
    queryset = Hotel.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HotelFilter
