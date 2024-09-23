from django.contrib import admin

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = (
        "uid",
        "slug",
        "title",
        "price",
        "discount",
    )
    search_fields = (
        "uid",
        "slug",
        "title",
        "status"
    )
    readonly_fields = ("price",)