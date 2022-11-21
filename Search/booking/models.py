from django.db import models


class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    succeeded_at = models.DateTimeField()

    user = models.PositiveIntegerField()
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="bookings"
    )
