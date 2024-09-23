from autoslug import AutoSlugField

from django.core.exceptions import ValidationError
from django.utils import timezone

from django.db import models

from accountio.models import Customer

from common.models import BaseModelWithUID

from .choices import InvoiceStatusChoices
from .utils import get_invoice_item_slug, get_invoice_slug, get_invoice_item_connector_slug


class InvoiceItem(BaseModelWithUID):
    slug = AutoSlugField(
        populate_from=get_invoice_item_slug, unique=True, db_index=True
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey("productio.Product", on_delete=models.CASCADE)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f"ID: {self.id}, Product Title: {self.product.title}"

    def save(self, *args, **kwargs):
        self.total = (
            self.product.get_discounted_price() or self.product.price
        ) * self.quantity
        self.title = self.product.title
        super().save(*args, **kwargs)


class Invoice(BaseModelWithUID):
    slug = AutoSlugField(populate_from=get_invoice_slug, unique=True, db_index=True)
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20, choices=InvoiceStatusChoices, default=InvoiceStatusChoices.UNPAID
    )
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quantity = models.IntegerField()
    company_name = models.CharField(max_length=50)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"ID: {self.id}, Company Name: {self.company_name}"
    
    def clean(self):
        super().clean()  # Call the parent's clean method
        if self.due_date < self.issue_date.date():
            raise ValidationError({'due_date': "Due date cannot be before the issue date."})


    def save(self, *args, **kwargs):
        if self.paid_amount == 0:
            self.payment_status = InvoiceStatusChoices.UNPAID
        elif self.paid_amount == self.total:
            self.payment_status = InvoiceStatusChoices.PAID
        elif timezone.now().date() > self.due_date and self.paid_amount != self.total:
            self.payment_status = InvoiceStatusChoices.OVERDUE
        self.quantity = self.invoice_items.all().count
        super().save(*args, **kwargs)

    # def get_total(self):
    #     return (
    #         sum(invoiceitem.get_total() for invoiceitem in self.invoice_items.all())
    #         + self.tax
    #     )
    
class InvoiceItemConnector(BaseModelWithUID):
    slug = AutoSlugField(populate_from=get_invoice_item_connector_slug, unique=True, db_index=True)
    invoice_item = models.ForeignKey(InvoiceItem, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id}, Invoice Item: {self.invoice_item}"
