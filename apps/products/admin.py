from django.contrib import admin
from .models import Product,ProductImage

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

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display =("product", "image")
    list_filter = ("product", "image")
