from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Brand, Category, Product, UseCase
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    UseCaseSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Категории товаров."""

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """Бренды."""

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class UseCaseViewSet(viewsets.ReadOnlyModelViewSet):
    """Теги «Подходит для»."""

    queryset = UseCase.objects.all()
    serializer_class = UseCaseSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Товары каталога (только опубликованные)."""

    queryset = Product.objects.published().with_cards()
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer
