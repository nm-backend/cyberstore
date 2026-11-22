"""One canonical hours string on every database.

The production row stored the same schedule with the «Ежедневно, с …»
prefix, which the exact-match migration could not see. Only rows that
clearly describe 9:00–22:00 every day are rewritten.
"""
from django.db import migrations

NEW_HOURS = "09:00 – 22:00, без выходных"


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    for site in SiteSettings.objects.all():
        hours = (site.work_hours or "").strip()
        lowered = hours.lower().replace("ё", "е")
        if "9:00" in lowered and "22:00" in lowered and "без выходных" in lowered:
            if hours != NEW_HOURS:
                site.work_hours = NEW_HOURS
                site.save(update_fields=["work_hours"])


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("core", "0012_hours_and_delivery_phrase")]
    operations = [migrations.RunPython(forwards, backwards)]
