from rest_framework import serializers
from .models import Product,ProductImage


class ProductListSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(
        source="category.title", read_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "category",
            "category_title",
            "product_type",
            "rent_price",
            "sell_price",
        )

class ProductDetailSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(
        source="category.title", read_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "category",
            "product_type",
            "rent_price",
            "sell_price",
            "deposit_price",
        ]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'created_at')