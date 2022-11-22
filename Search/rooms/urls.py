from django.urls import path, include
from rest_framework_nested import routers

from rooms.views import RoomsViewSet, RoomImagesViewSet

router = routers.SimpleRouter()

router.register(r"", RoomsViewSet, "rooms")

images_router = routers.NestedSimpleRouter(router, "", lookup="room")
images_router.register("images", RoomImagesViewSet, basename="images")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(images_router.urls)),
]
