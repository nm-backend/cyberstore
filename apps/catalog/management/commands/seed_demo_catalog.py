"""Наполняет пустые разделы каталога демонстрационными товарами.

Все созданные товары помечены «Демо-данные», поэтому их легко найти и удалить
в админке или командой ``manage.py seed_demo_catalog --clear``.
Повторный запуск обновляет товары по slug и не создаёт дублей.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Max

from apps.catalog.models import (
    Brand,
    Category,
    CategoryFilter,
    Product,
    ProductSpec,
    SpecOption,
    SpecType,
    UseCase,
)

# Новые бренды: (slug, название).
BRANDS = [
    ("samsung", "Samsung"),
    ("lg", "LG"),
    ("aoc", "AOC"),
    ("msi", "MSI"),
    ("gigabyte", "Gigabyte"),
    ("crucial", "Crucial"),
    ("intel", "Intel"),
    ("deepcool", "DeepCool"),
    ("zalman", "Zalman"),
    ("lenovo", "Lenovo"),
    ("apple", "Apple"),
]

# Значения, которых ещё нет в справочнике.
EXTRA_OPTIONS = {
    "Видеокарта": ["RX 7600"],
    "Объём накопителя": ["480 ГБ"],
    "Процессор": ["Apple M2"],
}

# Фильтры для подкатегорий комплектующих: раньше они наследовали только
# общие фильтры корня, поэтому характеристики в них не показывались.
EXTRA_FILTERS = {
    "gpu": ["Производитель видеокарты", "Видеокарта", "Объём видеопамяти"],
    "cpu": ["Количество ядер", "Охлаждение"],
    "storage": ["Тип накопителя", "Объём накопителя", "Интерфейс"],
    "ram": ["Тип памяти", "Объём памяти", "Частота памяти"],
    "motherboards": ["Сокет", "Форм-фактор", "Тип памяти"],
    "cases": ["Форм-фактор", "Цвет"],
}

# (slug, название, категория, бренд, цена, старая цена, состояние, доставка,
#  гарантия, рассрочка, на главной, короткое описание, назначения,
#  характеристики: (характеристика, значение, значение справочника или None))
PRODUCTS = [
    # --- Мониторы -------------------------------------------------------
    (
        "monitor-samsung-odyssey-g5-27", 'Монитор Samsung Odyssey G5 27"', "monitors", "Samsung",
        24900, 27900, "new", "free", "12 месяцев", True, True,
        '27", 2K, 144 Гц, изогнутый экран для игр',
        ["games", "design"],
        [
            ("Диагональ экрана", '27"', '27"'),
            ("Тип экрана", "VA", "VA"),
            ("Разрешение экрана", "2560×1440 (2K)", "2K"),
            ("Частота обновления", "144 Гц", "144 Гц"),
            ("Цвет", "Чёрный", "Чёрный"),
        ],
    ),
    (
        "monitor-lg-ultragear-24gn60r", "Монитор LG UltraGear 24GN60R", "monitors", "LG",
        15900, None, "new", "free", "12 месяцев", True, False,
        '23.8", Full HD, IPS, 144 Гц',
        ["games"],
        [
            ("Диагональ экрана", '23.8"', '23.8"'),
            ("Тип экрана", "IPS", "IPS"),
            ("Разрешение экрана", "1920×1080 (Full HD)", "Full HD"),
            ("Частота обновления", "144 Гц", "144 Гц"),
            ("Цвет", "Чёрный", "Чёрный"),
        ],
    ),
    (
        "monitor-aoc-24b2xh", "Монитор AOC 24B2XH", "monitors", "AOC",
        8900, None, "new", "pickup", "12 месяцев", False, False,
        '23.8", Full HD, IPS, 75 Гц — для офиса и учёбы',
        ["office", "study"],
        [
            ("Диагональ экрана", '23.8"', '23.8"'),
            ("Тип экрана", "IPS", "IPS"),
            ("Разрешение экрана", "1920×1080 (Full HD)", "Full HD"),
            ("Частота обновления", "75 Гц", "75 Гц"),
            ("Цвет", "Чёрный", "Чёрный"),
        ],
    ),
    (
        "monitor-msi-g274qpf", "Монитор MSI G274QPF", "monitors", "MSI",
        27500, None, "new", "free", "24 месяца", True, False,
        '27", 2K, Rapid IPS, 165 Гц',
        ["games", "design"],
        [
            ("Диагональ экрана", '27"', '27"'),
            ("Тип экрана", "IPS", "IPS"),
            ("Разрешение экрана", "2560×1440 (2K)", "2K"),
            ("Частота обновления", "165 Гц", "165 Гц"),
            ("Цвет", "Чёрный", "Чёрный"),
        ],
    ),
    (
        "monitor-samsung-viewfinity-s8-32", 'Монитор Samsung ViewFinity S8 32"', "monitors", "Samsung",
        38900, None, "new", "paid", "12 месяцев", True, False,
        '32", 4K, IPS, 60 Гц — для дизайна и монтажа',
        ["design", "video", "programming"],
        [
            ("Диагональ экрана", '32"', '32"'),
            ("Тип экрана", "IPS", "IPS"),
            ("Разрешение экрана", "3840×2160 (4K)", "4K"),
            ("Частота обновления", "60 Гц", "60 Гц"),
            ("Цвет", "Чёрный", "Чёрный"),
        ],
    ),
    (
        "monitor-lg-22mk400h", "Монитор LG 22MK400H", "monitors", "LG",
        7200, None, "new", "pickup", "12 месяцев", False, False,
        '21.5", Full HD, 75 Гц — компактный монитор для дома',
        ["office", "study"],
        [
            ("Диагональ экрана", '21.5"', '21.5"'),
            ("Тип экрана", "TN", "TN"),
            ("Разрешение экрана", "1920×1080 (Full HD)", "Full HD"),
            ("Частота обновления", "75 Гц", "75 Гц"),
            ("Цвет", "Чёрный", "Чёрный"),
        ],
    ),
    # --- Настольные ПК: моноблок и неттоп -------------------------------
    (
        "all-in-one-hp-proone-240-g9", "Моноблок HP ProOne 240 G9", "all-in-one", "HP",
        68900, None, "new", "free", "12 месяцев", True, False,
        '23.8", Intel Core i5, 8 ГБ, SSD 512 ГБ',
        ["office", "study"],
        [
            ("Процессор", "Intel Core i5-1235U", "Intel Core i5"),
            ("Количество ядер", "10 ядер", "10 ядер"),
            ("Оперативная память", "8 ГБ", "8 ГБ"),
            ("Накопитель", "512 ГБ SSD", None),
            ("Тип накопителя", "SSD", "SSD"),
            ("Видеокарта", "Intel UHD Graphics", "Встроенная"),
            ("Производитель видеокарты", "Intel Graphics", "Intel Graphics"),
            ("Тип ПК", "Моноблок", "Моноблок"),
            ("Цвет", "Чёрный", "Чёрный"),
        ],
    ),
    (
        "nettop-lenovo-thinkcentre-m75n", "Неттоп Lenovo ThinkCentre M75n", "nettops", "Lenovo",
        24900, None, "new", "free", "12 месяцев", False, False,
        "AMD Ryzen 5, 8 ГБ, SSD 256 ГБ, компактный корпус",
        ["office", "programming"],
        [
            ("Процессор", "AMD Ryzen 5 5500U", "AMD Ryzen 5"),
            ("Количество ядер", "6 ядер", "6 ядер"),
            ("Оперативная память", "8 ГБ", "8 ГБ"),
            ("Накопитель", "256 ГБ SSD", None),
            ("Тип накопителя", "SSD", "SSD"),
            ("Видеокарта", "AMD Radeon Graphics", "Встроенная"),
            ("Производитель видеокарты", "AMD Radeon", "AMD Radeon"),
            ("Тип ПК", "Неттоп / Тонкий клиент", "Неттоп / Тонкий клиент"),
            ("Цвет", "Чёрный", "Чёрный"),
        ],
    ),
    # --- Ноутбуки -------------------------------------------------------
    (
        "laptop-apple-macbook-air-13-m2", "Ноутбук Apple MacBook Air 13 M2", "laptops", "Apple",
        92000, 99000, "new", "free", "12 месяцев", True, True,
        "Apple M2, 8 ГБ, SSD 256 ГБ, 13.3\" Liquid Retina",
        ["study", "office", "programming", "design"],
        [
            ("Процессор", "Apple M2", "Apple M2"),
            ("Количество ядер", "8 ядер", "8 ядер"),
            ("Оперативная память", "8 ГБ", "8 ГБ"),
            ("Накопитель", "256 ГБ SSD", None),
            ("Тип накопителя", "SSD", "SSD"),
            ("Диагональ экрана", '13.3"', '13.3"'),
            ("Тип экрана", "IPS", "IPS"),
            ("Разрешение экрана", "2560×1664 (2K)", "2K"),
            ("Операционная система", "Mac OS", "Mac OS"),
            ("Цвет", "Серебристый", "Серебристый"),
        ],
    ),
    # --- Оперативная память ---------------------------------------------
    (
        "ram-kingston-fury-beast-16gb-ddr4", "Оперативная память Kingston Fury Beast 16 ГБ DDR4", "ram", "Kingston",
        4200, None, "new", "pickup", "Пожизненная", False, False,
        "2×8 ГБ, DDR4, 3200 МГц, радиаторы",
        ["games", "office"],
        [
            ("Тип памяти", "DDR4", "DDR4"),
            ("Объём памяти", "16 ГБ (2×8)", "16 ГБ"),
            ("Частота памяти", "3200 МГц", "3200 МГц"),
        ],
    ),
    (
        "ram-kingston-fury-beast-32gb-ddr4-3600", "Оперативная память Kingston Fury Beast 32 ГБ DDR4 3600", "ram", "Kingston",
        8900, None, "new", "pickup", "Пожизненная", False, False,
        "2×16 ГБ, DDR4, 3600 МГц",
        ["design", "video"],
        [
            ("Тип памяти", "DDR4", "DDR4"),
            ("Объём памяти", "32 ГБ (2×16)", "32 ГБ"),
            ("Частота памяти", "3600 МГц", "3600 МГц"),
        ],
    ),
    (
        "ram-crucial-8gb-ddr4-2666", "Оперативная память Crucial 8 ГБ DDR4 2666", "ram", "Crucial",
        2100, None, "new", "pickup", "Пожизненная", False, False,
        "8 ГБ, DDR4, 2666 МГц — для офисных ПК",
        ["office", "study"],
        [
            ("Тип памяти", "DDR4", "DDR4"),
            ("Объём памяти", "8 ГБ", "8 ГБ"),
            ("Частота памяти", "2666 МГц", "2666 МГц"),
        ],
    ),
    (
        "ram-kingston-fury-renegade-32gb-ddr5-6000", "Оперативная память Kingston Fury Renegade 32 ГБ DDR5 6000", "ram", "Kingston",
        14900, None, "new", "pickup", "Пожизненная", True, False,
        "2×16 ГБ, DDR5, 6000 МГц, RGB",
        ["games", "video"],
        [
            ("Тип памяти", "DDR5", "DDR5"),
            ("Объём памяти", "32 ГБ (2×16)", "32 ГБ"),
            ("Частота памяти", "6000 МГц", "6000 МГц"),
        ],
    ),
    # --- Видеокарты -----------------------------------------------------
    (
        "gpu-msi-rtx-4060-ventus-2x", "Видеокарта MSI GeForce RTX 4060 Ventus 2X", "gpu", "MSI",
        44900, None, "new", "pickup", "36 месяцев", True, True,
        "8 ГБ GDDR6, DLSS 3, два вентилятора",
        ["games", "design"],
        [
            ("Видеокарта", "GeForce RTX 4060 Ventus 2X", "RTX 4060"),
            ("Производитель видеокарты", "NVIDIA GeForce", "NVIDIA GeForce"),
            ("Объём видеопамяти", "8 ГБ", "8 ГБ"),
            ("Порты и интерфейсы", "3× DisplayPort 1.4, HDMI 2.1", None),
        ],
    ),
    (
        "gpu-gigabyte-radeon-rx-7600", "Видеокарта Gigabyte Radeon RX 7600 Gaming OC", "gpu", "Gigabyte",
        38900, None, "new", "pickup", "36 месяцев", False, False,
        "8 ГБ GDDR6, FSR 3, заводской разгон",
        ["games"],
        [
            ("Видеокарта", "Radeon RX 7600 Gaming OC", "RX 7600"),
            ("Производитель видеокарты", "AMD Radeon", "AMD Radeon"),
            ("Объём видеопамяти", "8 ГБ", "8 ГБ"),
            ("Порты и интерфейсы", "2× DisplayPort 2.1, HDMI 2.1", None),
        ],
    ),
    # --- Процессоры -----------------------------------------------------
    (
        "cpu-amd-ryzen-5-7600", "Процессор AMD Ryzen 5 7600", "cpu", "AMD",
        22900, None, "new", "pickup", "36 месяцев", False, False,
        "6 ядер / 12 потоков, AM5, до 5.1 ГГц",
        ["games", "programming"],
        [
            ("Процессор", "AMD Ryzen 5 7600", "AMD Ryzen 5"),
            ("Количество ядер", "6 ядер", "6 ядер"),
            ("Охлаждение", "Wraith Stealth в комплекте", None),
        ],
    ),
    (
        "cpu-intel-core-i5-13400f", "Процессор Intel Core i5-13400F", "cpu", "Intel",
        19900, None, "new", "pickup", "36 месяцев", False, False,
        "10 ядер / 16 потоков, LGA1700, до 4.6 ГГц",
        ["games", "office"],
        [
            ("Процессор", "Intel Core i5-13400F", "Intel Core i5"),
            ("Количество ядер", "10 ядер", "10 ядер"),
            ("Охлаждение", "Box-кулер в комплекте", None),
        ],
    ),
    # --- Накопители -----------------------------------------------------
    (
        "ssd-samsung-980-1tb", "SSD Samsung 980 1 ТБ NVMe", "storage", "Samsung",
        7900, None, "new", "pickup", "60 месяцев", False, False,
        "1 ТБ, NVMe, M.2 2280, до 3500 МБ/с",
        ["programming", "video"],
        [
            ("Тип накопителя", "SSD", "SSD"),
            ("Объём накопителя", "1 ТБ", "1 ТБ"),
            ("Интерфейс", "NVMe", "NVMe"),
        ],
    ),
    (
        "ssd-kingston-a400-480gb", "SSD Kingston A400 480 ГБ SATA", "storage", "Kingston",
        3200, None, "new", "pickup", "36 месяцев", False, False,
        "480 ГБ, SATA 3, 2.5\" — быстрый апгрейд ноутбука",
        ["office", "study"],
        [
            ("Тип накопителя", "SSD", "SSD"),
            ("Объём накопителя", "480 ГБ", "480 ГБ"),
            ("Интерфейс", "SATA", "SATA"),
        ],
    ),
    (
        "ssd-crucial-p3-plus-2tb", "SSD Crucial P3 Plus 2 ТБ NVMe", "storage", "Crucial",
        12900, None, "new", "pickup", "60 месяцев", True, False,
        "2 ТБ, NVMe, PCIe 4.0, до 5000 МБ/с",
        ["games", "video"],
        [
            ("Тип накопителя", "SSD", "SSD"),
            ("Объём накопителя", "2 ТБ", "2 ТБ"),
            ("Интерфейс", "NVMe", "NVMe"),
        ],
    ),
    # --- Материнские платы ----------------------------------------------
    (
        "mb-asus-prime-b650m-a", "Материнская плата ASUS PRIME B650M-A", "motherboards", "ASUS",
        14900, None, "new", "pickup", "36 месяцев", False, False,
        "AM5, mATX, DDR5, PCIe 4.0, HDMI + DisplayPort",
        ["programming", "games"],
        [
            ("Сокет", "AM5", "AM5"),
            ("Форм-фактор", "mATX", "mATX"),
            ("Тип памяти", "DDR5", "DDR5"),
            ("Порты и интерфейсы", "HDMI, DisplayPort, 4× SATA, M.2", None),
        ],
    ),
    (
        "mb-msi-b550m-pro-vdh", "Материнская плата MSI B550M PRO-VDH", "motherboards", "MSI",
        8900, None, "new", "pickup", "36 месяцев", False, False,
        "AM4, mATX, DDR4, PCIe 4.0",
        ["office", "study"],
        [
            ("Сокет", "AM4", "AM4"),
            ("Форм-фактор", "mATX", "mATX"),
            ("Тип памяти", "DDR4", "DDR4"),
            ("Порты и интерфейсы", "HDMI, VGA, DVI, M.2", None),
        ],
    ),
    # --- Корпуса --------------------------------------------------------
    (
        "case-deepcool-cc560", "Корпус DeepCool CC560", "cases", "DeepCool",
        4900, None, "new", "pickup", "12 месяцев", False, False,
        "ATX, 4 вентилятора, закалённое стекло",
        ["games", "office"],
        [
            ("Форм-фактор", "ATX", "ATX"),
            ("Цвет", "Чёрный", "Чёрный"),
        ],
    ),
    (
        "case-zalman-i3-neo-white", "Корпус Zalman i3 Neo White", "cases", "Zalman",
        5400, None, "new", "pickup", "12 месяцев", False, False,
        "ATX, белый, 4 ARGB-вентилятора",
        ["games", "design"],
        [
            ("Форм-фактор", "ATX", "ATX"),
            ("Цвет", "Белый", "Белый"),
        ],
    ),
    # --- Комплект для сборки --------------------------------------------
    (
        "build-kit-cyber-start", "Комплект для сборки CYBER Start", "build-kits", "CYBER",
        42900, 45900, "new", "free", "12 месяцев", True, False,
        "Ryzen 5, 16 ГБ DDR4, SSD 512 ГБ, корпус и блок питания",
        ["games", "office", "study"],
        [
            ("Процессор", "AMD Ryzen 5 5600", "AMD Ryzen 5"),
            ("Количество ядер", "6 ядер", "6 ядер"),
            ("Оперативная память", "16 ГБ", "16 ГБ"),
            ("Тип накопителя", "SSD", "SSD"),
            ("Накопитель", "512 ГБ SSD", None),
        ],
    ),
]


class Command(BaseCommand):
    help = "Создаёт демонстрационные товары в пустых разделах каталога (идемпотентно)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить все товары с отметкой «Демо-данные» и выйти.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["clear"]:
            products = Product.objects.filter(is_demo=True)
            total = products.count()
            products.delete()
            self.stdout.write(self.style.WARNING(f"Удалено демо-товаров: {total}"))
            return

        categories = {category.slug: category for category in Category.objects.all()}
        spec_types = {spec_type.name: spec_type for spec_type in SpecType.objects.all()}
        use_cases = {use_case.slug: use_case for use_case in UseCase.objects.all()}

        for slug, name in BRANDS:
            Brand.objects.get_or_create(slug=slug, defaults={"name": name})

        options_created = 0
        for type_name, names in EXTRA_OPTIONS.items():
            spec_type = spec_types.get(type_name)
            if not spec_type:
                continue
            for name in names:
                _, created = SpecOption.objects.get_or_create(spec_type=spec_type, name=name)
                options_created += int(created)

        filters_created = 0
        for category_slug, type_names in EXTRA_FILTERS.items():
            category = categories.get(category_slug)
            if not category:
                continue
            next_order = (category.filters.aggregate(Max("order"))["order__max"] or 0) + 1
            for type_name in type_names:
                spec_type = spec_types.get(type_name)
                if not spec_type:
                    continue
                _, created = CategoryFilter.objects.get_or_create(
                    category=category,
                    source=CategoryFilter.Source.SPEC,
                    spec_type=spec_type,
                    defaults={"order": next_order, "is_active": True},
                )
                if created:
                    next_order += 1
                    filters_created += 1

        brands = {brand.slug: brand for brand in Brand.objects.all()}
        created_products = updated_products = skipped = 0

        for row in PRODUCTS:
            (
                slug, title, category_slug, brand_slug, price, old_price, condition,
                delivery, warranty, installment, featured, short, use_case_slugs, specs,
            ) = row

            category = categories.get(category_slug)
            if not category:
                skipped += 1
                self.stdout.write(self.style.WARNING(f"Пропуск «{title}»: нет категории {category_slug}"))
                continue

            product, created = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "category": category,
                    "brand": brands.get(brand_slug.lower()),
                    "price": price,
                    "old_price": old_price,
                    "status": Product.Status.IN_STOCK,
                    "condition": condition,
                    "delivery": delivery,
                    "location": "Бишкек",
                    "warranty": warranty,
                    "installment_available": installment,
                    "short_description": short,
                    "description": (
                        f"{title} — демонстрационный товар для проверки каталога, фильтров "
                        f"и карточки. Характеристики заполнены из справочника раздела "
                        f"«{category.name}»."
                    ),
                    "is_published": True,
                    "is_featured": featured,
                    "is_demo": True,
                },
            )
            product.use_cases.set(
                [use_cases[slug_] for slug_ in use_case_slugs if slug_ in use_cases]
            )

            product.specs.all().delete()
            for order, (type_name, value, option_name) in enumerate(specs):
                spec_type = spec_types.get(type_name)
                if not spec_type:
                    continue
                option = None
                if option_name:
                    option = SpecOption.objects.filter(
                        spec_type=spec_type, name=option_name
                    ).first()
                ProductSpec.objects.create(
                    product=product,
                    spec_type=spec_type,
                    option=option,
                    value=value,
                    order=order,
                )

            created_products += int(created)
            updated_products += int(not created)

        total_demo = Product.objects.filter(is_demo=True).count()
        self.stdout.write(self.style.SUCCESS(
            f"Готово: создано товаров {created_products}, обновлено {updated_products}, "
            f"пропущено {skipped}. Новых значений справочника: {options_created}, "
            f"новых фильтров разделов: {filters_created}. Всего демо-товаров: {total_demo}."
        ))
