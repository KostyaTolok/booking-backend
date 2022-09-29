from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins

from hotels.filters import HotelFilter
from hotels.models import Hotel
from hotels.serializers import HotelSerializer, HotelListSerializer
from search.permissions import IsAdmin, IsAuthenticated


class HotelsViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_classes = {
        'list': HotelListSerializer,
        'retrieve': HotelSerializer,
        'create': HotelSerializer,
        'update': HotelSerializer,
        'destroy': HotelSerializer,
    }
    permission_classes = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAdmin,),
        'update': (IsAdmin,),
        'destroy': (IsAdmin,),
    }
    queryset = Hotel.objects.all().distinct()
    default_serializer_class = HotelSerializer
    default_permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HotelFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return (permission() for permission in self.permission_classes.get(self.action, self.default_permission_classes))
