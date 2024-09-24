from rest_framework import generics
from rest_framework.permissions import AllowAny

from accountio.django_rest.serializers.authentication import (
    CustomerRegistrationSerializer,
    CustomerLoginSerializer
)


class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [AllowAny]

class CustomerLoginView(generics.CreateAPIView):
    serializer_class = CustomerLoginSerializer
    permission_classes = [AllowAny]