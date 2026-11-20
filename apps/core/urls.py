from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("installment/", views.installment, name="installment"),
    path("delivery/", views.delivery, name="delivery"),
    path("contacts/", views.contacts, name="contacts"),
    path("privacy/", views.privacy, name="privacy"),
    path("robots.txt", views.robots_txt, name="robots"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap"),
]
