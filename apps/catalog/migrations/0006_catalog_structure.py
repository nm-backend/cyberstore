import re

from django.db import migrations


ROOTS = [
    ("laptops", "Ноутбуки и аксессуары", "laptop", 1, "Ноутбуки для игр, учёбы и работы"),
    ("pcs", "Настольные ПК", "desktop", 2, "Игровые и офисные системные блоки, моноблоки и неттопы"),
    ("components", "Комплектующие для ПК", "chip", 3, "Комплектующие для сборки и апгрейда ПК"),
    ("monitors", "Мониторы", "desktop", 4, "Мониторы для работы, учёбы и игр"),
]

SUBCATEGORIES = [
    ("systems", "Системные блоки", "pcs", "desktop", 1, "Готовые сборки и рабочие станции"),
    ("all-in-one", "Моноблоки", "pcs", "desktop", 2, "Моноблоки для дома и офиса"),
    ("nettops", "Неттопы / тонкие клиенты", "pcs", "desktop", 3, "Компактные ПК и тонкие клиенты"),
    ("gaming-pcs", "Игровые ПК", "systems", "gamepad", 1, "Игровые системные блоки"),
    ("office-pcs", "Офисные ПК", "systems", "briefcase", 2, "ПК для офиса и учёбы"),
    ("gaming-laptops", "Игровые ноутбуки", "laptops", "gamepad", 1, "Ноутбуки для игр"),
    ("office-laptops", "Ноутбуки для учёбы и офиса", "laptops", "briefcase", 2, "Ноутбуки для работы и учёбы"),
    ("ram", "Оперативная память", "components", "chip", 1, "Модули памяти для ПК"),
    ("motherboards", "Материнские платы", "components", "chip", 2, "Материнские платы"),
    ("gpu", "Видеокарты", "components", "desktop", 3, "Видеокарты для игр и работы"),
    ("cpu", "Процессоры", "components", "chip", 4, "Процессоры Intel и AMD"),
    ("storage", "SSD и накопители", "components", "chip", 5, "SSD, HDD и NVMe накопители"),
    ("cases", "Корпуса ПК", "components", "grid", 6, "Корпуса для сборки ПК"),
    ("build-kits", "Комплекты для сборки ПК", "components", "grid", 7, "Готовые комплекты для сборки"),
    ("sound-cards", "Звуковые карты", "components", "chip", 8, "Внутренние и внешние звуковые карты"),
    ("optical-drives", "Оптические приводы", "components", "grid", 9, "DVD и Blu-ray приводы"),
    ("capture-cards", "Карты видеозахвата", "components", "film", 10, "Карты захвата для стримов и записи"),
    ("other-components", "Другие комплектующие", "components", "grid", 11, "Прочие комплектующие"),
]

NEW_SPEC_TYPES = [
    ("Количество ядер", "number_unit", "ядер", 14, ["pcs", "laptops", "cpu"]),
    ("Диагональ экрана", "number_unit", "″", 15, ["laptops", "monitors"]),
    ("Тип экрана", "choice", "", 16, ["laptops", "monitors"]),
    ("Разрешение экрана", "choice", "", 17, ["laptops", "monitors"]),
    ("Частота обновления", "number_unit", "Гц", 18, ["monitors"]),
    ("Цвет", "multi_choice", "", 19, ["pcs", "laptops", "monitors", "cases"]),
    ("Тип ПК", "choice", "", 20, ["pcs"]),
    ("Тип накопителя", "choice", "", 21, ["pcs", "laptops", "storage"]),
    ("Объём накопителя", "number_unit", "ГБ", 22, ["storage"]),
    ("Тип памяти", "choice", "", 23, ["ram", "motherboards"]),
    ("Частота памяти", "number_unit", "МГц", 24, ["ram"]),
    ("Сокет", "choice", "", 25, ["motherboards"]),
    ("Форм-фактор", "choice", "", 26, ["motherboards", "cases"]),
    ("Объём видеопамяти", "number_unit", "ГБ", 27, ["gpu", "pcs", "laptops"]),
    ("Интерфейс", "choice", "", 28, ["storage"]),
    ("Производитель видеокарты", "choice", "", 29, ["gpu", "pcs", "laptops"]),
    ("Объём памяти", "number_unit", "ГБ", 30, ["ram"]),
]

EXISTING_SPEC_CATEGORIES = {
    "Процессор": ["pcs", "laptops"],
    "Видеокарта": ["pcs", "laptops", "gpu"],
    "Оперативная память": ["pcs", "laptops", "ram"],
    "Накопитель": ["pcs", "laptops", "storage"],
    "Экран": ["laptops", "monitors"],
    "Операционная система": ["laptops"],
    "Материнская плата": ["motherboards", "pcs"],
    "Блок питания": ["pcs"],
    "Корпус": ["cases", "pcs"],
    "Охлаждение": ["pcs", "cpu"],
    "Аккумулятор": ["laptops"],
    "Порты и интерфейсы": ["motherboards", "gpu", "cpu", "storage"],
    "Вес": ["laptops", "monitors"],
}

REFERENCE_OPTIONS = {
    "Процессор": [
        "Intel Core i3", "Intel Core i5", "Intel Core i7", "Intel Core i9",
        "AMD Ryzen 3", "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9",
    ],
    "Производитель видеокарты": ["NVIDIA GeForce", "AMD Radeon", "Intel Graphics", "Другое"],
    "Тип ПК": ["Системный блок", "Моноблок", "Неттоп / Тонкий клиент"],
    "Тип накопителя": ["SSD", "HDD", "SSHD", "eMMC"],
    "Тип экрана": ["IPS", "VA", "TN", "OLED", "Другое"],
    "Операционная система": ["Windows", "Mac OS", "Linux", "Другая ОС"],
    "Разрешение экрана": ["Full HD", "2K", "4K"],
    "Частота обновления": ["60 Гц", "75 Гц", "120 Гц", "144 Гц", "165 Гц", "240 Гц"],
    "Диагональ экрана": ['13.3"', '14"', '15.6"', '17.3"', '21.5"', '23.8"', '24"', '27"', '32"'],
    "Количество ядер": ["4 ядра", "6 ядер", "8 ядер", "10 ядер", "12 ядер", "16 ядер"],
    "Тип памяти": ["DDR3", "DDR4", "DDR5"],
    "Частота памяти": ["2666 МГц", "3200 МГц", "3600 МГц", "6000 МГц"],
    "Сокет": ["AM4", "AM5", "LGA1200", "LGA1700"],
    "Форм-фактор": ["ATX", "mATX", "Mini-ITX"],
    "Интерфейс": ["SATA", "NVMe", "PCIe", "USB"],
    "Цвет": ["Чёрный", "Белый", "Серый", "Серебристый", "Синий", "Красный"],
    "Объём памяти": ["4 ГБ", "8 ГБ", "16 ГБ", "32 ГБ", "64 ГБ", "128 ГБ"],
    "Объём накопителя": ["256 ГБ", "512 ГБ", "1 ТБ", "2 ТБ"],
    "Объём видеопамяти": ["4 ГБ", "6 ГБ", "8 ГБ", "12 ГБ", "16 ГБ"],
}

CATEGORY_FILTERS = {
    "pcs": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("spec", "Процессор", "Процессор"),
        ("spec", "Количество ядер", "Количество ядер"), ("spec", "Видеокарта", "Видеокарта"),
        ("spec", "Оперативная память", "Оперативная память"),
        ("spec", "Тип накопителя", "Тип накопителя"), ("use_case", None, "Назначение"),
        ("spec", "Тип ПК", "Тип ПК"), ("spec", "Цвет", "Цвет"),
        ("installment", None, "Рассрочка"), ("delivery", None, "Доставка"),
    ],
    "laptops": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("spec", "Процессор", "Процессор"),
        ("spec", "Количество ядер", "Количество ядер"), ("spec", "Видеокарта", "Видеокарта"),
        ("spec", "Оперативная память", "Оперативная память"),
        ("spec", "Диагональ экрана", "Диагональ"), ("spec", "Операционная система", "Операционная система"),
        ("spec", "Тип экрана", "Тип экрана"), ("spec", "Цвет", "Цвет"),
        ("spec", "Тип накопителя", "Тип накопителя"), ("use_case", None, "Назначение"),
        ("installment", None, "Рассрочка"), ("delivery", None, "Доставка"),
    ],
    "monitors": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("spec", "Диагональ экрана", "Диагональ"),
        ("spec", "Тип экрана", "Тип экрана"), ("spec", "Разрешение экрана", "Разрешение"),
        ("spec", "Частота обновления", "Частота обновления"), ("spec", "Цвет", "Цвет"),
        ("delivery", None, "Доставка"),
    ],
    "components": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("use_case", None, "Назначение"),
        ("delivery", None, "Доставка"),
    ],
    "cpu": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("spec", "Процессор", "Процессор"),
        ("spec", "Количество ядер", "Количество ядер"), ("delivery", None, "Доставка"),
    ],
    "gpu": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("spec", "Производитель видеокарты", "Производитель"),
        ("spec", "Видеокарта", "Модель"), ("spec", "Объём видеопамяти", "Объём видеопамяти"),
        ("delivery", None, "Доставка"),
    ],
    "storage": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("spec", "Тип накопителя", "Тип"),
        ("spec", "Объём накопителя", "Объём"), ("spec", "Интерфейс", "Интерфейс"),
        ("delivery", None, "Доставка"),
    ],
    "ram": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("spec", "Объём памяти", "Объём"),
        ("spec", "Тип памяти", "Тип памяти"), ("spec", "Частота памяти", "Частота"),
        ("delivery", None, "Доставка"),
    ],
    "motherboards": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("spec", "Сокет", "Сокет"),
        ("spec", "Форм-фактор", "Форм-фактор"), ("spec", "Тип памяти", "Тип памяти"),
        ("delivery", None, "Доставка"),
    ],
    "cases": [
        ("brand", None, "Бренд"), ("price", None, "Цена"), ("condition", None, "Состояние"),
        ("location", None, "Местоположение"), ("spec", "Форм-фактор", "Форм-фактор"),
        ("spec", "Цвет", "Цвет"), ("delivery", None, "Доставка"),
    ],
}


def _descendants(Category, category):
    ids, frontier = [category.pk], [category.pk]
    while frontier:
        frontier = list(Category.objects.filter(parent_id__in=frontier).values_list("pk", flat=True))
        ids.extend(frontier)
    return ids


def _ensure_category(Category, slug, name, parent, icon, order, description,
                     display_mode="both", show_brand_tiles=False):
    category, created = Category.objects.get_or_create(
        slug=slug,
        defaults={
            "name": name,
            "parent": parent,
            "icon": icon,
            "order": order,
            "description": description,
            "display_mode": display_mode,
            "show_brand_tiles": show_brand_tiles,
            "is_active": True,
        },
    )
    if not created:
        category.name = name
        category.parent = parent
        category.icon = icon
        category.order = order
        if description:
            category.description = description
        category.display_mode = display_mode
        category.show_brand_tiles = show_brand_tiles
        category.is_active = True
        category.save()
    return category


def _link_specs(SpecOption, ProductSpec):
    option_map = {
        (option.spec_type_id, option.name.lower()): option
        for option in SpecOption.objects.all()
    }
    for spec in ProductSpec.objects.all():
        label = (spec.filter_value or "").strip() or (spec.value or "").strip()
        option = option_map.get((spec.spec_type_id, label[:120].lower()))
        if option and spec.option_id != option.pk:
            spec.option = option
            spec.save(update_fields=["option"])


def load(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Brand = apps.get_model("catalog", "Brand")
    SpecType = apps.get_model("catalog", "SpecType")
    SpecOption = apps.get_model("catalog", "SpecOption")
    ProductSpec = apps.get_model("catalog", "ProductSpec")
    Product = apps.get_model("catalog", "Product")
    CategoryFilter = apps.get_model("catalog", "CategoryFilter")

    # ---- Categories -----------------------------------------------------
    categories = {}
    for slug, name, icon, order, description in ROOTS:
        categories[slug] = _ensure_category(
            Category, slug, name, None, icon, order, description, show_brand_tiles=True
        )
    for slug, name, parent_slug, icon, order, description in SUBCATEGORIES:
        categories[slug] = _ensure_category(
            Category, slug, name, categories[parent_slug], icon, order, description
        )

    # ---- Characteristics ------------------------------------------------
    spec_types = {spec.name: spec for spec in SpecType.objects.all()}
    for name, data_type, unit, order, category_slugs in NEW_SPEC_TYPES:
        spec, created = SpecType.objects.get_or_create(
            name=name,
            defaults={
                "data_type": data_type,
                "unit": unit,
                "order": order,
                "is_active": True,
            },
        )
        if not created:
            spec.data_type = data_type
            spec.unit = unit
            spec.order = order
            spec.is_active = True
            spec.save()
        spec_types[name] = spec

    for name, slugs in EXISTING_SPEC_CATEGORIES.items():
        spec = spec_types.get(name)
        if spec:
            spec.is_active = True
            spec.save(update_fields=["is_active"])
            spec.categories.set([categories[slug] for slug in slugs if slug in categories])

    for name, _, _, _, slugs in NEW_SPEC_TYPES:
        spec_types[name].categories.set([categories[slug] for slug in slugs if slug in categories])

    # ---- Dictionary values ---------------------------------------------
    for spec_name, labels in REFERENCE_OPTIONS.items():
        spec = spec_types.get(spec_name)
        if not spec:
            continue
        for order, label in enumerate(labels, start=1):
            SpecOption.objects.get_or_create(
                spec_type=spec, name=label, defaults={"order": order, "is_active": True}
            )

    # Canonical processor families: «Ryzen 9» -> «AMD Ryzen 9».
    processor = spec_types.get("Процессор")
    if processor:
        for spec in ProductSpec.objects.filter(spec_type=processor):
            label = (spec.filter_value or "").strip()
            if re.match(r"^ryzen\b", label, re.I):
                label = re.sub(r"^ryzen\b", "AMD Ryzen", label, flags=re.I)
                spec.filter_value = label
                spec.save(update_fields=["filter_value"])

    _link_specs(SpecOption, ProductSpec)

    # ---- Derived real characteristics ----------------------------------
    def spec_value_map(spec_name):
        spec = spec_types.get(spec_name)
        if not spec:
            return {}
        return {item.product_id: item.value for item in ProductSpec.objects.filter(spec_type=spec)}

    def add_spec(product_id, spec_name, value, order):
        spec = spec_types.get(spec_name)
        if not spec or not value:
            return
        if ProductSpec.objects.filter(product_id=product_id, spec_type=spec).exists():
            return
        label = value[:200]
        option = SpecOption.objects.filter(spec_type=spec, name__iexact=label[:120]).first()
        if not option:
            option = SpecOption.objects.create(spec_type=spec, name=label[:120], order=200)
        ProductSpec.objects.create(
            product_id=product_id, spec_type=spec, value=label,
            filter_value=label, option=option, order=order,
        )

    processors = spec_value_map("Процессор")
    screens = spec_value_map("Экран")
    storages = spec_value_map("Накопитель")
    gpus = spec_value_map("Видеокарта")

    pcs_root = categories.get("pcs")
    pcs_ids = set(_descendants(Category, pcs_root)) if pcs_root else set()

    for product in Product.objects.all():
        processor_value = processors.get(product.pk, "")
        if processor_value:
            match = re.search(r"(\d+)\s*ядер", processor_value, re.I)
            if match:
                add_spec(product.pk, "Количество ядер", f"{match.group(1)} ядер", 40)

        screen_value = screens.get(product.pk, "")
        if screen_value:
            match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:["″”]|дюйм)', screen_value)
            if match:
                add_spec(product.pk, "Диагональ экрана", match.group(1).replace(",", ".") + '"', 41)
            for screen_type in ("IPS", "VA", "TN", "OLED"):
                if re.search(rf"(?<![A-Za-z]){screen_type}(?![A-Za-z])", screen_value, re.I):
                    add_spec(product.pk, "Тип экрана", screen_type, 42)
                    break
            if re.search(r"full\s*hd|\bfhd\b", screen_value, re.I):
                add_spec(product.pk, "Разрешение экрана", "Full HD", 43)
            elif re.search(r"\bqhd\b|\b2k\b", screen_value, re.I):
                add_spec(product.pk, "Разрешение экрана", "2K", 43)
            elif re.search(r"\b4k\b|\buhd\b", screen_value, re.I):
                add_spec(product.pk, "Разрешение экрана", "4K", 43)

        storage_value = storages.get(product.pk, "")
        if storage_value:
            if re.search(r"ssd|nvme", storage_value, re.I):
                add_spec(product.pk, "Тип накопителя", "SSD", 44)
            elif re.search(r"hdd", storage_value, re.I):
                add_spec(product.pk, "Тип накопителя", "HDD", 44)

        gpu_value = gpus.get(product.pk, "")
        if gpu_value:
            if re.search(r"nvidia|geforce", gpu_value, re.I):
                add_spec(product.pk, "Производитель видеокарты", "NVIDIA GeForce", 45)
            elif re.search(r"radeon|amd", gpu_value, re.I):
                add_spec(product.pk, "Производитель видеокарты", "AMD Radeon", 45)
            elif re.search(r"intel|встроен", gpu_value, re.I):
                add_spec(product.pk, "Производитель видеокарты", "Intel Graphics", 45)

        if product.category_id in pcs_ids:
            add_spec(product.pk, "Тип ПК", "Системный блок", 46)

    _link_specs(SpecOption, ProductSpec)

    # ---- Category filters ----------------------------------------------
    for category_slug, rows in CATEGORY_FILTERS.items():
        category = categories.get(category_slug)
        if not category:
            continue
        for order, (source, spec_name, title) in enumerate(rows, start=1):
            spec = spec_types.get(spec_name) if spec_name else None
            row = CategoryFilter.objects.filter(
                category=category, source=source, spec_type=spec
            ).first()
            if row:
                row.title = title
                row.order = order
                row.is_active = True
                row.save()
            else:
                CategoryFilter.objects.create(
                    category=category, source=source, spec_type=spec,
                    title=title, order=order, is_active=True,
                )

    # ---- Brands: bind real brands to the roots they are sold in ---------
    brand_categories = {}
    for brand_id, category_id in Product.objects.exclude(brand=None).values_list("brand_id", "category_id"):
        category = Category.objects.filter(pk=category_id).first()
        if not category:
            continue
        node = category
        while node.parent_id:
            node = Category.objects.get(pk=node.parent_id)
        brand_categories.setdefault(brand_id, set()).add(node.pk)

    for brand in Brand.objects.all():
        if not brand.categories.exists():
            brand.is_active = True
            brand.save(update_fields=["is_active"])
            brand.categories.set(brand_categories.get(brand.pk, set()))


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_specoption_brand_categories_brand_is_active_and_more"),
    ]

    operations = [
        migrations.RunPython(load, migrations.RunPython.noop),
    ]
