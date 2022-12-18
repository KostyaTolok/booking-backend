from rest_framework_nested import routers

from booking.views import BookingsViewSet

router = routers.SimpleRouter()

router.register(r"", BookingsViewSet, "bookings")

urlpatterns = router.urls
