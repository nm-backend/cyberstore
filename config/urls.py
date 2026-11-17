from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.catalog.api import BrandViewSet, CategoryViewSet, ProductViewSet, UseCaseViewSet
from apps.leads.api import LeadViewSet
from config.api_docs import redoc_view, swagger_view

admin.site.site_header = "CyberStore — управление сайтом"
admin.site.site_title = "CyberStore"
admin.site.index_title = "Каталог, заявки и настройки"

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("brands", BrandViewSet)
router.register("use-cases", UseCaseViewSet)
router.register("products", ProductViewSet)
router.register("leads", LeadViewSet, basename="lead")

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # API
    path("api/", include(router.urls)),
    path("api/swagger/", swagger_view, name="swagger-ui"),
    path("api/redoc/", redoc_view, name="redoc"),
    # Site
    path("catalog/", include("apps.catalog.urls")),
    path("lead/", include("apps.leads.urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.core.views.not_found"
