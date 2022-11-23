from rest_framework_mongoengine import routers

from search_requests.views import SearchRequestsViewSet

router = routers.SimpleRouter()
router.register(r"", SearchRequestsViewSet, "search-requests")


urlpatterns = router.urls
