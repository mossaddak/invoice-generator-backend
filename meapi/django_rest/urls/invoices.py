from django.urls import path

from ..views.invoices import PrivateMeInvoiceItemList, PrivateMeInvoiceItemDetails, PrivateMeInvoiceList

urlpatterns = [
    path("-items", PrivateMeInvoiceItemList.as_view(), name="meapi.invoice-items-list"),
    path(
        "-items/<uuid:uid>", PrivateMeInvoiceItemDetails.as_view(), name="meapi.invoice-items-details"
    ),
    path("", PrivateMeInvoiceList.as_view(), name="meapi.invoice-list")
]
