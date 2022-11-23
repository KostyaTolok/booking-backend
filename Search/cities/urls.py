from rest_framework import routers

from cities.views import CitiesViewSet

router = routers.SimpleRouter()

router.register(r"", CitiesViewSet, "cities")

urlpatterns = router.urls
