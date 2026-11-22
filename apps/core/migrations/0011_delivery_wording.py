"""Normalise the delivery wording to the store's single promise."""
from django.db import migrations

OLD = "по всем регионам Кыргызстана"
NEW = "по всему Кыргызстану"
GIS_POINT = "https://2gis.kg/bishkek/geo/15763234351130156"


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    for site in SiteSettings.objects.all():
        fields = []
        if OLD in site.delivery_text:
            site.delivery_text = site.delivery_text.replace(OLD, NEW)
            fields.append("delivery_text")
        if site.gis_url and "2gis" in site.gis_url and "/search/" in site.gis_url:
            site.gis_url = GIS_POINT
            fields.append("gis_url")
        if fields:
            site.save(update_fields=fields)


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    for site in SiteSettings.objects.all():
        if NEW in site.delivery_text:
            site.delivery_text = site.delivery_text.replace(NEW, OLD)
            site.save(update_fields=["delivery_text"])


class Migration(migrations.Migration):
    dependencies = [("core", "0010_2gis_point_and_delivery_copy")]
    operations = [migrations.RunPython(forwards, backwards)]
