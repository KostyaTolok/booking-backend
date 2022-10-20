from django.db import models


class Roles(models.TextChoices):
    ADMIN = "admin"
    USER = "user"
