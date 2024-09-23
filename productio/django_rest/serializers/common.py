from rest_framework import serializers 

from productio.models import Product


class BaseProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.CharField(
        source="get_discounted_price", read_only=True
    )

    class Meta:
        model = Product
        fields = ["title", "price", "discounted_price"]


class ProvateMeProductSlimSerialize(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        fields = ["uid"] + BaseProductSerializer.Meta.fields


class PublicProductSlimSerialize(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        fields = ["slug"] + BaseProductSerializer.Meta.fields
