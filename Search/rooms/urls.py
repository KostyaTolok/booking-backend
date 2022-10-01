from rest_framework import routers

from rooms.views import RoomsViewSet

app_name = 'rooms'

router = routers.SimpleRouter()

router.register(r'', RoomsViewSet, 'rooms')

urlpatterns = router.urls
