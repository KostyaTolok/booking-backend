from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender='images.HotelImage')
def post_delete_image(sender, instance, *args, **kwargs):
    instance.image_key.delete(save=False)
