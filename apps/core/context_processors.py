from apps.catalog.models import Category

from .models import SiteSettings


def site(request):
    return {
        "site": SiteSettings.load(),
        "nav_categories": Category.objects.filter(is_active=True, parent__isnull=True),
    }
