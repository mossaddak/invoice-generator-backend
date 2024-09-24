from django.urls import path, include

urlpatterns = [
    path(
        "account/",
        include("accountio.django_rest.urls.authentication"),
    )
]
