from rest_framework import mixins, viewsets

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
        'default': CitySerializer,
    }
    permission_classes = {
        'list': (IsAuthenticated,),
        'default': (
            IsAuthenticated,
            IsAdmin,
        ),
    }
    queryset = City.objects.all()
