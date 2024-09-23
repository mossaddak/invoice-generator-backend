from rest_framework import serializers

from invoiceio.models import InvoiceItem, Invoice

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

    def update(self, instance,  validated_data):
        instance.product = validated_data.pop("product_slug", None)
        return super().update(instance, validated_data)
