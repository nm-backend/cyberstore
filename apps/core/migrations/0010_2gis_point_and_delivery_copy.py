"""Data fixes for the storefront copy and the 2GIS destination.

* The «2GIS» button used to open a search page. There is no CyberStore firm
  card at Айни 31 in 2GIS, so the link now opens the building's own card
  (a fixed point on the map) instead of a search result list.
* Delivery is free across Kyrgyzstan; the stored text must not imply a
  per-city price calculation.
"""
from django.db import migrations

OLD_GIS_LINKS = (
    "https://2gis.kg/bishkek/search/%D0%90%D0%B9%D0%BD%D0%B8%2031",
    "https://2gis.kg/bishkek/search/Айни 31",
    "https://2gis.kg/bishkek",
)
NEW_GIS = "https://2gis.kg/bishkek/geo/15763234351130156"

DELIVERY_TEXT = (
    "Бесплатная доставка по всем регионам Кыргызстана.\n"
    "Самовывоз из магазина в Бишкеке — сразу после подтверждения заказа.\n"
    "Точное время доставки менеджер подтвердит в WhatsApp."
)
OLD_DELIVERY = (
    "Бесплатная доставка по Кыргызстану.\n"
    "Сроки и детали доставки уточняйте у менеджера в WhatsApp.",
)


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(gis_url__in=OLD_GIS_LINKS).update(gis_url=NEW_GIS)
    SiteSettings.objects.filter(gis_url="").update(gis_url=NEW_GIS)
    SiteSettings.objects.filter(delivery_text__in=OLD_DELIVERY).update(
        delivery_text=DELIVERY_TEXT
    )


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(gis_url=NEW_GIS).update(gis_url=OLD_GIS_LINKS[0])
    SiteSettings.objects.filter(delivery_text=DELIVERY_TEXT).update(
        delivery_text=OLD_DELIVERY[0]
    )


class Migration(migrations.Migration):
    dependencies = [("core", "0009_restore_no_days_off")]

    operations = [migrations.RunPython(forwards, backwards)]
