from autoslug import AutoSlugField

from decimal import Decimal

from versatileimagefield.fields import VersatileImageField

from django.db import models

from common.models import BaseModelWithUID

from .choices import ProductStatusChoices

from .utils import get_product_slug, get_product_media_path_prefix


class Product(BaseModelWithUID):
    slug = AutoSlugField(populate_from=get_product_slug, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=ProductStatusChoices, default=ProductStatusChoices.DRAFT
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.FloatField(help_text="here will be perchantage of discount")
    image = VersatileImageField(
        "Image",
        upload_to=get_product_media_path_prefix,
        blank=True,
    )

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}"

    def get_discount(self):
        """Returns the discount amount in currency, not percentage."""
        discount = Decimal(self.discount)
        return self.price * (discount / 100) if discount else 0

    def get_discounted_price(self):
        """Returns the price after applying the discount."""
        return self.price - self.get_discount() if self.discount else self.price