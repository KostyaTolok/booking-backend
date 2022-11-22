from django.db.models import Min
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAdmin, IsAuthenticated
from hotels.filters import HotelFilter
from hotels.models import Hotel, HotelImage, HotelView
from hotels.permissions import IsHotelOwner
from hotels.serializers import (
    HotelSerializer,
    HotelListSerializer,
    HotelImageSerializer,
    HotelViewSerializer,
)
from hotels.services import add_hotel_image
from search_requests.models import SearchRequest
from search_requests.serializers import SearchRequestSerializer


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
        "list": HotelListSerializer,
        "retrieve": HotelSerializer,
        "create": HotelSerializer,
        "update": HotelSerializer,
        "destroy": HotelSerializer,
        "default": HotelSerializer,
    }
    permission_classes = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "create": (IsAdmin,),
        "update": (IsAdmin | IsHotelOwner,),
        "destroy": (IsAdmin | IsHotelOwner,),
        "get_recently_viewed": (IsAuthenticated,),
        "default": (IsAuthenticated,),
    }
    queryset = Hotel.objects.annotate(min_price=Min("rooms__price"))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HotelFilter

    def retrieve(self, request, *args, **kwargs):
        if request.user is not None:
            hotel = self.get_object()
            user_id = request.user.get("user_id")
            HotelView.objects.get_or_create(hotel=hotel, viewer=user_id)
        return super().retrieve(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        hotels = super().list(self, request, *args, **kwargs)
        if request.user is not None:
            user_id = request.user.get("user_id")
            if request.GET:
                serializer = SearchRequestSerializer(data=request.GET)
                serializer.is_valid(raise_exception=True)
                SearchRequest(**serializer.data, user=user_id).save()
        return hotels

    @action(detail=False, methods=["get"], url_path="recently-viewed")
    def get_recently_viewed(self, request):
        user_id = request.user.get("user_id")
        views = HotelView.objects.filter(viewer=user_id).order_by("-date")
        serializer = HotelViewSerializer(views, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class HotelImagesViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        "default": HotelImageSerializer,
    }
    permission_classes = {
        "create": (IsAdmin | IsHotelOwner,),
        "destroy": (IsAdmin | IsHotelOwner,),
        "default": (IsAdmin,),
    }

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_pk")
        hotel = get_object_or_404(Hotel, id=hotel_id)
        return HotelImage.objects.filter(hotel=hotel)

    def create(self, request, *args, **kwargs):
        hotel_image = request.FILES.get("image_file")
        hotel_id = kwargs.get("hotel_pk")
        image = add_hotel_image(hotel_id, hotel_image)
        serializer = HotelImageSerializer(image)
        return Response(serializer.data, status.HTTP_201_CREATED)
