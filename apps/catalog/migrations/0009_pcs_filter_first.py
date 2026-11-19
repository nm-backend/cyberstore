"""«Настольные ПК» открываются сразу фильтром и товарами.

Плитки подразделов и брендов уводили панель фильтров вниз, поэтому раздел
переключается в режим «Товары с фильтром»: слева полный набор фильтров,
справа список объявлений. Подразделы остаются доступны в меню каталога.
"""

from django.db import migrations


def filter_first(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Category.objects.filter(slug="pcs").update(
        display_mode="products",
        show_brand_tiles=False,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0008_catalog_four_sections"),
    ]

    operations = [
        migrations.RunPython(filter_first, migrations.RunPython.noop),
    ]
