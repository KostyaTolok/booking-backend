from rest_framework import routers

from hotels.views import HotelsViewSet

app_name = 'hotels'

router = routers.SimpleRouter()

router.register(r'', HotelsViewSet, 'hotels')

urlpatterns = router.urls
