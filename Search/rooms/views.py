from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from rooms.filters import RoomFilter
from rooms.models import Room
from rooms.serializers import RoomListSerializer, RoomSerializer
from search.permissions import IsAuthenticated, IsAdmin


class RoomsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': RoomListSerializer,
        'retrieve': RoomSerializer,
        'create': RoomSerializer,
        'update': RoomSerializer,
        'destroy': RoomSerializer,
    }
    permission_classes = {
        'list': (IsAuthenticated(),),
        'retrieve': (IsAuthenticated(),),
        'create': (IsAdmin(),),
        'update': (IsAdmin(),),
        'destroy': (IsAdmin(),),
    }
    queryset = Room.objects.all()
    default_serializer_class = RoomSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RoomFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return self.permission_classes.get(self.action, (IsAuthenticated(),))
