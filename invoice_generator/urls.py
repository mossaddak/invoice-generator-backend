from django.contrib import admin
from django.urls import path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Change Admin Top Nav Header
admin.site.site_header = "Invoice Generator"

schema_view = get_schema_view(
    openapi.Info(title="Invoice Generator API", default_version="main"),
    public=False,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Swagger
    path(
        r"api/v1/docs",
        schema_view.with_ui("swagger", cache_timeout=10),
        name="schema-swagger-ui",
    ),
    path('admin/', admin.site.urls),
]
