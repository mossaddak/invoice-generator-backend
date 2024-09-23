from django.urls import path, include

urlpatterns = [
    path(
        "invoices",
        include("meapi.django_rest.urls.invoices"),
    )
    
]
