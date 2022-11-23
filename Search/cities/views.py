from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from cities.models import City
from cities.serializer import CitySerializer
from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAdmin, IsAuthenticated


class CitiesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
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
    queryset = City.objects.all()
