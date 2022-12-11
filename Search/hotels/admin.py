from django.contrib import admin

from hotels.models import Hotel, HotelImage, HotelView

admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(HotelView)
