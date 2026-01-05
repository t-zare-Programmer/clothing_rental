from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import Product, ProductImage
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    ProductImageSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .permissions import IsOwnerOrReadOnly,IsProductOwnerOrReadOnly
from core.pagination import DefaultPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


#___________________________________________________________________________________________
class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer
    pagination_class = DefaultPagination

    # ====================================================================================
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, is_published=True,is_approved=True,status=Product.Status.PUBLISHED)

        category_id = self.request.query_params.get("category")
        product_type = self.request.query_params.get("type")  # rent | sell

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if product_type in ["rent", "sell"]:
            queryset = queryset.filter(product_type=product_type)

        return queryset

    # ====================================================================================
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    # ====================================================================================
    def get_permissions(self):
        if self.request.method == "POST":
            # فقط کاربران لاگین شده می‌توانند محصول بسازند
            return [permissions.IsAuthenticated()]
        # همه می‌توانند مشاهده کنند
        return [permissions.AllowAny()]

    # ====================================================================================
    def perform_create(self, serializer):
        # ست کردن Owner خودکار هنگام ساخت محصول
        serializer.save(owner=self.request.user)
    #====================================================================================
    @extend_schema(
        summary="List products",
        description="Get list of active products with optional filters",
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by category id",
            ),
            OpenApiParameter(
                name="type",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by product type (rent | sell)",
                enum=["rent", "sell"],
            ),
        ],
        responses={200: ProductListSerializer(many=True)},
    )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    #====================================================================================
    @extend_schema(
        summary="Create product",
        description="Create a new product (authenticated users only)",
        request=ProductCreateUpdateSerializer,
        responses={201: ProductDetailSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


#___________________________________________________________________________________________
@extend_schema(
    description="""
Retrieve, update or delete a product.
Only the product owner can update or delete the product.
Other users can only view it.
"""
)
# مشاهده، بروزرسانی و حذف محصول خاص
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Product.objects.filter(
                Q(is_active=True, is_published=True, is_approved=True)
                |
                Q(owner=user)
            )

        return Product.objects.filter(
            is_active=True,
            is_published=True,
            is_approved=True
        )

    # Soft Delete
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

#________________________________________________________________________________________________________
class ProductImageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductImageSerializer

    # ====================================================================================
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        # مشاهده فقط برای همه، و ویرایش/حذف فقط برای مالک محصول
        return [IsProductOwnerOrReadOnly()]

    # ====================================================================================
    @extend_schema(
        summary="List product images",
        description="Get product images with optional filters",
        parameters=[
            OpenApiParameter(
                name="product_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter images by product id",
            ),
            OpenApiParameter(
                name="category_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter images by product category id",
            ),
        ],
        responses={200: ProductImageSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    # ====================================================================================
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

    # ====================================================================================
    @extend_schema(
        summary="Upload product image",
        description="Upload image for a product (only product owner)",
        request=ProductImageSerializer,
        responses={201: ProductImageSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#________________________________________________________________________________________________________
@extend_schema(
    description="""
Retrieve or delete a product image.
Only the product owner can delete the image.
Other users can only view it.
"""
)
class ProductImageDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsProductOwnerOrReadOnly
    ]
#________________________________________________________________________________________________________
class ProductPublishAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, owner=request.user)

        product.status = Product.Status.PENDING_REVIEW
        product.is_published = False
        product.is_approved = False
        product.save(update_fields=[
            'status',
            'is_published',
            'is_approved',
        ])

        return Response(
            {"جزییات": "محصول با موفقیت انتشار یافت"},
            status=status.HTTP_200_OK
        )