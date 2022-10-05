from rest_framework import routers

from images.views import HotelImagesViewSet, RoomImagesViewSet

app_name = 'images'

router = routers.SimpleRouter()

router.register(r'hotel-images', HotelImagesViewSet, 'hotel-images')
router.register(r'room-images', RoomImagesViewSet, 'room-images')

urlpatterns = router.urls
