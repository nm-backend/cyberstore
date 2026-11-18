from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import InstallmentOption, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Контакты и соцсети", {"fields": ("shop_name", "tagline", "phone", "whatsapp_number", "instagram_url", "telegram_url")}),
        ("Где находимся", {"fields": ("city", "address", "address_note", "work_days", "work_hours", "gis_url")}),
        ("Каталог", {"fields": ("catalog_title", "usd_rate")}),
        ("Главная страница", {"fields": ("hero_title", "hero_subtitle", "hero_video", "hero_poster")}),
        ("Тексты страниц", {"fields": ("delivery_text", "installment_note")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # One settings row: open it straight away instead of showing a list.
        obj = SiteSettings.load()
        return redirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))


@admin.register(InstallmentOption)
class InstallmentOptionAdmin(admin.ModelAdmin):
    list_display = ("title", "badge", "order", "is_active")
    list_editable = ("order", "is_active")
