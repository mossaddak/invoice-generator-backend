from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from invoiceio.choices import InvoiceStatusChoices
from invoiceio.django_rest.serializers.common import InvoiceItemSlimSerializer
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
        fields = [
            "uid",
            "title",
            "product",
            "total",
            "quantity",
            "created_at",
        ]
        read_only_fields = ["uid", "title", "total", "created_at"]

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
    total = serializers.CharField(source="get_total", read_only=True)
    quantity = serializers.CharField(source="get_quantity", read_only=True)
    invoice_item_uuid_list = serializers.ListField(write_only=True)

    class Meta:
        model = Invoice
        fields = [
            "uid",
            "company_name",
            "issue_date",
            "due_date",
            "total",
            "paid_amount",
            "status",
            "tax",
            "quantity",
            "invoice_item_uuid_list",
        ]
        read_only_fields = ["uid", "title", "total", "issue_date", "status", "quantity"]

    def validate(self, attrs):
        customer = self.context["request"].user
        invoice_item_uuid_list = attrs.pop("invoice_item_uuid_list", None)
        tax = attrs["tax"]
        paid_amount = attrs["paid_amount"]
        due_date = attrs["due_date"]

        if due_date < timezone.now().date():
            raise serializers.ValidationError(
                {"due_date": "Due date cannot be before the issue date."}
            )

        # Getting associate invoice items
        invoice_items = InvoiceItem.objects.filter(
            uid__in=invoice_item_uuid_list, customer=customer
        )
        invoice_total = sum(invoice_item.total for invoice_item in invoice_items) + tax

        if paid_amount == 0:
            invoice_status = InvoiceStatusChoices.UNPAID
        elif paid_amount == invoice_total:
            invoice_status = InvoiceStatusChoices.PAID
        elif timezone.now().date() > due_date and paid_amount != invoice_total:
            invoice_status = InvoiceStatusChoices.OVERDUE
        else:
            invoice_status = InvoiceStatusChoices.PARTIAL

        attrs["status"] = invoice_status
        attrs["invoice_items"] = invoice_items
        return attrs

    def create(self, validated_data):
        invoice_items = validated_data.pop("invoice_items", None)
        
        with transaction.atomic():

            # Create invoice
            invoice = Invoice.objects.create(**validated_data)

            # Create relations between invoice and invoice items
            InvoiceItemConnector.objects.bulk_create(
                [
                    InvoiceItemConnector(invoice=invoice, invoice_item=invoice_item)
                    for invoice_item in invoice_items
                ]
            )
        return invoice


class PrivateMeInvoiceDetailSerializer(serializers.ModelSerializer):
    total = serializers.CharField(source="get_total", read_only=True)
    quantity = serializers.CharField(source="get_quantity", read_only=True)
    invoice_items = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "uid",
            "company_name",
            "issue_date",
            "due_date",
            "total",
            "paid_amount",
            "status",
            "tax",
            "quantity",
            "invoice_items",
        ]
        read_only_fields = [
            "uid",
            "title",
            "total",
            "issue_date",
            "status",
            "quantity",
            "invoice_items",
        ]

    def get_invoice_items(self, instance):
        connectors = instance.invoiceitemconnector_set.all().select_related(
            "invoice_item"
        )
        return InvoiceItemSlimSerializer(
            [connector.invoice_item for connector in connectors], many=True
        ).data
