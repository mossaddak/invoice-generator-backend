from autoslug import AutoSlugField

from phonenumber_field.modelfields import PhoneNumberField

from django.db.models import Q, Value, Sum
from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModelWithUID

from .choices import CustomerStatus
from .managers import CustomCustomerManager
from .utils import get_customer_slug


class Customer(AbstractUser, BaseModelWithUID):
    slug = AutoSlugField(populate_from=get_customer_slug, unique=True, db_index=True)
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True, db_index=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CustomerStatus,
        db_index=True,
        default=CustomerStatus.DRAFT
    )
    objects = CustomCustomerManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"ID: {self.id}, Username: {self.username}"
