from django.db import models


class Hotel(models.Model):
    name = models.CharField(verbose_name="Hotel name", max_length=50, blank=False)
    description = models.CharField(verbose_name="Hotel description", max_length=300, blank=True, null=True)
    address = models.CharField(verbose_name="Hotel address", max_length=100, blank=False)
    rating = models.DecimalField(verbose_name="Hotel rating", max_digits=2, decimal_places=1)
    has_parking = models.BooleanField(verbose_name="Hotel has parking", default=False)
    has_wifi = models.BooleanField(verbose_name="Hotel has wi-fi", default=False)

    owner = models.PositiveIntegerField(verbose_name="Hotel owner")
    city = models.ForeignKey('cities.City', verbose_name="Hotel city", on_delete=models.CASCADE, related_name="hotels")
