"""Вернуть «без выходных» в часы работы.

Магазин работает каждый день, и это важно покупателю. Значение по умолчанию
однажды потеряло эту приписку, а вместе с ней — и уже сохранённые строки.
Миграция меняет только те записи, где стоят стандартные часы без уточнения,
поэтому расписание, введённое вручную, остаётся нетронутым.
"""
from django.db import migrations, models

OLD_HOURS = (
    "09:00 – 22:00",
    "9:00 – 22:00",
    "09:00-22:00",
    "Ежедневно с 9:00 до 22:00",
    "Ежедневно с 09:00 до 22:00",
)
NEW_HOURS = "09:00 – 22:00, без выходных"


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(work_hours__in=OLD_HOURS).update(work_hours=NEW_HOURS)


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(work_hours=NEW_HOURS).update(work_hours="09:00 – 22:00")


class Migration(migrations.Migration):
    dependencies = [("core", "0008_fill_2gis_address_link")]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="work_hours",
            field=models.CharField(
                default=NEW_HOURS, max_length=120, verbose_name="Часы работы"
            ),
        ),
        migrations.RunPython(forwards, backwards),
    ]
