from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from hotels.models import HotelView, HotelImage


@receiver(post_delete, sender=HotelImage)
def post_delete_image(sender, instance, *args, **kwargs):
    instance.image_key.delete(save=False)


@receiver(post_save, sender=HotelView)
def post_save_hotel_view(sender, instance, *args, **kwargs):
    if HotelView.objects.count() > settings.HOTEL_VIEWS_MAX_AMOUNT:
        HotelView.objects.earliest("date").delete()
