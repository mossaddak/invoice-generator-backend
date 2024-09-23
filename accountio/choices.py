from django.db import models


class CustomerStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    DEACTIVE = "DEACTIVE", "Deactive"
    PENDING = "PENDING", "Pending"
