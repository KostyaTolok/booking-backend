from django.contrib import admin

from images.models import HotelImage, RoomImage

admin.site.register(HotelImage)
admin.site.register(RoomImage)
