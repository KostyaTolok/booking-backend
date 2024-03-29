from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from common.utils import SearchOpenAPISchemaGenerator

schema_view = get_schema_view(
    openapi.Info(title="Booking Search API", default_version="v1"),
    public=True,
    permission_classes=(AllowAny,),
    generator_class=SearchOpenAPISchemaGenerator,
)

urlpatterns = [
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("hotels/", include("hotels.urls")),
                path("rooms/", include("rooms.urls")),
                path("cities/", include("cities.urls")),
                path("search-requests/", include("search_requests.urls")),
                path("bookings/", include("booking.urls")),
            ]
        ),
    ),
]
