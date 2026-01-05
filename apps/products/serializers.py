from rest_framework import serializers
from .models import Product, ProductImage

# =========================================================================================
# Product List (Public)
# =========================================================================================
class ProductListSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(
        source="category.title",
        read_only=True
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
            "cover_image",
        )


# =========================================================================================
# Product Images
# =========================================================================================
MAX_PRODUCT_IMAGES = 5

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
            "created_at",
            "product",
        )

    def validate(self, attrs):
        product = attrs.get("product")

        images_count = ProductImage.objects.filter(product=product).count()

        if images_count >= MAX_PRODUCT_IMAGES:
            raise serializers.ValidationError({
                "image": f"برای هر محصول حداکثر {MAX_PRODUCT_IMAGES} تصویر مجاز است."
            })

        return attrs


# =========================================================================================
# Product Detail (Public)
# =========================================================================================
class ProductDetailSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(
        source="category.title",
        read_only=True
    )

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "product_type",
            "sell_price",
            "rent_price",
            "deposit_price",
            "cover_image",
            "category",
            "category_title",
            "images",
        )


# =========================================================================================
# Product Create / Update (User)
# =========================================================================================
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    ✔ کاربر فقط می‌تواند محصول را بسازد یا ویرایش کند
    ❌ هیچ دسترسی به approve / owner / approved_at ندارد
    """

    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "product_type",
            "sell_price",
            "rent_price",
            "deposit_price",
            "category",
            "cover_image",
            "is_published",   # فقط درخواست انتشار
        )

    def validate(self, attrs):
        instance = self.instance

        product_type = attrs.get(
            "product_type",
            instance.product_type if instance else None
        )
        rent_price = attrs.get(
            "rent_price",
            instance.rent_price if instance else None
        )
        deposit_price = attrs.get(
            "deposit_price",
            instance.deposit_price if instance else None
        )
        sell_price = attrs.get(
            "sell_price",
            instance.sell_price if instance else None
        )

        errors = {}

        if product_type == "rent":
            if rent_price is None:
                errors["rent_price"] = "برای محصول اجاره‌ای وارد کردن rent_price الزامی است."
            if deposit_price is None:
                errors["deposit_price"] = "برای محصول اجاره‌ای وارد کردن deposit_price الزامی است."
            if sell_price is not None:
                errors["sell_price"] = "برای محصول اجاره‌ای نباید sell_price وارد شود."

        elif product_type == "sell":
            if sell_price is None:
                errors["sell_price"] = "برای محصول فروشی وارد کردن sell_price الزامی است."
            if rent_price is not None:
                errors["rent_price"] = "برای محصول فروشی نباید rent_price وارد شود."
            if deposit_price is not None:
                errors["deposit_price"] = "برای محصول فروشی نباید deposit_price وارد شود."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        """
        امنیت اصلی اینجاست
        """
        request = self.context["request"]

        validated_data["owner"] = request.user
        validated_data["is_approved"] = False
        validated_data["approved_at"] = None

        return super().create(validated_data)


# =========================================================================================
# Product Admin Serializer
# =========================================================================================
class ProductAdminSerializer(serializers.ModelSerializer):
    """
    فقط برای ادمین
    """

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = (
            "owner",
            "approved_at",
        )
