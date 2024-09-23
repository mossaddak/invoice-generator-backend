from rest_framework import serializers

from invoiceio.models import InvoiceItem, Invoice, InvoiceItemConnector

from productio.choices import ProductStatusChoices
from productio.django_rest.serializers.common import ProvateMeProductSlimSerialize
from productio.models import Product


class PrivateMeInvoiceItemListSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.filter(status=ProductStatusChoices.ACTIVE),
        slug_field="slug",
        write_only=True,
    )

    class Meta:
        model = InvoiceItem
        fields = ["uid", "title", "customer", "product", "total", "quantity"]
        read_only_fields = ["uid", "title", "customer", "total"]

    def create(self, validated_data):
        return InvoiceItem.objects.create(
            customer=self.context["request"].user, **validated_data
        )


class PrivateMeInvoiceItemDetailsSerializer(serializers.ModelSerializer):
    product = ProvateMeProductSlimSerialize(read_only=True)
    product_slug = serializers.SlugRelatedField(
        queryset=Product.objects.filter(status=ProductStatusChoices.ACTIVE),
        slug_field="slug",
        write_only=True,
    )

    class Meta:
        model = InvoiceItem
        fields = [
            "uid",
            "title",
            "customer",
            "product",
            "product_slug",
            "total",
            "quantity",
            "created_at",
        ]
        read_only_fields = ["uid", "title", "customer", "total", "created_at"]

    def update(self, instance, validated_data):
        instance.product = validated_data.pop("product_slug", None)
        return super().update(instance, validated_data)


class PrivateMeInvoiceListSerializer(serializers.ModelSerializer):
    # total = serializers.CharField(source="get_total", read_only=True)
    invoice_item_uuid_list = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Invoice
        fields = [
            "uid",
            "title",
            "issue_date",
            "due_date",
            # "total",
            "paid_amount",
            "status",
            "tax",
            "quantity",
            "company_name",
            "invoice_item_uuid_list",
        ]
        read_only_fields = ["uid", "title", "total", "issue_date", "status"]

    def create(self, validated_data):
        customer = self.context["request"].user
        invoice_item_uuid_list = validated_data.pop("invoice_item_uuid_list", None)
        
        invoice = Invoice.objects.create(**validated_data)

        
        if invoice_item_uuid_list:
            invoice_items = InvoiceItem.objects.filter(
                uid__in=invoice_item_uuid_list, invoice_item__customer=customer
            )

            for item in invoice_items:
                InvoiceItemConnector.objects.create(invoice=invoice, invoice_item=item)
