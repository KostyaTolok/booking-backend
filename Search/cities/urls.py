from rest_framework import routers

from cities.views import CitiesViewSet

app_name = 'cities'

router = routers.SimpleRouter()

router.register(r'', CitiesViewSet, 'cities')

urlpatterns = router.urls
