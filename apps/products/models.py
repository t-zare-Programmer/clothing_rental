from django.db import models
from django.core.exceptions import ValidationError
from apps.categories.models import Category


class Product(models.Model):

    class ProductType(models.TextChoices):
        RENT = "rent", "اجاره‌ای"
        SELL = "sell", "فروشی"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    product_type = models.CharField(
        max_length=10,
        choices=ProductType.choices
    )

    rent_price = models.PositiveIntegerField(null=True, blank=True)
    sell_price = models.PositiveIntegerField(null=True, blank=True)
    deposit_price = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.product_type == "rent" and not self.rent_price:
            raise ValidationError("برای محصول اجاره‌ای، قیمت اجاره الزامی است.")

        if self.product_type == "sell" and not self.sell_price:
            raise ValidationError("برای محصول فروشی، قیمت فروش الزامی است.")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to='media/products/images/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Image for {self.product.title}"