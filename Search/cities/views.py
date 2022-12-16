from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from cities.models import City
from cities.serializer import CitySerializer
from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAdmin, IsAuthenticated


class CitiesViewSet(
    mixins.ListModelMixin,
    SerializerPermissionsMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        "default": CitySerializer,
    }
    permission_classes = {
        "list": (AllowAny,),
        "default": (IsAdmin,),
    }

    def get_queryset(self):
        return City.objects.raw(
            """
            SELECT
                id, name
            FROM
                cities_city
            """
        )
