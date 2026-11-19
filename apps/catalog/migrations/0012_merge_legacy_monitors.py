"""Убирает старый дубль раздела «Мониторы» (slug ``monitory``).

Миграция 0008 создала новый корневой раздел ``monitors``, но в базе прода
оставался прежний ``monitory`` с тем же названием. В меню, на главной и в
подвале «Мониторы» выводились дважды. Переносим товары и подразделы в новый
раздел, старый скрываем.
"""

from django.db import migrations

LEGACY_ROOTS = {
    "monitory": "monitors",
}


def merge_legacy_roots(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Product = apps.get_model("catalog", "Product")

    for legacy_slug, target_slug in LEGACY_ROOTS.items():
        target = Category.objects.filter(slug=target_slug, parent__isnull=True).first()
        if target is None:
            continue
        legacy = (
            Category.objects.filter(slug=legacy_slug, parent__isnull=True)
            .exclude(pk=target.pk)
            .first()
        )
        if legacy is None:
            continue
        Category.objects.filter(parent=legacy).update(parent=target)
        Product.objects.filter(category=legacy).update(category=target)
        Category.objects.filter(pk=legacy.pk).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0011_alter_category_icon_alter_usecase_icon"),
    ]

    operations = [
        migrations.RunPython(merge_legacy_roots, migrations.RunPython.noop),
    ]
