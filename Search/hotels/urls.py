from django.urls import path, include
from rest_framework_nested import routers

from hotels.views import HotelsViewSet, HotelImagesViewSet

app_name = 'hotels'

router = routers.SimpleRouter()
router.register(r'', HotelsViewSet, 'hotels')

images_router = routers.NestedSimpleRouter(router, '', lookup='hotel')
images_router.register('images', HotelImagesViewSet, basename='images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(images_router.urls)),
]
