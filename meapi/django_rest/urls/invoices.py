from django.urls import path

from ..views.invoices import PrivateMeInvoiceItemList, PrivateMeInvoiceItemDetails

urlpatterns = [
    path("-items", PrivateMeInvoiceItemList.as_view(), name="meapi.invoice-items-list"),
    path(
        "-items/<uuid:uid>", PrivateMeInvoiceItemDetails.as_view(), name="meapi.invoice-items-details"
    ),
]
