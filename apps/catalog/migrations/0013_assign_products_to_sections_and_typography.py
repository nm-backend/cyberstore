import re

from django.db import migrations


PRODUCT_CATEGORIES = {
    # Laptops
    "dell-alienware-m16-moshchnyy-igrovoy-noutbuk": "gaming-laptops",
    "hp-omen-16-moshchnyy-igrovoy-noutbuk-premium-klassa": "gaming-laptops",
    "asus-tuf-gaming-a15": "gaming-laptops",
    "acer-extensa-15": "office-laptops",
    "hp-laptop-15": "office-laptops",
    # Ready-made PCs
    "igrovoy-pk-cyber-phantom-rtx-4060": "gaming-pcs",
    "igrovoy-pk-cyber-beast-rtx-4070-ti-super": "gaming-pcs",
    "pk-cyber-strike-kibersport-i-rabota": "gaming-pcs",
    "ofisnyy-pk-cyber-office-pro": "office-pcs",
    # Components
    "videokarta-palit-geforce-rtx-4070-dual-12gb": "gpu",
    "ssd-nakopitel-kingston-kc3000-1tb-m2-pcie-40": "storage",
    "protsessor-amd-ryzen-7-7800x3d-am5-oem": "cpu",
}


def assign(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Product = apps.get_model("catalog", "Product")
    ProductSpec = apps.get_model("catalog", "ProductSpec")

    for slug, category_slug in PRODUCT_CATEGORIES.items():
        target = Category.objects.filter(slug=category_slug, is_active=True).first()
        if not target:
            continue
        product = Product.objects.filter(slug=slug).first()
        # Only move goods that still sit in the broad root section. An editor's
        # later choice of a more precise category is never overwritten.
        if product and product.category_id != target.pk and product.category.parent_id is None:
            product.category = target
            product.save(update_fields=["category"])

    inch = re.compile(r"(\d+)\.(\d+)\"")
    for spec in ProductSpec.objects.filter(value__contains='"'):
        fixed = inch.sub(lambda m: f"{m.group(1)},{m.group(2)}\u2033", spec.value)
        fixed = re.sub(r"(\d+)\"", lambda m: f"{m.group(1)}\u2033", fixed)
        if fixed != spec.value:
            spec.value = fixed
            spec.save(update_fields=["value"])


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0012_merge_legacy_monitors"),
    ]

    operations = [
        migrations.RunPython(assign, migrations.RunPython.noop),
    ]