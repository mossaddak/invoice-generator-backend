from django.contrib import admin

from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = (
        "uid",
        "slug",
        "username",
        "email",
        "status",
    )
    search_fields = (
        "uid",
        "slug",
        "id",
        "email",
        "phone",
        "status",
        "created_at",
    )