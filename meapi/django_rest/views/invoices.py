from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from invoiceio.models import InvoiceItem

from ..serializer.invoices import PrivateMeInvoiceItemListSerializer, PrivateMeInvoiceItemDetailsSerializer


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
            uid = self.kwargs.get("uid", None)
        )
