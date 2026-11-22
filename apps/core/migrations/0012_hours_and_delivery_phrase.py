"""Align the stored hours and delivery phrase with the storefront copy.

Production kept an older hand-edited variant («с 9:00 до 22:00») that the
earlier normalisation did not recognise, and its delivery paragraph still
said «по Кыргызстану». Both values describe the same schedule and promise;
this migration only rewrites the known variants.
"""
from django.db import migrations

OLD_HOURS = (
    "с 9:00 до 22:00, без выходных",
    "с 09:00 до 22:00, без выходных",
    "Ежедневно, с 9:00 до 22:00, без выходных",
    "Ежедневно, с 09:00 до 22:00, без выходных",
    "9:00-22:00, без выходных",
    "09:00-22:00, без выходных",
)
NEW_HOURS = "09:00 – 22:00, без выходных"
OLD_PHRASE = "Бесплатная доставка по Кыргызстану."
NEW_PHRASE = "Бесплатная доставка по всему Кыргызстану."


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(work_hours__in=OLD_HOURS).update(work_hours=NEW_HOURS)
    for site in SiteSettings.objects.all():
        if OLD_PHRASE in site.delivery_text:
            site.delivery_text = site.delivery_text.replace(OLD_PHRASE, NEW_PHRASE)
            site.save(update_fields=["delivery_text"])


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(work_hours=NEW_HOURS).update(work_hours=OLD_HOURS[0])
    for site in SiteSettings.objects.all():
        if NEW_PHRASE in site.delivery_text:
            site.delivery_text = site.delivery_text.replace(NEW_PHRASE, OLD_PHRASE)
            site.save(update_fields=["delivery_text"])


class Migration(migrations.Migration):
    dependencies = [("core", "0011_delivery_wording")]
    operations = [migrations.RunPython(forwards, backwards)]
