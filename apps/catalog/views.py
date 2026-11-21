import re
from collections import defaultdict

from django.core.paginator import Paginator
from django.db.models import Count, F, Max, Min, Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.core.models import SiteSettings

from .models import Brand, Category, CategoryFilter, Product, ProductSpec, SpecOption, UseCase
from .tree import CategoryTree

PAGE_SIZE = 12

# "По умолчанию" keeps the featured items on top; the other modes really reorder.
SORTS = {
    "default": ("По умолчанию", ("-is_featured", "-created_at", "-id")),
    "new": ("Сначала новые", ("-created_at", "-id")),
    "price_asc": ("Сначала дешевле", (F("price").asc(nulls_last=True), "-id")),
    "price_desc": ("Сначала дороже", (F("price").desc(nulls_last=True), "-id")),
}

FILTER_PARAMS = (
    "q", "brand", "use_case", "price_min", "price_max",
    "condition", "delivery", "installment", "stock",
)


def _int(value):
    try:
        return max(int(value), 0)
    except (TypeError, ValueError):
        return None


def _leading_number(text):
    match = re.search(r"\d+(?:[.,]\d+)?", text or "")
    return float(match.group().replace(",", ".")) if match else None


def _filter_rows(category):
    """Nearest category with its own filter rows wins; subcategories inherit them."""
    node = category
    while node is not None:
        rows = list(node.filters.filter(is_active=True).select_related("spec_type"))
        if rows:
            return rows
        node = node.parent
    return []


def _global_filter_rows():
    """Useful filters for a search that spans every section."""
    anchor = Category.objects.filter(is_active=True, parent__isnull=True).first()
    if not anchor:
        return []
    return [
        CategoryFilter(category=anchor, source="price", title="Цена"),
        CategoryFilter(category=anchor, source="brand", title="Бренд"),
        CategoryFilter(category=anchor, source="use_case", title="Назначение"),
        CategoryFilter(category=anchor, source="installment", title="Рассрочка"),
        CategoryFilter(category=anchor, source="condition", title="Состояние"),
    ]


def _selected(request):
    use_cases = set()
    for chunk in request.GET.getlist("use_case"):
        use_cases.update(slug for slug in chunk.split(",") if slug)
    return {
        "brand": {value for value in request.GET.getlist("brand") if value},
        "use_case": use_cases,
        "condition": {value for value in request.GET.getlist("condition") if value},
        "delivery": {value for value in request.GET.getlist("delivery") if value},
        "installment": {value for value in request.GET.getlist("installment") if value in {"0", "1"}},
        "stock": request.GET.get("stock") == "1",
    }


def _spec_values(request):
    return {
        key: [value for value in request.GET.getlist(key) if value]
        for key in request.GET.keys() if key.startswith("spec_")
    }


def _apply_filters(qs, request, rows, selected, rate, skip=None):
    """Applies every active filter except the group named by ``skip``.

    Skipping one group is how facet counters stay honest: the numbers next to
    a filter's options are computed with all *other* groups applied, so they
    always match what the catalog will show after clicking them.
    """
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(brand__name__icontains=query)
            | Q(specs__value__icontains=query)
            | Q(specs__filter_value__icontains=query)
            | Q(specs__option__name__icontains=query)
        ).distinct()

    if skip != "brand" and selected["brand"]:
        qs = qs.filter(brand__slug__in=selected["brand"])
    if skip != "use_case" and selected["use_case"]:
        qs = qs.filter(use_cases__slug__in=selected["use_case"]).distinct()

    if skip != "price":
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

    if skip != "condition" and selected["condition"]:
        qs = qs.filter(condition__in=selected["condition"])
    if skip != "delivery" and selected["delivery"]:
        qs = qs.filter(delivery__in=selected["delivery"])
    # «Местоположение» is gone from the storefront filters: the shop is one city,
    # so every good already comes from the same place.
    if skip != "installment":
        if selected["installment"] == {"1"}:
            qs = qs.filter(installment_available=True)
        elif selected["installment"] == {"0"}:
            qs = qs.filter(installment_available=False)
    if skip != "stock" and selected["stock"]:
        qs = qs.exclude(status=Product.Status.OUT_OF_STOCK)

    for row in rows:
        if row.source != "spec" or not row.spec_type_id:
            continue
        key = f"spec_{row.pk}"
        if skip == key:
            continue
        values = [value for value in request.GET.getlist(key) if value]
        if not values:
            continue
        matching = ProductSpec.objects.filter(spec_type_id=row.spec_type_id).filter(
            Q(option__name__in=values)
            | Q(option__isnull=True, filter_value__in=values)
            | Q(option__isnull=True, filter_value="", value__in=values)
        ).values("product_id")
        qs = qs.filter(pk__in=matching).distinct()
    return qs


def _spec_options(spec_type, qs, selected_values):
    """Options come from the admin-managed dictionary, counts from real products.

    Every active value is listed even when it currently has no products, so a
    processor/GPU/colour added in the admin panel shows up in the filter
    immediately. Legacy ``filter_value`` strings that have no dictionary row
    stay filterable too.
    """
    active = list(SpecOption.objects.filter(spec_type=spec_type, is_active=True))
    active_by_pk = {option.pk: option.name for option in active}
    active_by_name = {option.name: option for option in active}
    inactive_names = set(
        SpecOption.objects.filter(spec_type=spec_type, is_active=False).values_list("name", flat=True)
    )
    counts = defaultdict(set)
    rows = ProductSpec.objects.filter(
        product_id__in=qs.values("pk"), spec_type=spec_type
    ).values_list("product_id", "option_id", "filter_value", "value")
    for product_id, option_id, filter_value, value in rows:
        if option_id:
            label = active_by_pk.get(option_id)
            if not label:
                continue  # disabled option: products keep it, the filter hides it
        else:
            label = (filter_value or "").strip() or (value or "").strip()
            if not label:
                continue
        counts[label].add(product_id)

    labels = set(active_by_name)
    for label in counts:
        if label not in inactive_names:
            labels.add(label)
    for label in selected_values:
        if label not in inactive_names:
            labels.add(label)

    def order_key(label):
        option = active_by_name.get(label)
        if option:
            return (0, option.order, option.name.lower())
        number = _leading_number(label)
        return (1, number if number is not None else 0, label.lower())

    return [
        {"value": label, "label": label, "count": len(counts.get(label, ())), "checked": label in selected_values}
        for label in sorted(labels, key=order_key)
    ]


def _price_bounds(qs, currency, rate):
    bounds = qs.aggregate(low=Min("price"), high=Max("price"))
    low, high = bounds["low"], bounds["high"]
    if currency == "usd" and rate:
        low = int(low / rate) if low else None
        high = int(high / rate) if high else None
    return low, high


def _build_filter_groups(rows, request, base, selected, rate, currency):
    groups = []
    spec_selection = _spec_values(request)
    for row in rows:
        if row.source == "location":
            continue  # removed from the storefront, admin rows are ignored
        key = f"spec_{row.pk}" if row.source == "spec" else row.source
        facet_base = _apply_filters(base, request, rows, selected, rate, skip=key)

        if row.source == "price":
            low, high = _price_bounds(facet_base, currency, rate)
            # Configured price filter stays visible even in an empty section.
            groups.append({
                "key": "price", "title": row.display_title, "type": "price",
                "low": low, "high": high, "open": True,
            })
            continue

        options = []
        if row.source == "brand":
            stats = (
                facet_base.exclude(brand=None)
                .filter(brand__is_active=True)
                .values("brand__slug", "brand__name")
                .annotate(n=Count("id", distinct=True))
                .order_by("brand__name")
            )
            options = [
                {
                    "value": item["brand__slug"], "label": item["brand__name"],
                    "count": item["n"], "checked": item["brand__slug"] in selected["brand"],
                }
                for item in stats
            ]
            if not options:
                # No goods yet: offer brands assigned to the section, then brands
                # sold anywhere on the site, so the configured filter is not lost.
                fallback = row.category.brands.filter(is_active=True)
                if not fallback.exists():
                    fallback = Brand.objects.filter(
                        is_active=True, products__is_published=True
                    ).distinct()
                options = [
                    {
                        "value": brand.slug, "label": brand.name, "count": 0,
                        "checked": brand.slug in selected["brand"],
                    }
                    for brand in fallback.order_by("name")
                ]
        elif row.source == "use_case":
            stats = (
                facet_base.filter(use_cases__isnull=False)
                .values("use_cases__slug")
                .annotate(n=Count("id", distinct=True))
            )
            counts = {item["use_cases__slug"]: item["n"] for item in stats}
            # The block is configured in the admin, so every destination is listed;
            # a zero means «пока нет товаров», not «фильтр сломан».
            options = [
                {
                    "value": use_case.slug, "label": use_case.name,
                    "count": counts.get(use_case.slug, 0), "checked": use_case.slug in selected["use_case"],
                }
                for use_case in UseCase.objects.all()
            ]
        elif row.source == "spec":
            if not row.spec_type_id:
                continue
            options = _spec_options(
                row.spec_type, facet_base, spec_selection.get(f"spec_{row.pk}", [])
            )
        elif row.source == "condition":
            for value, label in Product.Condition.choices:
                if not value:
                    continue
                options.append({
                    "value": value, "label": label,
                    "count": facet_base.filter(condition=value).count(),
                    "checked": value in selected["condition"],
                })
        elif row.source == "delivery":
            for value, label in Product.Delivery.choices:
                if not value:
                    continue
                options.append({
                    "value": value, "label": label,
                    "count": facet_base.filter(delivery=value).count(),
                    "checked": value in selected["delivery"],
                })
        elif row.source == "installment":
            yes = facet_base.filter(installment_available=True).count()
            no = facet_base.filter(installment_available=False).count()
            if yes or no:
                options = [
                    {
                        "value": "1", "label": "В рассрочку", "count": yes,
                        "checked": "1" in selected["installment"],
                    },
                    {
                        "value": "0", "label": "Без рассрочки", "count": no,
                        "checked": "0" in selected["installment"],
                    },
                ]
        elif row.source == "stock":
            count = facet_base.exclude(status=Product.Status.OUT_OF_STOCK).count()
            if count:
                options = [{
                    "value": "1", "label": "В наличии", "count": count,
                    "checked": selected["stock"],
                }]

        if not options:
            continue
        groups.append({
            "key": key, "title": row.display_title, "type": "checkbox",
            "options": options, "searchable": len(options) > 6,
            # Long lists stay folded: the group title works as a button that
            # opens the choices, so the sidebar is a short list of buttons.
            "collapsible": len(options) > 4,
            "active_count": sum(1 for option in options if option["checked"]),
            "open": len(options) <= 4 or any(option["checked"] for option in options),
        })
    return groups


def _url_without(request, key, value=None):
    params = request.GET.copy()
    params.pop("page", None)
    if key:
        if key == "use_case":
            values = [slug for chunk in params.getlist(key) for slug in chunk.split(",") if slug]
            values = [slug for slug in values if slug != value]
            if values:
                params.setlist(key, values)
            else:
                params.pop(key, None)
        elif value is None:
            params.pop(key, None)
        else:
            values = [item for item in params.getlist(key) if item != value]
            if values:
                params.setlist(key, values)
            else:
                params.pop(key, None)
    query = params.urlencode()
    return f"{request.path}?{query}" if query else request.path


def _active_filters(request, groups, category, currency):
    chips = []
    for group in groups:
        for option in group.get("options", []):
            if option["checked"]:
                chips.append({
                    "label": f"{group['title']}: {option['label']}",
                    "url": _url_without(request, group["key"], option["value"]),
                })
    money = "USD" if currency == "usd" else "сом"
    if request.GET.get("price_min"):
        chips.append({"label": f"Цена от {request.GET['price_min']} {money}", "url": _url_without(request, "price_min")})
    if request.GET.get("price_max"):
        chips.append({"label": f"Цена до {request.GET['price_max']} {money}", "url": _url_without(request, "price_max")})
    if request.GET.get("q", "").strip():
        chips.append({"label": f"Поиск: {request.GET['q'].strip()}", "url": _url_without(request, "q")})
    # The category chip is only useful when it narrows a broader page, not when
    # the visitor is already inside that section.
    if category and request.path != category.get_absolute_url():
        params = request.GET.copy()
        params.pop("category", None)
        params.pop("page", None)
        query = params.urlencode()
        base = reverse("catalog:list")
        chips.append({
            "label": f"Категория: {category.name}",
            "url": f"{base}?{query}" if query else base,
        })
    return chips


def _tiles(categories, tree, current=None):
    return [
        {
            "category": category,
            "url": category.get_absolute_url(),
            "name": category.name,
            "description": category.description,
            "icon": category.icon,
            "image": category.image,
            "count": tree.totals.get(category.pk, 0),
            "is_current": bool(current and current.pk == category.pk),
        }
        for category in categories
    ]


def product_list(request, category_slug=None):
    site = SiteSettings.load()
    rate = site.usd_rate
    tree = CategoryTree()

    category = None
    if "category" in request.GET:
        chosen = request.GET.get("category", "").strip()
        if chosen:
            category = get_object_or_404(Category, slug=chosen, is_active=True)
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)

    base = Product.objects.published()
    ancestors = []
    if category:
        base = base.filter(category_id__in=category.descendant_ids())
        node = category.parent
        while node is not None:
            ancestors.insert(0, node)
            node = node.parent

    current_path = request.path
    root_tiles = (
        [tile for tile in _tiles(tree.roots, tree) if tile["count"]]
        if category is None else []
    )
    subcategory_tiles = []
    if category and tree.children[category.pk]:
        subcategory_tiles = [{
            "category": category,
            "url": current_path,
            "name": "Все товары",
            "description": "Весь раздел без выбора подкатегории",
            "icon": category.icon,
            "image": category.image,
            "count": tree.totals.get(category.pk, 0),
            "is_current": True,
            "is_all": True,
        }] + [
            tile for tile in _tiles(tree.children[category.pk], tree) if tile["count"]
        ]

    currency = request.GET.get("currency", "kgs")
    if currency == "usd" and not rate:
        currency = "kgs"

    selected = _selected(request)
    if category:
        rows = _filter_rows(category)
    elif query_for_filters := request.GET.get("q", "").strip():
        rows = _global_filter_rows() if query_for_filters else []
    else:
        rows = []
    groups = _build_filter_groups(rows, request, base, selected, rate, currency) if rows else []

    query = request.GET.get("q", "").strip()
    spec_selection = _spec_values(request)
    has_filters = (
        bool(query)
        or any(request.GET.get(key) for key in FILTER_PARAMS if key != "q")
        or any(spec_selection.values())
    )

    if category is None:
        # /catalog/ is both the section index and the «Все товары» page:
        # keep the section tiles and show every published product below them.
        show_tiles = not has_filters
        show_products = True
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
    sort = request.GET.get("sort", "default")
    if sort not in SORTS:
        sort = "default"
    qs = qs.order_by(*SORTS[sort][1])

    page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)

    quick_links = []
    if category and show_products and not has_filters:
        quick_links = list(category.quick_links.filter(is_active=True).prefetch_related("use_cases"))

    # «Под ваши задачи» goes above the goods: the visitor narrows the section
    # before scrolling through it. Only the tasks this section actually has.
    use_case_tiles = []
    if category and not has_filters:
        stats = (
            base.filter(use_cases__isnull=False)
            .values("use_cases__slug")
            .annotate(n=Count("id", distinct=True))
        )
        counts = {item["use_cases__slug"]: item["n"] for item in stats}
        if counts:
            use_case_tiles = [
                {"case": case, "count": counts[case.slug], "selected": case.slug in selected["use_case"]}
                for case in UseCase.objects.filter(slug__in=counts)
            ]

    price_low, price_high = _price_bounds(
        _apply_filters(base, request, rows, selected, rate, skip="price"), currency, rate
    )

    brand_tiles = []
    if category and category.show_brand_tiles and show_products and not has_filters:
        counts = (
            base.exclude(brand=None)
            .filter(brand__is_active=True)
            .values("brand_id")
            .annotate(n=Count("id", distinct=True))
            .order_by("-n")
        )
        brands = {brand.pk: brand for brand in Brand.objects.filter(pk__in=[item["brand_id"] for item in counts])}
        brand_tiles = [
            {"brand": brands[item["brand_id"]], "count": item["n"]}
            for item in counts if item["brand_id"] in brands
        ]
        brand_tiles.sort(key=lambda item: (-item["count"], item["brand"].name.lower()))

    category_options = []
    for item, depth in tree.flat:
        if not tree.totals.get(item.pk, 0):
            continue
        category_options.append({
            "slug": item.slug,
            "name": f"{'— ' * depth}{item.name}",
            "category": item,
            "count": tree.totals.get(item.pk, 0),
            "selected": bool(category and category.pk == item.pk),
        })

    return render(
        request,
        "catalog/list.html",
        {
            "category": category,
            "ancestors": ancestors,
            "root_tiles": root_tiles,
            "subcategory_tiles": subcategory_tiles,
            "brand_tiles": brand_tiles,
            "quick_links": quick_links,
            "use_case_tiles": use_case_tiles,
            "page": page,
            "filter_groups": groups,
            "category_options": category_options,
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
            "sorts": [(key, label) for key, (label, _) in SORTS.items()],
            "querystring": params.urlencode(),
            "has_filters": has_filters,
            "show_tiles": show_tiles,
            "show_products": show_products,
            "result_count": page.paginator.count,
            "active_filters": _active_filters(request, groups, category, currency),
        },
    )


def category_index(request):
    tree = CategoryTree()
    query = request.GET.get("q", "").strip()
    needle = query.lower()
    groups = []

    for root in tree.roots:
        root_matches = not needle or needle in root.name.lower()
        items = []

        def collect(category, depth):
            matches = not needle or root_matches or needle in category.name.lower()
            count = tree.totals.get(category.pk, 0)
            if matches and count:
                items.append({"category": category, "depth": depth, "count": count})
            for child in tree.children[category.pk]:
                collect(child, depth + 1)

        collect(root, 0)
        if items:
            groups.append({
                "root": root,
                "count": tree.totals.get(root.pk, 0),
                "items": items,
            })

    # Empty sections stay reachable by direct URL for the manager, but they are
    # not advertised in navigation, search or the category index.
    groups = [
        group for group in groups
        if group["count"] or any(item["count"] for item in group["items"])
    ]

    return render(
        request,
        "catalog/categories.html",
        {"groups": groups, "query": query},
    )


def _visible_specs(specs):
    """Drop a spec row whose value is already spelled out inside a richer row.

    Products carry both a detailed row («Экран: 16″ QHD+ (2560x1600) 165Hz IPS»)
    and a short facet row («Разрешение экрана: 2560x1600») used by the catalog
    filters. The short one is redundant on the product page, so it is hidden
    there while staying available for filtering.
    """
    # A two-row table (e.g. a CPU: model + core count) reads better complete.
    if len(specs) <= 3:
        return specs
    values = [(spec.value or "").strip().lower() for spec in specs]
    visible = []
    for index, spec in enumerate(specs):
        value = values[index]
        redundant = bool(value) and any(
            other != index and values[other] and value != values[other] and value in values[other]
            for other in range(len(values))
        )
        if not redundant:
            visible.append(spec)
    return visible


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.published().with_cards(), slug=slug)
    related = (
        Product.objects.published().with_cards()
        .filter(category=product.category).exclude(pk=product.pk)[:4]
    )
    lead_state = request.session.pop("lead_form_state", None)
    return render(
        request,
        "catalog/detail.html",
        {
            "product": product,
            "images": list(product.images.all()),
            "specs": _visible_specs(list(product.specs.select_related("spec_type"))),
            "use_cases": list(product.use_cases.all()),
            "related": related,
            "lead_state": lead_state,
        },
    )
