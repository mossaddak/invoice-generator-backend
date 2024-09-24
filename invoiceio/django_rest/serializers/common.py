from rest_framework import serializers

from invoiceio.models import InvoiceItem


class InvoiceItemSlimSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceItem
        fields = [
            "uid",
            "title",
            "total",
            "quantity",
            "created_at",
        ]
