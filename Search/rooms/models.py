from django.db import models

from common.choices import EquipmentStates


class Room(models.Model):
    name = models.CharField(verbose_name="Room name", max_length=50, blank=False)
    description = models.CharField(verbose_name="Room description", max_length=200, blank=True, null=True)
    price = models.DecimalField(verbose_name="Room price", max_digits=6, decimal_places=2)
    beds_number = models.PositiveIntegerField(verbose_name="Room beds number")
    equipment_state = models.PositiveIntegerField(
        verbose_name="Room equipment state",
        choices=EquipmentStates.choices,
        default=EquipmentStates.PENDING_VERIFICATION,
    )

    has_washing_machine = models.BooleanField(verbose_name="Room has washing machine", default=False)
    has_kitchen = models.BooleanField(verbose_name="Room has kitchen", default=False)

    hotel = models.ForeignKey(
        'hotels.Hotel', verbose_name="Hotel rooms", on_delete=models.CASCADE, related_name="rooms"
    )
