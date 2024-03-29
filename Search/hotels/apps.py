from django.apps import AppConfig
from django.db.models.signals import post_delete


class HotelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hotels"

    def ready(self):
        from hotels import signals
        from hotels.models import HotelImage

        post_delete.connect(signals.post_delete_image, sender=HotelImage)
