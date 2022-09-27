from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hotels/', include('hotels.urls')),
    path('api/rooms/', include('rooms.urls'))
]
