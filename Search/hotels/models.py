from functools import partial

from django.db import models

from common.utils import path_and_rename


class Hotel(models.Model):
    name = models.CharField(verbose_name="Hotel name", max_length=50, blank=False)
    description = models.TextField(
        verbose_name="Hotel description", max_length=1000, blank=True, null=True
    )
    address = models.CharField(
        verbose_name="Hotel address", max_length=100, blank=False
    )
    rating = models.DecimalField(
        verbose_name="Hotel rating", max_digits=3, decimal_places=1
    )
    has_parking = models.BooleanField(verbose_name="Hotel has parking", default=False)
    has_wifi = models.BooleanField(verbose_name="Hotel has wi-fi", default=False)
    latitude = models.DecimalField(
        verbose_name="Hotel latitude", max_digits=9, decimal_places=6
    )
    longitude = models.DecimalField(
        verbose_name="Hotel longitude", max_digits=9, decimal_places=6
    )

    owner = models.PositiveIntegerField(verbose_name="Hotel owner")
    city = models.ForeignKey(
        "cities.City",
        verbose_name="Hotel city",
        on_delete=models.CASCADE,
        related_name="hotels",
    )


class HotelImage(models.Model):
    image_key = models.ImageField(
        verbose_name="Image key",
        blank=False,
        upload_to=partial(path_and_rename, path="hotels"),
    )
    hotel = models.ForeignKey(
        "hotels.Hotel",
        verbose_name="Hotel",
        on_delete=models.CASCADE,
        related_name="images",
    )


class HotelView(models.Model):
    hotel = models.ForeignKey(
        "hotels.Hotel", on_delete=models.CASCADE, related_name="views"
    )
    viewer = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
