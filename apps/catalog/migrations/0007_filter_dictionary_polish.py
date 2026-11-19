from django.db import migrations


def polish(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    CategoryFilter = apps.get_model("catalog", "CategoryFilter")
    ProductSpec = apps.get_model("catalog", "ProductSpec")
    SpecOption = apps.get_model("catalog", "SpecOption")
    SpecType = apps.get_model("catalog", "SpecType")

    def option(spec_type, name, order):
        value, _ = SpecOption.objects.get_or_create(
            spec_type=spec_type, name=name, defaults={"order": order, "is_active": True}
        )
        return value

    def link(spec_type, name, option_obj):
        ProductSpec.objects.filter(
            spec_type=spec_type, option__isnull=True, filter_value=name
        ).update(option=option_obj, filter_value=name)

    # GPU models really present in the shop become manageable values.
    gpu_models = SpecType.objects.filter(name="Видеокарта").first()
    if gpu_models:
        for order, name in enumerate(
            ["RTX 4070", "RTX 4060", "RTX 4070 Ti", "RTX 3070 Ti", "Встроенная"], start=1
        ):
            link(gpu_models, name, option(gpu_models, name, order))

    # RAM volumes: the listed capacities stay visible even before a product uses them.
    ram = SpecType.objects.filter(name="Оперативная память").first()
    if ram:
        for order, name in enumerate(["4 ГБ", "8 ГБ", "16 ГБ", "32 ГБ", "64 ГБ", "128 ГБ"], start=1):
            ram_option = option(ram, name, order)
            if name in {"8 ГБ", "16 ГБ", "32 ГБ"}:
                link(ram, name, ram_option)

    # «Windows 11» is the Windows family for filtering; the full version stays in `value`.
    os_type = SpecType.objects.filter(name="Операционная система").first()
    if os_type:
        windows = option(os_type, "Windows", 1)
        ProductSpec.objects.filter(
            spec_type=os_type, filter_value__istartswith="Windows"
        ).update(option=windows, filter_value="Windows")

    # A CPU's own «Процессор» row should filter by its family, not by a core count.
    cpu_type = SpecType.objects.filter(name="Процессор").first()
    if cpu_type:
        ryzen7 = SpecOption.objects.filter(spec_type=cpu_type, name="AMD Ryzen 7").first()
        if ryzen7:
            ProductSpec.objects.filter(
                spec_type=cpu_type, product__category__slug="cpu", filter_value="8 ядер"
            ).update(option=ryzen7, filter_value="AMD Ryzen 7")

    # Vendor filter next to the model filter on laptops and ready-made PCs.
    vendor = SpecType.objects.filter(name="Производитель видеокарты").first()
    if vendor:
        for slug in ("laptops", "pcs"):
            category = Category.objects.filter(slug=slug).first()
            if not category:
                continue
            if CategoryFilter.objects.filter(category=category, spec_type=vendor).exists():
                continue
            for row in CategoryFilter.objects.filter(category=category, order__gte=7).order_by("-order"):
                row.order += 1
                row.save(update_fields=["order"])
            CategoryFilter.objects.create(
                category=category, source="spec", spec_type=vendor, order=7, is_active=True
            )


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0006_catalog_structure"),
    ]

    operations = [
        migrations.RunPython(polish, migrations.RunPython.noop),
    ]
