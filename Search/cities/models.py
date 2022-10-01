from django.db import models


class City(models.Model):
    name = models.CharField(verbose_name="City name", max_length=50, blank=False)
