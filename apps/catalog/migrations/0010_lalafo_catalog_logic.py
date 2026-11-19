"""Каталог по логике Lalafo для четырёх разделов.

Подкатегории есть только у «Комплектующие для ПК» (как на lalafo.kg), у ПК,
мониторов и ноутбуков — свой набор фильтров без подразделов.

Каждый раздел/подраздел получает собственные блоки фильтров:
- Настольные ПК: назначение, процессор, ядра, видеокарта, ОЗУ, накопитель, тип ПК, цвет;
- Комплектующие: у каждого подраздела свои характеристики (сокет, частота памяти,
  объём видеопамяти, мощность блока питания и т. д.);
- Мониторы: диагональ, тип экрана, разрешение, частота, цвет;
- Ноутбуки: процессор, ядра, видеокарта, ОЗУ, диагональ, экран, ОС, накопитель, цвет.
"""

from django.db import migrations

COMPONENT_SUBCATEGORIES = [
    # slug, название, иконка, порядок
    ("gpu", "Видеокарты", "desktop", 1),
    ("storage", "Жёсткие диски", "chip", 2),
    ("ram", "Оперативная память (RAM)", "chip", 3),
    ("motherboards", "Материнские платы", "chip", 4),
    ("cpu", "Процессоры", "chip", 5),
    ("power-supplies", "Блоки питания", "chip", 6),
    ("cases", "Корпуса ПК", "grid", 7),
    ("build-kits", "Комплекты для сборки ПК", "grid", 8),
    ("sound-cards", "Звуковые карты", "chip", 9),
    ("optical-drives", "Оптические приводы", "grid", 10),
    ("capture-cards", "Карты видеозахвата", "film", 11),
    ("other-components", "Другие комплектующие", "grid", 12),
]

NEW_SPEC_TYPES = [
    # name, data_type, unit, категории, значения справочника
    ("Мощность блока питания", "number_unit", "Вт", ["power-supplies"],
     ["350 Вт", "400 Вт", "450 Вт", "500 Вт", "550 Вт", "600 Вт", "650 Вт",
      "700 Вт", "750 Вт", "800 Вт", "850 Вт", "1000 Вт", "1200 Вт"]),
    ("Сертификат 80 Plus", "choice", "", ["power-supplies"],
     ["Без сертификата", "80 Plus", "80 Plus Bronze", "80 Plus Silver",
      "80 Plus Gold", "80 Plus Platinum", "80 Plus Titanium"]),
    ("Состав комплекта", "choice", "", ["build-kits"],
     ["Процессор", "Материнская плата", "Процессор + материнская плата",
      "Процессор + плата + ОЗУ", "Полный комплект"]),
    ("Форм-фактор накопителя", "choice", "", ["storage"],
     ['2.5"', '3.5"', "M.2"]),
]

EXTRA_OPTIONS = {
    "Тип экрана": ["LED", "LCD"],
    "Сокет": ["LGA1851", "AM4", "AM5", "LGA1200", "LGA1700"],
}

# slug раздела/подраздела → [(источник, характеристика, заголовок)]
FILTERS = {
    "pcs": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("location", None, "Местоположение"),
        ("use_case", None, "Назначение"),
        ("spec", "Процессор", "Процессор"),
        ("spec", "Количество ядер", "Количество ядер"),
        ("spec", "Видеокарта", "Видеокарта"),
        ("spec", "Оперативная память", "Оперативная память"),
        ("spec", "Тип накопителя", "Накопитель"),
        ("spec", "Тип ПК", "Тип ПК"),
        ("spec", "Цвет", "Цвет"),
        ("installment", None, "Рассрочка"),
        ("delivery", None, "Доставка"),
    ],
    "components": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("location", None, "Местоположение"),
        ("use_case", None, "Назначение"),
        ("delivery", None, "Доставка"),
    ],
    "gpu": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("spec", "Производитель видеокарты", "Производитель"),
        ("spec", "Видеокарта", "Модель"),
        ("spec", "Объём видеопамяти", "Объём видеопамяти"),
        ("delivery", None, "Доставка"),
    ],
    "storage": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("spec", "Тип накопителя", "Тип"),
        ("spec", "Объём накопителя", "Объём"),
        ("spec", "Интерфейс", "Интерфейс"),
        ("spec", "Форм-фактор накопителя", "Форм-фактор"),
        ("delivery", None, "Доставка"),
    ],
    "ram": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("spec", "Тип памяти", "Тип памяти"),
        ("spec", "Объём памяти", "Объём"),
        ("spec", "Частота памяти", "Частота"),
        ("delivery", None, "Доставка"),
    ],
    "motherboards": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("spec", "Сокет", "Сокет"),
        ("spec", "Форм-фактор", "Форм-фактор"),
        ("spec", "Тип памяти", "Тип памяти"),
        ("delivery", None, "Доставка"),
    ],
    "cpu": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("spec", "Процессор", "Процессор"),
        ("spec", "Количество ядер", "Количество ядер"),
        ("spec", "Сокет", "Сокет"),
        ("delivery", None, "Доставка"),
    ],
    "power-supplies": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("spec", "Мощность блока питания", "Мощность"),
        ("spec", "Сертификат 80 Plus", "Сертификат"),
        ("delivery", None, "Доставка"),
    ],
    "cases": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("spec", "Форм-фактор", "Форм-фактор"),
        ("spec", "Цвет", "Цвет"),
        ("delivery", None, "Доставка"),
    ],
    "build-kits": [
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("spec", "Состав комплекта", "Состав комплекта"),
        ("delivery", None, "Доставка"),
    ],
    "sound-cards": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("delivery", None, "Доставка"),
    ],
    "optical-drives": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("delivery", None, "Доставка"),
    ],
    "capture-cards": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("delivery", None, "Доставка"),
    ],
    "other-components": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("delivery", None, "Доставка"),
    ],
    "monitors": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("location", None, "Местоположение"),
        ("spec", "Диагональ экрана", "Диагональ"),
        ("spec", "Тип экрана", "Тип экрана"),
        ("spec", "Разрешение экрана", "Разрешение"),
        ("spec", "Частота обновления", "Частота обновления"),
        ("spec", "Цвет", "Цвет"),
        ("delivery", None, "Доставка"),
    ],
    "laptops": [
        ("brand", None, "Бренд"),
        ("price", None, "Цена"),
        ("condition", None, "Состояние"),
        ("location", None, "Местоположение"),
        ("use_case", None, "Назначение"),
        ("spec", "Процессор", "Процессор"),
        ("spec", "Количество ядер", "Количество ядер"),
        ("spec", "Видеокарта", "Видеокарта"),
        ("spec", "Оперативная память", "Оперативная память"),
        ("spec", "Диагональ экрана", "Диагональ"),
        ("spec", "Тип экрана", "Тип экрана"),
        ("spec", "Операционная система", "Операционная система"),
        ("spec", "Тип накопителя", "Накопитель"),
        ("spec", "Цвет", "Цвет"),
        ("installment", None, "Рассрочка"),
        ("delivery", None, "Доставка"),
    ],
}


def configure(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    SpecType = apps.get_model("catalog", "SpecType")
    SpecOption = apps.get_model("catalog", "SpecOption")
    CategoryFilter = apps.get_model("catalog", "CategoryFilter")

    components = Category.objects.filter(slug="components").first()
    if components is None:
        return

    # --- Подразделы «Комплектующих» как на Lalafo -----------------------
    for slug, name, icon, order in COMPONENT_SUBCATEGORIES:
        Category.objects.update_or_create(
            slug=slug,
            defaults={
                "name": name,
                "parent": components,
                "icon": icon,
                "order": order,
                "is_active": True,
                "display_mode": "products",
            },
        )

    # --- Новые характеристики и значения справочника --------------------
    spec_types = {spec.name: spec for spec in SpecType.objects.all()}
    for name, data_type, unit, category_slugs, options in NEW_SPEC_TYPES:
        spec, _ = SpecType.objects.get_or_create(
            name=name,
            defaults={"data_type": data_type, "unit": unit, "is_active": True, "order": 100},
        )
        spec.data_type = data_type
        spec.unit = unit
        spec.is_active = True
        spec.save(update_fields=["data_type", "unit", "is_active"])
        spec.categories.set(
            Category.objects.filter(slug__in=category_slugs)
        )
        for order, label in enumerate(options, start=1):
            SpecOption.objects.get_or_create(
                spec_type=spec, name=label, defaults={"order": order, "is_active": True}
            )
        spec_types[name] = spec

    for spec_name, labels in EXTRA_OPTIONS.items():
        spec = spec_types.get(spec_name)
        if spec is None:
            continue
        existing = set(spec.options.values_list("name", flat=True))
        for label in labels:
            if label in existing:
                continue
            SpecOption.objects.create(
                spec_type=spec, name=label, order=100, is_active=True
            )

    # --- Собственные фильтры у каждого раздела и подраздела -------------
    for category_slug, rows in FILTERS.items():
        category = Category.objects.filter(slug=category_slug).first()
        if category is None:
            continue
        CategoryFilter.objects.filter(category=category).delete()
        for order, (source, spec_name, title) in enumerate(rows, start=1):
            spec = spec_types.get(spec_name) if spec_name else None
            CategoryFilter.objects.create(
                category=category,
                source=source,
                spec_type=spec,
                title=title,
                order=order,
                is_active=True,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0009_pcs_filter_first"),
    ]

    operations = [
        migrations.RunPython(configure, migrations.RunPython.noop),
    ]
