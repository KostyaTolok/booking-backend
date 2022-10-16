from django.db.models.signals import post_delete
from django.dispatch import receiver

from rooms.models import RoomImage


@receiver(post_delete, sender=RoomImage)
def post_delete_image(sender, instance, *args, **kwargs):
    instance.image_key.delete(save=False)
