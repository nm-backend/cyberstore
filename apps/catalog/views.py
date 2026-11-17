from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Brand, Category, Product, UseCase

PAGE_SIZE = 12
SORTS = {
    "new": ("-created_at", "Сначала новые"),
    "price_asc": ("price", "Сначала дешёвые"),
    "price_desc": ("-price", "Сначала дорогие"),
}


def _int(value):
    try:
        return max(int(value), 0)
    except (TypeError, ValueError):
        return None


def product_list(request, category_slug=None):
    base = Product.objects.published()
    category = None
    subcategories = []
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        base = base.filter(Q(category=category) | Q(category__parent=category))
        subcategories = category.children.filter(is_active=True)

    # Filter options come from the products that exist in this section.
    brands = Brand.objects.filter(products__in=base).distinct()
    use_cases = UseCase.objects.filter(products__in=base).distinct()

    qs = base.with_cards()
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(title__icontains=query) | Q(brand__name__icontains=query) | Q(specs__value__icontains=query)
        ).distinct()

    selected_brands = request.GET.getlist("brand")
    if selected_brands:
        qs = qs.filter(brand__slug__in=selected_brands)

    use_case = request.GET.get("use_case", "")
    if use_case:
        qs = qs.filter(use_cases__slug=use_case)

    price_min, price_max = _int(request.GET.get("price_min")), _int(request.GET.get("price_max"))
    if price_min is not None:
        qs = qs.filter(price__gte=price_min)
    if price_max is not None:
        qs = qs.filter(price__lte=price_max)

    in_stock = request.GET.get("in_stock") == "1"
    if in_stock:
        qs = qs.exclude(status=Product.Status.OUT_OF_STOCK)

    sort = request.GET.get("sort", "new")
    if sort not in SORTS:
        sort = "new"
    qs = qs.order_by(SORTS[sort][0], "-id")

    page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)

    return render(
        request,
        "catalog/list.html",
        {
            "category": category,
            "subcategories": subcategories,
            "page": page,
            "brands": brands,
            "use_cases": use_cases,
            "selected_brands": selected_brands,
            "use_case": use_case,
            "query": query,
            "price_min": price_min,
            "price_max": price_max,
            "in_stock": in_stock,
            "sort": sort,
            "sorts": [(key, label) for key, (_, label) in SORTS.items()],
            "querystring": params.urlencode(),
            "has_filters": bool(
                query or selected_brands or use_case or in_stock
                or price_min is not None or price_max is not None
            ),
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.published().with_cards(), slug=slug)
    related = (
        Product.objects.published().with_cards()
        .filter(category=product.category).exclude(pk=product.pk)[:4]
    )
    return render(
        request,
        "catalog/detail.html",
        {
            "product": product,
            "images": list(product.images.all()),
            "specs": list(product.specs.all()),
            "use_cases": list(product.use_cases.all()),
            "related": related,
        },
    )
