from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from apps.catalog.models import Product, UseCase
from apps.catalog.tree import CategoryTree

from .models import InstallmentOption


def home(request):
    products = Product.objects.published().with_cards()
    featured = list(products.filter(is_featured=True)[:8])
    if not featured:
        featured = list(products[:8])
    # Counts include nested sections, and empty roots are not advertised.
    tree = CategoryTree()
    categories = [root for root in tree.roots if tree.totals.get(root.pk, 0)]
    # The mobile section strip shows how many goods each section has.
    for root in categories:
        root.product_count = tree.totals.get(root.pk, 0)
    return render(
        request,
        "core/home.html",
        {
            "featured": featured,
            "total": products.count(),
            "categories": categories,
            "use_cases": UseCase.objects.all(),
            "installment_options": InstallmentOption.objects.filter(is_active=True),
        },
    )


def installment(request):
    return render(
        request,
        "core/installment.html",
        {"options": InstallmentOption.objects.filter(is_active=True)},
    )


def delivery(request):
    return render(request, "core/delivery.html")


def contacts(request):
    return render(request, "core/contacts.html")


def privacy(request):
    return render(request, "core/privacy.html")


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Disallow: /{settings.ADMIN_URL}",
        "Disallow: /api/",
        "Disallow: /lead/",
        "",
        f"Sitemap: {request.build_absolute_uri(reverse('core:sitemap'))}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    tree = CategoryTree()
    paths = [
        reverse("core:home"),
        reverse("catalog:list"),
        reverse("catalog:categories"),
        reverse("core:installment"),
        reverse("core:delivery"),
        reverse("core:contacts"),
        reverse("core:privacy"),
    ]
    paths += [
        item.get_absolute_url()
        for item in tree.categories
        if tree.totals.get(item.pk, 0)
    ]
    products = Product.objects.published().only("slug", "updated_at").order_by("pk")
    entries = [(request.build_absolute_uri(path), "") for path in paths]
    entries += [
        (request.build_absolute_uri(product.get_absolute_url()), product.updated_at.date().isoformat())
        for product in products
    ]

    rows = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod in entries:
        rows.append("  <url>")
        rows.append(f"    <loc>{escape(url)}</loc>")
        if lastmod:
            rows.append(f"    <lastmod>{lastmod}</lastmod>")
        rows.append("  </url>")
    rows.append("</urlset>")
    return HttpResponse("\n".join(rows), content_type="application/xml; charset=utf-8")


def not_found(request, exception):
    return render(request, "404.html", status=404)
