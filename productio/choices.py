from django.db import models


class ProductStatusChoices(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    DEACTIVE = "DEACTIVE", "Deactive"
    PENDING = "PENDING", "Pending"
