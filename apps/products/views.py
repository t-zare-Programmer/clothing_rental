from rest_framework import generics,permissions
from .models import Product,ProductImage
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateSerializer,
    ProductImageSerializer,
)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        category_id = self.request.query_params.get("category")
        product_type = self.request.query_params.get("type")  # rent | sell

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if product_type in ["rent", "sell"]:
            queryset = queryset.filter(product_type=product_type)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductListSerializer



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer


class ProductImageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ProductImage.objects.all()

        # فیلتر بر اساس شناسه محصول
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        # فیلتر بر اساس دسته‌بندی
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(product__category_id=category_id)

        return queryset
