import logging

from rest_framework import serializers

from ...models import Customer
from ...utils import get_token

logger = logging.getLogger(__name__)


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "uid",
            "slug",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "password",
        ]
        read_only_fields = ["uid", "slug"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Customer.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class CustomerLoginSerializer(serializers.Serializer):
    username = serializers.SlugRelatedField(
        queryset=Customer.objects.all(), slug_field="username", write_only=True
    )
    password = serializers.CharField(write_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user = Customer.objects.get(username=username.username)
        except Customer.DoesNotExist:
            raise serializers.ValidationError({"detail": "Invalid credential!"})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid credential!"})

        # If you have a function to generate tokens
        attrs["refresh"], attrs["access"] = get_token(
            user
        )  # Replace with your token generation logic

        return attrs

    def create(self, validated_data):
        return validated_data