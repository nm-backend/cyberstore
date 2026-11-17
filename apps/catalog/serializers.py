from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Brand, Category, Product, ProductImage, ProductSpec, UseCase


class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source="parent.name", read_only=True, default=None)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "parent_name", "icon", "description", "order", "is_active"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug"]


class UseCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseCase
        fields = ["id", "name", "slug", "icon", "order"]


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt", "order"]


class ProductSpecSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="spec_type.name", read_only=True)

    class Meta:
        model = ProductSpec
        fields = ["id", "name", "value", "order"]


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    brand = BrandSerializer(read_only=True)
    main_image = serializers.SerializerMethodField()
    url = serializers.URLField(source="get_absolute_url", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "title", "slug", "short_description", "price", "old_price",
            "status", "discount_percent", "category", "brand", "main_image",
            "is_featured", "installment_available", "warranty", "url",
            "created_at", "updated_at",
        ]

    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_main_image(self, obj):
        img = obj.main_image
        if img and img.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(img.image.url)
            return img.image.url
        return None


class ProductDetailSerializer(ProductListSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    specs = ProductSpecSerializer(many=True, read_only=True)
    use_cases = UseCaseSerializer(many=True, read_only=True)

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + [
            "description", "images", "specs", "use_cases",
        ]
