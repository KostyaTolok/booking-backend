from rest_framework import routers

from images.views import ImagesViewSet

app_name = 'images'

router = routers.SimpleRouter()

router.register(r'', ImagesViewSet, 'images')

urlpatterns = router.urls
