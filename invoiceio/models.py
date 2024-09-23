from autoslug import AutoSlugField

from django.utils import timezone

from versatileimagefield.fields import VersatileImageField

from django.db import models

from accountio.models import Customer

from common.models import BaseModelWithUID

from productio.models import Product

from .choices import InvoiceStatusChoices
from .utils import get_invoice_item_slug, get_invoice_slug


class InvoiceItem(BaseModelWithUID):
    slug = AutoSlugField(
        populate_from=get_invoice_item_slug, unique=True, db_index=True
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"ID: {self.id}, Product Title: {self.product.title}"


class Invoice(BaseModelWithUID):
    slug = AutoSlugField(populate_from=get_invoice_slug, unique=True, db_index=True)
    invoice_item = models.ForeignKey(InvoiceItem, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20, choices=InvoiceStatusChoices, default=InvoiceStatusChoices.UNPAID
    )
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quantity = models.IntegerField()
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return f"ID: {self.id}, Company Name: {self.company_name}"
