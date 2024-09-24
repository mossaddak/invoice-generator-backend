from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from invoiceio.models import InvoiceItem, Invoice, InvoiceItemConnector

from ...file_helpers import create_invoice

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
        invoice = get_object_or_404(
            Invoice.objects.filter(),
            uid=self.kwargs.get("uid", None),
        )

        invoice_item_ids = invoice.invoiceitemconnector_set.filter(
            invoice_item__customer=self.request.user
        ).values_list("invoice_item_id", flat=True)
        invoice_items = InvoiceItem.objects.filter(id__in=invoice_item_ids).values(
            "title", "quantity", "total"
        )
        total_amount = invoice.get_total()
        if self.request.query_params.get("download_invoice", None) == "true":
            invoice_url = create_invoice(
                self.request,
                invoice.company_name,
                invoice.issue_date,
                invoice.due_date,
                total_amount,
                invoice.paid_amount,
                invoice_items,
                filename=f"invoice-{invoice.uid}.pdf",
            )
            invoice.file = invoice_url
            invoice.save()
        return invoice
