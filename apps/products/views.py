from rest_framework import generics, permissions
from .models import Product, ProductImage
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateSerializer,
    ProductImageSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .permissions import IsOwnerOrReadOnly

#___________________________________________________________________________________________
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

    def get_permissions(self):
        if self.request.method == "POST":
            # فقط کاربران لاگین شده می‌توانند محصول بسازند
            return [permissions.IsAuthenticated()]
        # همه می‌توانند مشاهده کنند
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # ست کردن Owner خودکار هنگام ساخت محصول
        serializer.save(owner=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter by category id",
            ),
            OpenApiParameter(
                name="type",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter by product type (rent | sell)",
                enum=["rent", "sell"],
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

#___________________________________________________________________________________________
# مشاهده، بروزرسانی و حذف محصول خاص
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

#___________________________________________________________________________________________
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
