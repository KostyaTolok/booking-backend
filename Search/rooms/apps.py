from django.apps import AppConfig
from django.db.models.signals import post_delete


class RoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rooms'

    def ready(self):
        from rooms import signals
        from rooms.models import RoomImage

        post_delete.connect(signals.post_delete_image, sender=RoomImage)
