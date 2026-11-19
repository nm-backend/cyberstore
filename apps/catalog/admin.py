from django.contrib import admin, messages
from django.db.models import Count, Max
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Brand, Category, CategoryFilter, CategoryQuickLink, Product, ProductImage, ProductSpec,
    SpecOption, SpecType, UseCase, make_unique_slug,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ("image", "alt", "order")


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 8
    fields = ("spec_type", "option", "value", "filter_value", "order")
    autocomplete_fields = ("spec_type", "option")
    verbose_name = "Характеристика товара"
    verbose_name_plural = "Характеристики товара (значения видны в карточке и фильтрах)"


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


class SpecOptionInline(admin.TabularInline):
    model = SpecOption
    extra = 3
    fields = ("name", "order", "is_active", "used_by")
    readonly_fields = ("used_by",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(used_total=Count("product_specs", distinct=True))

    @admin.display(description="Товаров")
    def used_by(self, obj):
        return getattr(obj, "used_total", 0)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "thumb", "title", "category", "brand", "price", "status",
        "is_published", "is_featured", "is_demo",
    )
    list_display_links = ("thumb", "title")
    list_editable = ("price", "status", "is_published", "is_featured")
    list_filter = ("category", "brand", "status", "is_published", "is_featured", "is_demo")
    search_fields = ("title", "brand__name", "specs__value", "specs__option__name")
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
    list_display = ("name", "parent", "display_mode", "show_brand_tiles", "own_products", "filters_total", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "display_mode", "show_brand_tiles", "parent")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CategoryFilterInline, CategoryQuickLinkInline]
    fieldsets = (
        ("Раздел", {"fields": ("name", "slug", "parent", "icon", "image", "description")}),
        (
            "Что показывать на странице",
            {
                "fields": ("display_mode", "show_brand_tiles", "quick_links_title", "order", "is_active"),
                "description": "Подраздел без своих фильтров использует фильтры ближайшего родителя.",
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_total=Count("products", distinct=True),
            filters_count=Count("filters", distinct=True),
        )

    @admin.display(description="Товаров", ordering="products_total")
    def own_products(self, obj):
        return getattr(obj, "products_total", 0)

    @admin.display(description="Фильтров", ordering="filters_count")
    def filters_total(self, obj):
        return getattr(obj, "filters_count", 0)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "logo_thumb", "categories_label", "products_total", "is_active", "slug")
    list_editable = ("is_active",)
    list_filter = ("is_active", "categories")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("categories",)
    fieldsets = (
        ("Бренд", {"fields": ("name", "slug", "logo", "is_active")}),
        (
            "Категории",
            {
                "fields": ("categories",),
                "description": "Где показывать бренд. Пусто — во всех категориях, где есть его товары.",
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("categories").annotate(
            products_total=Count("products", distinct=True)
        )

    @admin.display(description="Логотип")
    def logo_thumb(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:32px;border-radius:4px">', obj.logo.url)
        return "—"

    @admin.display(description="Товаров", ordering="products_total")
    def products_total(self, obj):
        return getattr(obj, "products_total", 0)

    @admin.display(description="Категории")
    def categories_label(self, obj):
        names = [category.name for category in obj.categories.all()]
        return ", ".join(names) if names else "Все категории"


@admin.register(UseCase)
class UseCaseAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "order")
    list_editable = ("icon", "order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(SpecType)
class SpecTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name", "data_type", "unit", "categories_label", "options_link",
        "products_total", "is_active", "order",
    )
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "data_type", "categories")
    search_fields = ("name", "options__name")
    filter_horizontal = ("categories",)
    inlines = [SpecOptionInline]
    save_on_top = True
    actions = ("activate", "deactivate")
    fieldsets = (
        ("Характеристика", {"fields": ("name", "data_type", "unit", "order", "is_active")}),
        (
            "Где показывать",
            {
                "fields": ("categories",),
                "description": "Выберите разделы, где характеристика доступна для товаров и фильтров. "
                               "Значения ниже сразу появляются в фильтрах каталога.",
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("categories").annotate(
            options_total=Count("options", distinct=True),
            products_count=Count("options__product_specs__product", distinct=True),
        )

    @admin.display(description="Значения", ordering="options_total")
    def options_link(self, obj):
        url = reverse("admin:catalog_specoption_changelist")
        return format_html('<a href="{}?spec_type__id__exact={}">{} знач.</a>', url, obj.pk, getattr(obj, "options_total", 0))

    @admin.display(description="Товаров", ordering="products_count")
    def products_total(self, obj):
        return getattr(obj, "products_count", 0)

    @admin.display(description="Категории")
    def categories_label(self, obj):
        names = [category.name for category in obj.categories.all()]
        return ", ".join(names) if names else "Все разделы"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if change:
            return
        spec_type = form.instance
        for category in spec_type.categories.all():
            next_order = (
                CategoryFilter.objects.filter(category=category).aggregate(Max("order"))["order__max"] or 0
            ) + 1
            CategoryFilter.objects.get_or_create(
                category=category,
                spec_type=spec_type,
                defaults={"source": "spec", "order": next_order, "is_active": True},
            )

    @admin.action(description="Включить выбранные характеристики")
    def activate(self, request, queryset):
        self.message_user(request, f"Включено: {queryset.update(is_active=True)}")

    @admin.action(description="Отключить выбранные характеристики")
    def deactivate(self, request, queryset):
        self.message_user(request, f"Отключено: {queryset.update(is_active=False)}")


@admin.register(SpecOption)
class SpecOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "spec_type", "categories_label", "products_total", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "spec_type", "spec_type__categories")
    search_fields = ("name", "spec_type__name")
    list_select_related = ("spec_type",)
    save_on_top = True
    actions = ("activate", "deactivate")
    fieldsets = (
        (
            "Значение фильтра",
            {
                "fields": ("spec_type", "name", "order", "is_active"),
                "description": "Новое значение сразу появляется в фильтре своего раздела. "
                               "Отключённое значение скрывается из фильтра, но остаётся у старых товаров.",
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("spec_type").prefetch_related(
            "spec_type__categories"
        ).annotate(products_count=Count("product_specs__product", distinct=True))

    @admin.display(description="Товаров", ordering="products_count")
    def products_total(self, obj):
        return getattr(obj, "products_count", 0)

    @admin.display(description="Категории")
    def categories_label(self, obj):
        names = [category.name for category in obj.spec_type.categories.all()]
        return ", ".join(names) if names else "Все разделы"

    @admin.action(description="Включить выбранные значения")
    def activate(self, request, queryset):
        self.message_user(request, f"Включено: {queryset.update(is_active=True)}")

    @admin.action(description="Отключить выбранные значения")
    def deactivate(self, request, queryset):
        self.message_user(request, f"Отключено: {queryset.update(is_active=False)}")

    def delete_model(self, request, obj):
        used = obj.product_specs.values("product_id").distinct().count()
        if used:
            self.message_user(
                request,
                f"«{obj.name}» используется в {used} товар(ах). Сначала отключите значение — "
                "удаление доступно только для неиспользуемых вариантов.",
                messages.ERROR,
            )
            return
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        used = queryset.annotate(used_total=Count("product_specs", distinct=True)).filter(used_total__gt=0)
        if used.exists():
            names = ", ".join(f"«{obj.name}»" for obj in used)
            self.message_user(
                request,
                f"Не удалены используемые значения: {names}. Сначала отключите их.",
                messages.ERROR,
            )
            queryset = queryset.exclude(pk__in=used.values("pk"))
        super().delete_queryset(request, queryset)
