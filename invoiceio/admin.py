from django.contrib import admin

from .models import InvoiceItem, Invoice, InvoiceItemConnector


@admin.register(InvoiceItem)
class InvoiceImtemAdmin(admin.ModelAdmin):
    model = InvoiceItem
    list_display = (
        "uid",
        "slug",
        "total",
        "quantity",
    )
    search_fields = ("uid", "slug")
    readonly_fields = ("total",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    list_display = (
        "uid",
        "slug"
    )
    search_fields = ("uid", "slug")


@admin.register(InvoiceItemConnector)
class InvoiceItemConnectorAdmin(admin.ModelAdmin):
    model = InvoiceItemConnector
    list_display = ("uid", "slug")
    search_fields = ("uid", "slug")
