from django.contrib import admin, messages
from django.utils.html import format_html

from .models import (
    Brand, Category, CategoryFilter, CategoryQuickLink, Product, ProductImage, ProductSpec,
    SpecType, UseCase, make_unique_slug,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ("image", "alt", "order")


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 8
    fields = ("spec_type", "value", "filter_value", "order")


class CategoryFilterInline(admin.TabularInline):
    model = CategoryFilter
    extra = 1
    fields = ("source", "spec_type", "title", "order", "is_active")
    autocomplete_fields = ("spec_type",)


class CategoryQuickLinkInline(admin.TabularInline):
    model = CategoryQuickLink
    extra = 1
    fields = ("label", "use_cases", "order", "is_active")
    autocomplete_fields = ("use_cases",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "thumb", "title", "category", "brand", "price", "status",
        "is_published", "is_featured", "is_demo",
    )
    list_display_links = ("thumb", "title")
    list_editable = ("price", "status", "is_published", "is_featured")
    list_filter = ("category", "brand", "status", "is_published", "is_featured", "is_demo")
    search_fields = ("title", "brand__name", "specs__value")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("use_cases",)
    inlines = [ProductSpecInline, ProductImageInline]
    list_per_page = 30
    save_on_top = True
    actions = ["duplicate", "publish", "unpublish"]
    fieldsets = (
        ("Основное", {"fields": ("title", "slug", "category", "brand", "short_description")}),
        ("Цена и наличие", {"fields": ("price", "old_price", "status", "installment_available")}),
        ("Состояние и доставка", {"fields": ("condition", "delivery", "location", "warranty")}),
        ("Описание", {"fields": ("description", "use_cases")}),
        ("Публикация", {"fields": ("is_published", "is_featured", "is_demo")}),
    )

    @admin.display(description="Фото")
    def thumb(self, obj):
        image = obj.main_image
        if image and image.image:
            return format_html('<img src="{}" style="height:44px;border-radius:6px">', image.image.url)
        return "—"

    @admin.action(description="Дублировать выбранные товары (с характеристиками и фото)")
    def duplicate(self, request, queryset):
        for product in queryset.prefetch_related("specs", "images", "use_cases"):
            specs, images, use_cases = list(product.specs.all()), list(product.images.all()), list(product.use_cases.all())
            product.pk = None
            product.title = f"{product.title} (копия)"
            product.slug = make_unique_slug(Product, product.title, 220)
            product.is_published = False
            product.is_featured = False
            product.save()
            product.use_cases.set(use_cases)
            for spec in specs:
                spec.pk = None
                spec.product = product
                spec.save()
            for image in images:
                image.pk = None
                image.product = product
                image.save()
        self.message_user(request, "Копии созданы и скрыты с сайта. Проверьте и опубликуйте.", messages.SUCCESS)

    @admin.action(description="Показать на сайте")
    def publish(self, request, queryset):
        self.message_user(request, f"Опубликовано: {queryset.update(is_published=True)}")

    @admin.action(description="Скрыть с сайта")
    def unpublish(self, request, queryset):
        self.message_user(request, f"Скрыто: {queryset.update(is_published=False)}")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "display_mode", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "display_mode", "parent")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CategoryFilterInline, CategoryQuickLinkInline]
    fieldsets = (
        ("Раздел", {"fields": ("name", "slug", "parent", "icon", "image", "description")}),
        (
            "Что показывать на странице",
            {
                "fields": ("display_mode", "quick_links_title", "order", "is_active"),
                "description": "Подраздел без своих фильтров использует фильтры ближайшего родителя.",
            },
        ),
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(UseCase)
class UseCaseAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "order")
    list_editable = ("icon", "order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(SpecType)
class SpecTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    search_fields = ("name",)
