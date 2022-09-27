from rest_framework import viewsets, mixins, status
from django_filters.rest_framework import DjangoFilterBackend

from hotels.filters import HotelFilter
from hotels.models import Hotel
from hotels.serializers import HotelSerializer, HotelListSerializer


class HotelsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': HotelListSerializer,
        'retrieve': HotelSerializer,
        'create': HotelSerializer,
        'update': HotelSerializer,
        'destroy': HotelSerializer,
    }
    queryset = Hotel.objects.all().distinct()
    default_serializer_class = HotelSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HotelFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
