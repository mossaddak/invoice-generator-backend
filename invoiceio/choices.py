from django.db import models


class InvoiceStatusChoices(models.TextChoices):
    PAID = "PAID", "Paid"
    UNPAID = "UNPAID", "Un Paid"
    OVERDUE = "OVERDUE", "Overdue"
    PARTIAL = "PARTIAL", "Partial"
