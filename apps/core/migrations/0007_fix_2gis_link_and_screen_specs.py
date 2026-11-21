"""Ship two content fixes that live in the database.

* The «2GIS» button pointed at the city root instead of the shop's address.
* Two laptops listed «Разрешение экрана: 2K», which contradicted their own
  screen specification (QHD+ 2560x1600 and QHD 2560x1440). The value now holds
  the exact pixel resolution; the «2K» facet option keeps working for filtering.

Both updates are narrow and idempotent: they only touch rows that still hold
the old value, so a database where the manager has already edited them stays
untouched.
"""
from django.db import migrations

OLD_GIS = "https://2gis.kg/bishkek"
NEW_GIS = "https://2gis.kg/bishkek/search/%D0%90%D0%B9%D0%BD%D0%B8%2031"

RESOLUTIONS = {
    "dell-alienware-m16-moshchnyy-igrovoy-noutbuk": "2560x1600",
    "hp-omen-16-moshchnyy-igrovoy-noutbuk-premium-klassa": "2560x1440",
}


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(gis_url=OLD_GIS).update(gis_url=NEW_GIS)

    ProductSpec = apps.get_model("catalog", "ProductSpec")
    for slug, resolution in RESOLUTIONS.items():
        ProductSpec.objects.filter(
            product__slug=slug, spec_type__name="Разрешение экрана", value="2K"
        ).update(value=resolution)


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(gis_url=NEW_GIS).update(gis_url=OLD_GIS)

    ProductSpec = apps.get_model("catalog", "ProductSpec")
    for slug, resolution in RESOLUTIONS.items():
        ProductSpec.objects.filter(
            product__slug=slug, spec_type__name="Разрешение экрана", value=resolution
        ).update(value="2K")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_sitesettings_catalog_title_sitesettings_usd_rate_and_more"),
        ("catalog", "0013_assign_products_to_sections_and_typography"),
    ]

    operations = [migrations.RunPython(forwards, backwards)]
