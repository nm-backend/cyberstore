import re
from decimal import Decimal, InvalidOperation

from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, Q
from django.shortcuts import get_object_or_404, render

from apps.core.models import SiteSettings

from .models import Brand, Category, Product, ProductSpec, UseCase

PAGE_SIZE = 12
SORTS = {
    "new": ("-created_at", "Сначала новые"),
    "price_asc": ("price", "Сначала дешёвые"),
    "price_desc": ("-price", "Сначала дорогие"),
}
ACTIVE_PARAMS = (
    "q", "brand", "use_case", "price_min", "price_max",
    "condition", "delivery", "location", "installment", "stock",
)


def _int(value):
    try:
        return max(int(value), 0)
    except (TypeError, ValueError):
        return None


def _leading_number(text):
    match = re.search(r"\d+(?:[.,]\d+)?", text or "")
    return float(match.group().replace(",", ".")) if match else None


def _option_sort(item):
    label = item[0]
    number = _leading_number(label)
    return (number is None, number if number is not None else 0, label.lower())


def _filter_rows(category):
    """Nearest category with its own filter rows wins; subcategories inherit them."""
    node = category
    while node is not None:
        rows = list(node.filters.filter(is_active=True).select_related("spec_type"))
        if rows:
            return rows
        node = node.parent
    return []


def _selected(request):
    return {
        "brand": set(request.GET.getlist("brand")),
        "use_case": {s for s in request.GET.get("use_case", "").split(",") if s},
        "condition": set(request.GET.getlist("condition")),
        "delivery": set(request.GET.getlist("delivery")),
        "location": set(request.GET.getlist("location")),
        "installment": request.GET.get("installment") == "1",
        "stock": request.GET.get("stock") == "1",
    }


def _checkbox_group(key, title, options):
    return {"key": key, "title": title, "type": "checkbox", "options": options}


def _build_filter_groups(rows, base, selected, spec_values):
    groups = []
    for row in rows:
        if row.source == "price":
            groups.append({"key": "price", "title": row.display_title, "type": "price"})
            continue

        if row.source == "brand":
            stats = (
                base.exclude(brand=None)
                .values("brand__slug", "brand__name")
                .annotate(n=Count("id"))
                .order_by("brand__name")
            )
            options = [
                {"value": item["brand__slug"], "label": item["brand__name"], "count": item["n"],
                 "checked": item["brand__slug"] in selected["brand"]}
                for item in stats
            ]
        elif row.source == "use_case":
            stats = (
                base.filter(use_cases__isnull=False)
                .values("use_cases__slug", "use_cases__name")
                .annotate(n=Count("id", distinct=True))
                .order_by("use_cases__name")
            )
            options = [
                {"value": item["use_cases__slug"], "label": item["use_cases__name"], "count": item["n"],
                 "checked": item["use_cases__slug"] in selected["use_case"]}
                for item in stats
            ]
        elif row.source == "spec":
            products_by_value = {}
            for product_id, value, filter_value in ProductSpec.objects.filter(
                product__in=base, spec_type=row.spec_type
            ).values_list("product_id", "value", "filter_value"):
                label = (filter_value or "").strip() or (value or "").strip()
                if label:
                    products_by_value.setdefault(label, set()).add(product_id)
            key = f"spec_{row.pk}"
            selected_values = set(spec_values.get(key, []))
            options = [
                {"value": label, "label": label, "count": len(ids), "checked": label in selected_values}
                for label, ids in sorted(products_by_value.items(), key=_option_sort)
            ]
        elif row.source == "condition":
            options = [
                {"value": value, "label": label, "count": base.filter(condition=value).count(),
                 "checked": value in selected["condition"]}
                for value, label in Product.Condition.choices if value
            ]
            options = [item for item in options if item["count"]]
        elif row.source == "delivery":
            options = [
                {"value": value, "label": label, "count": base.filter(delivery=value).count(),
                 "checked": value in selected["delivery"]}
                for value, label in Product.Delivery.choices if value
            ]
            options = [item for item in options if item["count"]]
        elif row.source == "location":
            stats = (
                base.exclude(location="")
                .values("location")
                .annotate(n=Count("id"))
                .order_by("location")
            )
            options = [
                {"value": item["location"], "label": item["location"], "count": item["n"],
                 "checked": item["location"] in selected["location"]}
                for item in stats
            ]
        elif row.source == "installment":
            count = base.filter(installment_available=True).count()
            options = [{"value": "1", "label": "Есть рассрочка", "count": count,
                        "checked": selected["installment"]}] if count else []
        elif row.source == "stock":
            count = base.exclude(status=Product.Status.OUT_OF_STOCK).count()
            options = [{"value": "1", "label": "В наличии", "count": count,
                        "checked": selected["stock"]}] if count else []
        else:
            options = []

        groups.append(_checkbox_group(f"spec_{row.pk}" if row.source == "spec" else row.source,
                                      row.display_title, options))
    return groups


def _apply_filters(qs, request, rows, selected, rate):
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(title__icontains=query) | Q(brand__name__icontains=query) | Q(specs__value__icontains=query)
        ).distinct()

    if selected["brand"]:
        qs = qs.filter(brand__slug__in=selected["brand"])
    if selected["use_case"]:
        qs = qs.filter(use_cases__slug__in=selected["use_case"]).distinct()

    price_min = _int(request.GET.get("price_min"))
    price_max = _int(request.GET.get("price_max"))
    currency = request.GET.get("currency", "kgs")
    if currency == "usd" and rate:
        price_min = int(price_min * rate) if price_min is not None else None
        price_max = int(price_max * rate) if price_max is not None else None
    if price_min is not None:
        qs = qs.filter(price__gte=price_min)
    if price_max is not None:
        qs = qs.filter(price__lte=price_max)

    if selected["condition"]:
        qs = qs.filter(condition__in=selected["condition"])
    if selected["delivery"]:
        qs = qs.filter(delivery__in=selected["delivery"])
    if selected["location"]:
        qs = qs.filter(location__in=selected["location"])
    if selected["installment"]:
        qs = qs.filter(installment_available=True)
    if selected["stock"]:
        qs = qs.exclude(status=Product.Status.OUT_OF_STOCK)

    for row in rows:
        if row.source != "spec":
            continue
        values = request.GET.getlist(f"spec_{row.pk}")
        if values:
            qs = qs.filter(
                Q(specs__spec_type=row.spec_type, specs__filter_value__in=values)
                | Q(specs__spec_type=row.spec_type, specs__filter_value="", specs__value__in=values)
            ).distinct()
    return qs


def product_list(request, category_slug=None):
    site = SiteSettings.load()
    rate = site.usd_rate

    category = None
    base = Product.objects.published()
    subcategories = []
    root_categories = []
    ancestors = []

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        base = base.filter(category_id__in=category.descendant_ids())
        subcategories = list(category.children.filter(is_active=True))
        node = category.parent
        while node is not None:
            ancestors.insert(0, node)
            node = node.parent
    else:
        root_categories = list(Category.objects.filter(is_active=True, parent__isnull=True))

    spec_values = {
        key: request.GET.getlist(key)
        for key in request.GET.keys() if key.startswith("spec_")
    }
    selected = _selected(request)
    rows = _filter_rows(category) if category else []
    groups = _build_filter_groups(rows, base, selected, spec_values)

    query = request.GET.get("q", "").strip()
    has_filters = bool(query) or any(request.GET.get(key) for key in ACTIVE_PARAMS) or any(
        spec_values.values()
    )

    currency = request.GET.get("currency", "kgs")
    if currency == "usd" and not rate:
        currency = "kgs"

    if category is None:
        show_tiles = not has_filters
        show_products = has_filters
    else:
        show_tiles = (
            category.display_mode in (Category.DisplayMode.TILES, Category.DisplayMode.BOTH)
            and not has_filters
        )
        show_products = (
            category.display_mode in (Category.DisplayMode.PRODUCTS, Category.DisplayMode.BOTH)
            or has_filters
        )

    qs = _apply_filters(base.with_cards(), request, rows, selected, rate)
    sort = request.GET.get("sort", "new")
    if sort not in SORTS:
        sort = "new"
    qs = qs.order_by(SORTS[sort][0], "-id")

    page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)

    quick_links = []
    if category and show_products and not has_filters:
        quick_links = list(category.quick_links.filter(is_active=True).prefetch_related("use_cases"))

    price_bounds = base.aggregate(low=Min("price"), high=Max("price"))
    price_low, price_high = price_bounds["low"], price_bounds["high"]
    if currency == "usd" and rate:
        price_low = int(price_low / rate) if price_low else None
        price_high = int(price_high / rate) if price_high else None

    return render(
        request,
        "catalog/list.html",
        {
            "category": category,
            "ancestors": ancestors,
            "subcategories": subcategories,
            "root_categories": root_categories,
            "quick_links": quick_links,
            "page": page,
            "filter_groups": groups,
            "selectedspec_values": spec_values,
            "query": query,
            "price_min": _int(request.GET.get("price_min")),
            "price_max": _int(request.GET.get("price_max")),
            "price_low": price_low,
            "price_high": price_high,
            "currency": currency,
            "selected_use_case": ",".join(sorted(selected["use_case"])),
            "has_use_case_group": any(group["key"] == "use_case" for group in groups),
            "usd_rate": rate,
            "sort": sort,
            "sorts": [(key, label) for key, (_, label) in SORTS.items()],
            "querystring": params.urlencode(),
            "has_filters": has_filters,
            "show_tiles": show_tiles,
            "show_products": show_products,
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
