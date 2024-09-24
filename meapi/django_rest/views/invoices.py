from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from invoiceio.models import InvoiceItem, Invoice, InvoiceItemConnector

from ..serializer.invoices import (
    PrivateMeInvoiceItemListSerializer,
    PrivateMeInvoiceItemDetailsSerializer,
    PrivateMeInvoiceListSerializer,
    PrivateMeInvoiceDetailSerializer,
)


class PrivateMeInvoiceItemList(ListCreateAPIView):
    serializer_class = PrivateMeInvoiceItemListSerializer

    def get_queryset(self):
        return InvoiceItem.objects.filter(customer=self.request.user)


class PrivateMeInvoiceItemDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateMeInvoiceItemDetailsSerializer

    def get_object(self):
        return get_object_or_404(
            InvoiceItem.objects.filter(),
            customer=self.request.user,
            uid=self.kwargs.get("uid", None),
        )


class PrivateMeInvoiceList(ListCreateAPIView):
    serializer_class = PrivateMeInvoiceListSerializer

    def get_queryset(self):
        invoice_ids = (
            InvoiceItemConnector.objects.filter(
                invoice_item__customer=self.request.user
            )
            .distinct()
            .values_list("invoice_id", flat=True)
        )
        return Invoice.objects.filter(id__in=invoice_ids)


class PrivateMeInvoiceDetails(RetrieveDestroyAPIView):
    serializer_class = PrivateMeInvoiceDetailSerializer

    def get_object(self):
        return get_object_or_404(
            Invoice.objects.filter(),
            uid=self.kwargs.get("uid", None),
        )
