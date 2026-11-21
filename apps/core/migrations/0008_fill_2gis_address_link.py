"""Give environments with no 2GIS link yet the shop's address search.

The contacts page hides the map button when ``gis_url`` is empty, and some
databases (the live one included) were bootstrapped before the field existed.
This fills only blank values, so an address a manager typed by hand survives.
"""
from django.db import migrations

ADDRESS_MAP = "https://2gis.kg/bishkek/search/%D0%90%D0%B9%D0%BD%D0%B8%2031"


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(gis_url="").update(gis_url=ADDRESS_MAP)


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(gis_url=ADDRESS_MAP).update(gis_url="")


class Migration(migrations.Migration):
    dependencies = [("core", "0007_fix_2gis_link_and_screen_specs")]

    operations = [migrations.RunPython(forwards, backwards)]
