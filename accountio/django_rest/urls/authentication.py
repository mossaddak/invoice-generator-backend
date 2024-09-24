from django.urls import path, include

from ..views.authentication import CustomerRegistrationView, CustomerLoginView

urlpatterns = [
    path(
        r"create",
        CustomerRegistrationView.as_view(),
        name="accountio.customer-registration",
    ),
    path(
        r"login",
        CustomerLoginView.as_view(),
        name="accountio.customer-login",
    )
]
