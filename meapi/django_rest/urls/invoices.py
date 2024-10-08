from django.urls import path

from ..views.invoices import (
    PrivateMeInvoiceItemList,
    PrivateMeInvoiceItemDetails,
    PrivateMeInvoiceList,
    PrivateMeInvoiceDetails,
)

urlpatterns = [
    path("-items", PrivateMeInvoiceItemList.as_view(), name="meapi.invoice-items-list"),
    path(
        "-items/<uuid:uid>",
        PrivateMeInvoiceItemDetails.as_view(),
        name="meapi.invoice-items-details",
    ),
    path(
        "/<uuid:uid>",
        PrivateMeInvoiceDetails.as_view(),
        name="meapi.invoice-details",
    ),
    path("", PrivateMeInvoiceList.as_view(), name="meapi.invoice-list"),
]
