import datetime

from django.db.models import Min
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection

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
from search_requests.models import SearchRequest
from search_requests.serializers import SearchRequestSerializer


class HotelsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        "list": HotelListSerializer,
        "retrieve": HotelSerializer,
        "default": HotelSerializer,
    }
    permission_classes = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "get_recently_viewed": (IsAuthenticated,),
        "default": (IsAuthenticated,),
    }

    def get_queryset(self):
        sql_query = """
            SELECT DISTINCT
                hotel.id, hotel.name, hotel.description, hotel.rating,
                MIN(room.price) AS min_price, city.name as city_name
            FROM
                hotels_hotel AS hotel
            FULL JOIN
                rooms_room AS room
            ON
                hotel.id = room.hotel_id
            FULL JOIN
                cities_city AS city
            ON
                hotel.city_id = city.id
            FULL JOIN
                booking_booking as booking
            ON
                room.id = booking.room_id"""
        params = dict()
        query_params = self.request.query_params
        for name, value in query_params.items():
            expression = " WHERE" if not params else " AND"

            if name in ["name", "address"] and value != "":
                sql_query += expression + f" LOWER(hotel.name) LIKE %({name})s"
                value = '%' + value.lower() + '%'
                params[name] = value
            elif name in ["owner", "city"] and value.isdigit():
                if name == "owner":
                    sql_query += expression + f" hotel.owner = %({name})s"
                else:
                    sql_query += expression + f" hotel.city_id = %({name})s"
                params[name] = value
            elif name in ["beds_number", "rooms_number"] and value.isdigit():
                sql_query += expression + f" room.{name} >= %({name})s"
                params[name] = value
            elif name in ["has_parking", "has_wifi"] and value.lower() in ["true", "false"]:
                sql_query += expression + f" hotel.{name} IS %({name})s"
                params[name] = True if value.lower() == "true" else False
            elif name in ["has_washing_machine", "has_kitchen"] and value.lower() in ["true", "false"]:
                sql_query += expression + f" room.{name} IS %({name})s"
                params[name] = True if value.lower() == "true" else False
            elif name in ["price_min", "price_max"] and value.replace('.', '', 1).isdigit():
                if name == "price_min":
                    sql_query += expression + f" room.price >= %({name})s"
                else:
                    sql_query += expression + f" room.price <= %({name})s"
                params[name] = value

        sql_query += """
            GROUP BY
                hotel.id, city.name
        """

        if query_params.get("date_after") and query_params.get("date_before"):
            sql_query += """
            HAVING NOT (
                (
                    COUNT(DISTINCT room.id) - COUNT(DISTINCT room.id)
                    FILTER (
                        WHERE (
                            (booking.start_date >= %(date_after)s AND booking.end_date <= %(date_before)s)
                            OR
                            (booking.start_date <= %(date_before)s AND booking.end_date >= %(date_after)s)
                        )
                )
            ) = 0)
            """
            params["date_after"] = query_params.get("date_after")
            params["date_before"] = query_params.get("date_before")

        order = query_params.get("order")
        if order in ["rating", "-rating", "min_price", "-min_price"]:
            is_descending = order[0] == "-"
            order = order[1:] if is_descending else order
            sql_query += f" ORDER BY {order}" + (" DESC" if is_descending else " ASC")

        params = params if params else None

        return Hotel.objects.raw(sql_query, params=params)

    def get_object(self):
        hotels = Hotel.objects.raw(
            """
            SELECT
                hotel.id, hotel.name, hotel.description,
                hotel.address, hotel.rating, hotel.has_parking,
                hotel.has_wifi, hotel.latitude, hotel.longitude,
                hotel.owner, city.name AS city_name
            FROM
                hotels_hotel AS hotel
            JOIN
                cities_city AS city
            ON
                hotel.city_id = city.id
            JOIN
                hotels_hotelimage as image
            ON
                image.hotel_id = hotel.id
            WHERE
                hotel.id = %s
            """,
            [self.kwargs[self.lookup_field]],
        )
        if hotels:
            return hotels[0]
        else:
            raise Http404("Not found")

    def retrieve(self, request, *args, **kwargs):
        if request.user is not None:
            hotel = self.get_object()
            user_id = request.user.get("user_id")
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                INSERT INTO hotels_hotelview(hotel_id, viewer, date)
                VALUES (%s, %s, %s)
                """,
                    [str(hotel.id), user_id, str(datetime.datetime.now())],
                )
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
        views = HotelView.objects.raw(
            """
            SELECT
                id, hotel_id, date
            FROM
                hotels_hotelview AS hotel_view
            WHERE
                hotel_view.viewer = %s
            ORDER BY date DESC
            """,
            [user_id],
        )
        serializer = HotelViewSerializer(views, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class HotelImagesViewSet(
    mixins.ListModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        "default": HotelImageSerializer,
    }
    permission_classes = {
        "list": (AllowAny,),
        "default": (IsAdmin,),
    }

    def get_queryset(self):
        return HotelImage.objects.raw(
            """
            SELECT
                image.id, image.image_key, image.hotel_id
            FROM
                hotels_hotelimage as image
            JOIN
                hotels_hotel as hotel
            ON
                image.hotel_id = hotel.id
            WHERE
                hotel.id = %s
            """,
            [self.kwargs.get("hotel_pk")],
        )
