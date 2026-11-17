from django.db import migrations, models

HERO_TITLE = "Мощные игровые ПК и ноутбуки в Бишкеке"
HERO_SUBTITLE = (
    "Сборки любой сложности на RTX 40-й серии, проверенные ноутбуки с гарантией, "
    "выгодная рассрочка с банком и без банка, бесплатная доставка по всему Кыргызстану."
)


def apply_copy(apps, schema_editor):
    """Put the real marketing copy into the settings row so the hero stays editable in admin."""
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(pk=1).update(
        hero_title=HERO_TITLE, hero_subtitle=HERO_SUBTITLE
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_sitesettings_address_note_sitesettings_telegram_url_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="hero_title",
            field=models.CharField(
                default=HERO_TITLE, max_length=120, verbose_name="Заголовок на главной"
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="hero_subtitle",
            field=models.CharField(
                default=HERO_SUBTITLE,
                help_text="Показывается под главным заголовком на первом экране.",
                max_length=250,
                verbose_name="Подзаголовок на главной",
            ),
        ),
        migrations.RunPython(apply_copy, migrations.RunPython.noop),
    ]
