from rest_framework import mixins, viewsets

from cities.models import City
from cities.serializer import CitySerializer
from common.permissions import IsAdmin


class CitiesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CitySerializer
    permission_classes = (IsAdmin,)
    queryset = City.objects.all()
