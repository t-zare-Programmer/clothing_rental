from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "product_type",
        "rent_price",
        "sell_price",
        "deposit_price",
        "is_active",
        "created_at",
    )

    list_filter = (
        "product_type",
        "category",
        "is_active",
    )

    search_fields = ("title",)
