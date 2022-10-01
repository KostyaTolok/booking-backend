from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
   openapi.Info(
      title="Booking Search API",
      default_version='v1'
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/hotels/', include('hotels.urls')),
    path('api/rooms/', include('rooms.urls')),
    path('api/images/', include('images.urls')),
    path('api/cities/', include('cities.urls'))
]
