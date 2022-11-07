from django.apps import AppConfig
from django.conf import settings

from booking.consumer import Consumer


class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking'

    def ready(self):
        consumer = Consumer(settings)
        consumer.daemon = True
        consumer.start()
