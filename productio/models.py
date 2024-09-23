from autoslug import AutoSlugField

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
        return self.name
