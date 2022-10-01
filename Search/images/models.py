from django.db import models


class Image(models.Model):
    image_key = models.CharField(verbose_name="Image key", max_length=200, blank=False)
