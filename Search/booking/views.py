from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from booking.models import Booking
from booking.serializers import BookingSerializer
from common.mixins import SerializerPermissionsMixin
from common.permissions import IsAdmin, IsAuthenticated


class BookingsViewSet(SerializerPermissionsMixin, viewsets.GenericViewSet):
    serializer_classes = {
        "default": BookingSerializer,
    }
    permission_classes = {
        "get_my_bookings": (IsAuthenticated,),
        "default": (IsAdmin,),
    }
    queryset = Booking.objects.all()

    @action(detail=False, url_path="me", methods=["GET"])
    def get_my_bookings(self, request):
        user_id = request.user.get("user_id")
        bookings = Booking.objects.filter(user=user_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
