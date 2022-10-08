from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAdmin, IsAuthenticated
from hotels.filters import HotelFilter
from hotels.models import Hotel
from hotels.permissions import IsHotelOwner
from hotels.serializers import HotelSerializer, HotelListSerializer
from hotels.services import add_hotel_image, delete_hotel_image


class HotelsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        'list': HotelListSerializer,
        'retrieve': HotelSerializer,
        'create': HotelSerializer,
        'update': HotelSerializer,
        'destroy': HotelSerializer,
        'default': HotelSerializer,
    }
    permission_classes = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAdmin,),
        'update': (IsAdmin | IsHotelOwner,),
        'destroy': (IsAdmin | IsHotelOwner,),
        'add_hotel_image': (IsAdmin | IsHotelOwner,),
        'delete_hotel_image': (IsAdmin | IsHotelOwner,),
        'default': (IsAuthenticated,),
    }
    queryset = Hotel.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HotelFilter

    @action(detail=True, methods=["post"], url_path="images")
    def add_hotel_image(self, request, pk=None):
        hotel_image = request.FILES.get("image")
        hotel = self.get_object()
        add_hotel_image(hotel, hotel_image)
        return Response("Image added to hotel images", status.HTTP_200_OK)

    @action(detail=True, methods=["delete"], url_path="images/(?P<image_id>\d+)")
    def delete_hotel_image(self, request, pk=None, image_id=None):
        delete_hotel_image(image_id)
        return Response(None, status.HTTP_204_NO_CONTENT)
