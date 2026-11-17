from django.db.models import Count, Q
from django.shortcuts import render

from apps.catalog.models import Category, Product, UseCase

from .models import InstallmentOption


def home(request):
    products = Product.objects.published().with_cards()
    featured = list(products.filter(is_featured=True)[:8])
    if not featured:
        featured = list(products[:8])
    categories = Category.objects.filter(is_active=True, parent__isnull=True).annotate(
        total=Count(
            "products",
            filter=Q(products__is_published=True),
            distinct=True,
        )
    )
    return render(
        request,
        "core/home.html",
        {
            "featured": featured,
            "total": products.count(),
            "categories": categories,
            "use_cases": UseCase.objects.all(),
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


def not_found(request, exception):
    return render(request, "404.html", status=404)
