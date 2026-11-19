"""Закрепляет четыре раздела каталога и их порядок.

1. Настольные ПК
2. Комплектующие для ПК
3. Мониторы
4. Ноутбуки

Старый раздел «Готовые ПК» (slug ``pc``) сливается с «Настольными ПК»:
товары и подразделы переносятся, сам раздел скрывается, чтобы в меню,
на главной и в подвале осталось ровно четыре раздела.
"""

from django.db import migrations

SECTIONS = [
    ("pcs", "Настольные ПК", 1),
    ("components", "Комплектующие для ПК", 2),
    ("monitors", "Мониторы", 3),
    ("laptops", "Ноутбуки", 4),
]

# Прежние названия корневых slug → раздел, который их заменил.
LEGACY_ROOTS = {
    "pc": "pcs",
    "desktops": "pcs",
    "desktop-pc": "pcs",
    "computers": "pcs",
    "laptops-and-accessories": "laptops",
}


def configure_sections(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Product = apps.get_model("catalog", "Product")

    sections = {}
    for slug, name, order in SECTIONS:
        category = Category.objects.filter(slug=slug).first()
        if category is None:
            category = Category.objects.create(
                slug=slug,
                name=name,
                order=order,
                parent=None,
                display_mode="both",
                is_active=True,
            )
        else:
            category.name = name
            category.order = order
            category.parent = None
            category.is_active = True
            category.save(update_fields=["name", "order", "parent", "is_active"])
        sections[slug] = category

    for legacy_slug, target_slug in LEGACY_ROOTS.items():
        legacy = Category.objects.filter(slug=legacy_slug, parent__isnull=True).first()
        target = sections[target_slug]
        if legacy is None or legacy.pk == target.pk:
            continue
        Category.objects.filter(parent=legacy).update(parent=target)
        Product.objects.filter(category=legacy).update(category=target)
        Category.objects.filter(pk=legacy.pk).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_filter_dictionary_polish"),
    ]

    operations = [
        migrations.RunPython(configure_sections, migrations.RunPython.noop),
    ]
