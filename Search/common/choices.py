from django.db import models


class EquipmentStates(models.IntegerChoices):
    PENDING_VERIFICATION = 0
    VERIFIED = 1
    PENDING_EQUIPMENT = 2
    EQUIPMENT_INSTALLED = 3


class Roles(models.TextChoices):
    ADMIN = "admin"
    USER = "user"
