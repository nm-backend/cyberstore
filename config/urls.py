from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "CyberStore — управление сайтом"
admin.site.site_title = "CyberStore"
admin.site.index_title = "Каталог, заявки и настройки"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("catalog/", include("apps.catalog.urls")),
    path("lead/", include("apps.leads.urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.core.views.not_found"
