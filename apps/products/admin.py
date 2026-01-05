from django.contrib import admin
from .models import Product,ProductImage
from django.utils.timezone import now
#___________________________________________________________________________________________
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "category",
        "product_type",
        "rent_price",
        "sell_price",
        "deposit_price",
        "is_active",
        "is_published",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "product_type",
        "category",
        "is_active",
        "is_published",
        "is_approved",
    )

    search_fields = ("title",)

    actions = ["approve_products"]

    def approve_products(self, request, queryset):
        queryset.update(
            is_approved=True,
            approved_at=now()
        )

    approve_products.short_description = "Approve selected products"
#___________________________________________________________________________________________
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display =("product", "image")
    list_filter = ("product", "image")
