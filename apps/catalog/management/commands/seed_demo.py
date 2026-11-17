import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.catalog.models import (
    Brand, Category, Product, ProductImage, ProductSpec, SpecType, UseCase,
)

DEMO_PRODUCTS = [
    # --- НОУТБУКИ (из Instagram + хиты) ---
    dict(
        title="Dell Alienware M16 — мощный игровой ноутбук",
        category="laptops",
        brand="Dell",
        short="Премиальный игровой ноутбук с мощным охлаждением и экраном 165Hz",
        price=113000,
        old_price=125000,
        featured=True,
        demo=False,
        image_name="dell-alienware.jpg",
        warranty="12 месяцев",
        use=["games", "video", "design", "programming"],
        specs=[
            ("Процессор", "Intel Core 7 (14 ядер / 20 потоков, до 5.0 ГГц)"),
            ("Видеокарта", "NVIDIA GeForce RTX 4050 6GB GDDR6"),
            ("Оперативная память", "16 ГБ DDR5 4800 МГц"),
            ("Накопитель", "SSD 512 ГБ NVMe M.2 PCIe"),
            ("Экран", "16\" QHD+ (2560x1600) 165Hz IPS 100% sRGB"),
            ("Операционная система", "Windows 11 Home Лицензия"),
            ("Охлаждение", "Alienware Cryo-Tech с испарительной камерой"),
            ("Вес", "2.6 кг"),
        ],
        desc="Флагманский игровой ноутбук Dell Alienware в металлическом корпусе Dark Metallic Moon. Оснащён инновационной системой охлаждения Alienware Cryo-Tech, полноразмерной RGB-клавиатурой с индивидуальной подсветкой каждой клавиши и экраном высокого разрешения 165 Гц. Идеален для Cyberpunk 2077, GTA V, CS2, а также видеомонтажа в 4K и работы с 3D-графикой.",
    ),
    dict(
        title="HP OMEN 16 — мощный игровой ноутбук премиум-класса",
        category="laptops",
        brand="HP",
        short="Для игр, стримов, разработки и тяжёлых профессиональных задач",
        price=150000,
        old_price=162000,
        featured=True,
        demo=False,
        image_name="hp-omen-16.jpg",
        warranty="12 месяцев",
        use=["games", "programming", "design", "video"],
        specs=[
            ("Процессор", "Intel Core Ultra 7 255H (16 ядер / 16 потоков, AI Boost)"),
            ("Видеокарта", "NVIDIA GeForce RTX 5070 8GB GDDR7"),
            ("Оперативная память", "24 ГБ DDR5 5600 МГц"),
            ("Накопитель", "SSD 1 ТБ M.2 NVMe PCIe 4.0"),
            ("Экран", "16\" 2K QHD (2560x1440) 240Hz IPS"),
            ("Операционная система", "Windows 11 Pro"),
            ("Охлаждение", "OMEN Tempest Cooling с тремя теплотрубками"),
            ("Вес", "2.35 кг"),
        ],
        desc="Новейший ноутбук HP OMEN 16 на базе процессора Intel Core Ultra с поддержкой искусственного интеллекта. Экран с частотой обновления 240 Гц даёт безупречную плавность в любых киберспортивных дисциплинах. Отличный выбор для геймеров, разработчиков и контент-мейкеров.",
    ),
    dict(
        title="Acer Extensa 15",
        category="laptops",
        brand="Acer",
        short="Мощный и надёжный ноутбук для работы, учёбы и бизнеса",
        price=38500,
        old_price=42000,
        featured=True,
        demo=False,
        image_name="acer-extensa-15.jpg",
        warranty="12 месяцев",
        use=["study", "office", "programming"],
        specs=[
            ("Процессор", "AMD Ryzen 7 7730U (8 ядер / 16 потоков, до 4.5 ГГц)"),
            ("Оперативная память", "16 ГБ DDR4 3200 МГц"),
            ("Накопитель", "SSD 512 ГБ NVMe PCIe"),
            ("Экран", "15.6\" Full HD (1920x1080) IPS матовый"),
            ("Операционная система", "Windows 11"),
            ("Аккумулятор", "До 8.5 часов автономной работы"),
            ("Вес", "1.78 кг"),
        ],
        desc="Надёжный помощник на каждый день в лёгком корпусе. 8-ядерный процессор Ryzen 7 легко справляется с десятками открытых вкладок, тяжёлыми таблицами, базами данных и программированием. Качественный IPS-дисплей не утомляет глаза при долгой работе.",
    ),
    dict(
        title="HP Laptop 15",
        category="laptops",
        brand="HP",
        short="Удобный ноутбук для учёбы, работы и интернет-серфинга",
        price=29500,
        old_price=None,
        featured=False,
        demo=False,
        image_name="hp-laptop-15.jpg",
        warranty="12 месяцев",
        use=["study", "office"],
        specs=[
            ("Процессор", "Intel Core i3-N305 (8 ядер / 8 потоков, до 3.8 ГГц)"),
            ("Оперативная память", "8 ГБ DDR4"),
            ("Накопитель", "SSD 256 ГБ NVMe M.2"),
            ("Экран", "15.6\" Full HD (1920x1080)"),
            ("Вес", "1.65 кг"),
        ],
        desc="Доступный и качественный ноутбук от известного бренда HP. Оснащён современным 8-ядерным процессором Intel с высокой энергоэффективностью и быстрым SSD накопителем. Идеален для школьников, студентов и офисной работы.",
    ),
    dict(
        title="ASUS TUF Gaming A15",
        category="laptops",
        brand="ASUS",
        short="Надёжный военный стандарт прочности и отличная игровая производительность",
        price=74000,
        old_price=79000,
        featured=True,
        demo=False,
        image_name="asus-tuf-gaming.jpg",
        warranty="12 месяцев",
        use=["games", "video", "programming"],
        specs=[
            ("Процессор", "AMD Ryzen 7 7735HS (8 ядер / 16 потоков, до 4.75 ГГц)"),
            ("Видеокарта", "NVIDIA GeForce RTX 4060 8GB GDDR6 (140W TGP)"),
            ("Оперативная память", "16 ГБ DDR5 4800 МГц"),
            ("Накопитель", "SSD 512 ГБ PCIe 4.0 NVMe"),
            ("Экран", "15.6\" Full HD 144Hz IPS 100% sRGB"),
            ("Операционная система", "Windows 11"),
            ("Вес", "2.2 кг"),
        ],
        desc="Полноценная RTX 4060 с теплопакетом 140 Вт обеспечивает максимальный FPS в современных играх. Корпус сертифицирован по стандарту MIL-STD-810H на устойчивость к вибрациям, падениям и перепадам температур.",
    ),

    # --- ГОТОВЫЕ КОМПЬЮТЕРЫ / СБОРКИ ПК ---
    dict(
        title="Игровой ПК Cyber Phantom RTX 4060",
        category="pc",
        brand="CyberStore",
        short="Сбалансированная игровая сборка для ультра-настроек в Full HD и 2K",
        price=89500,
        old_price=96000,
        featured=True,
        demo=False,
        image_name="pc-gaming-pro.jpg",
        warranty="12 месяцев",
        use=["games", "video", "design", "programming"],
        specs=[
            ("Процессор", "Intel Core i5-13400F (10 ядер / 16 потоков, до 4.6 ГГц)"),
            ("Видеокарта", "NVIDIA GeForce RTX 4060 8GB GDDR6 Dual Fan"),
            ("Оперативная память", "32 ГБ DDR4 3200 МГц Kingston Fury (2x16 dual)"),
            ("Накопитель", "1 ТБ M.2 NVMe PCIe SSD (чтение 3500 МБ/с)"),
            ("Материнская плата", "MSI PRO B760M-A WiFi DDR4"),
            ("Охлаждение", "Башенный кулер DeepCool AG400 ARGB"),
            ("Блок питания", "DeepCool PK650D 650W 80+ Bronze"),
            ("Корпус", "DeepCool CC560 V2 ARGB с закаленным стеклом"),
            ("Операционная система", "Windows 11 Pro 64-bit активированная"),
        ],
        desc="Готовый игровой системный блок от магазина CyberStore. Собран профессиональными инженерами, аккуратный кабель-менеджмент, стресс-тесты пройдены без перегрева. Включил и играй! Тянет все современные хиты (Cyberpunk 2077, Warzone, CS2, RDR2, Dota 2) на ультра-настройках.",
    ),
    dict(
        title="Игровой ПК Cyber Beast RTX 4070 Ti Super",
        category="pc",
        brand="CyberStore",
        short="Ультимативная белая сборка с водяным охлаждением для 4K гейминга и стримов",
        price=168000,
        old_price=179000,
        featured=True,
        demo=False,
        image_name="pc-beast-white.jpg",
        warranty="24 месяца",
        use=["games", "video", "design"],
        specs=[
            ("Процессор", "AMD Ryzen 7 7800X3D (8 ядер / 16 потоков, 96MB 3D V-Cache)"),
            ("Видеокарта", "NVIDIA GeForce RTX 4070 Ti Super 16GB GDDR6X"),
            ("Оперативная память", "32 ГБ DDR5 6000 МГц G.Skill Trident Z5 RGB (2x16)"),
            ("Накопитель", "2 ТБ Samsung 980 Pro PCIe 4.0 NVMe M.2"),
            ("Материнская плата", "ASUS TUF GAMING B650-PLUS WIFI AM5"),
            ("Охлаждение", "СЖО 360мм DeepCool LT720 White ARGB"),
            ("Блок питания", "Seasonic Focus GX-850 850W 80+ Gold Modular"),
            ("Корпус", "LIAN LI O11 Dynamic EVO White со стеклянными панелями"),
            ("Операционная система", "Windows 11 Pro"),
        ],
        desc="Мечта любого геймера и создателя контента: лучший игровой процессор в мире AMD Ryzen 7 7800X3D с технологией 3D V-Cache в паре с мощной видеокартой RTX 4070 Ti Super на 16 ГБ видеопамяти. Роскошный белоснежный дизайн, бесшумное водяное охлаждение и максимальный FPS в любом разрешении вплоть до 4K.",
    ),
    dict(
        title="ПК Cyber Strike — киберспорт и работа",
        category="pc",
        brand="CyberStore",
        short="Оптимальная сборка для киберспортивных дисциплин, учёбы и видеомонтажа",
        price=54000,
        old_price=59000,
        featured=False,
        demo=False,
        image_name="pc-cyber-strike.jpg",
        warranty="12 месяцев",
        use=["games", "study", "office", "programming"],
        specs=[
            ("Процессор", "AMD Ryzen 5 5600 (6 ядер / 12 потоков, до 4.4 ГГц)"),
            ("Видеокарта", "NVIDIA GeForce RTX 3060 12GB GDDR6"),
            ("Оперативная память", "16 ГБ DDR4 3200 МГц (2x8GB)"),
            ("Накопитель", "SSD 512 ГБ M.2 NVMe"),
            ("Материнская плата", "Gigabyte B550M DS3H"),
            ("Охлаждение", "ID-COOLING SE-214-XT ARGB"),
            ("Блок питания", "600W 80+ Bronze"),
            ("Корпус", "1stPlayer Trilobite T3 со стеклом"),
            ("Операционная система", "Windows 11 Pro"),
        ],
        desc="Народный хит продаж! 12 ГБ видеопамяти видеокарты RTX 3060 гарантируют запас производительности на годы вперёд. CS2 выдаёт 250+ FPS, Dota 2, GTA V и другие популярные игры работают безупречно.",
    ),
    dict(
        title="Офисный ПК Cyber Office Pro",
        category="pc",
        brand="CyberStore",
        short="Компактный и тихий системный блок для офиса, бухгалтерии (1C) и учёбы",
        price=28900,
        old_price=None,
        featured=False,
        demo=False,
        image_name="pc-cyber-office.jpg",
        warranty="12 месяцев",
        use=["office", "study"],
        specs=[
            ("Процессор", "Intel Core i3-12100 (4 ядра / 8 потоков, до 4.3 ГГц)"),
            ("Видеокарта", "Встроенная Intel UHD Graphics 730"),
            ("Оперативная память", "16 ГБ DDR4 3200 МГц"),
            ("Накопитель", "SSD 512 ГБ NVMe M.2"),
            ("Материнская плата", "ASUS PRIME H610M-K D4"),
            ("Блок питания", "450W FSP"),
            ("Корпус", "Prime Box Black компактный Micro-ATX"),
            ("Операционная система", "Windows 11 Pro"),
        ],
        desc="Быстрый, тихий и надёжный компьютер для работы с документами, 1С Предприятие, браузером на 50 вкладок и офисными приложениями. Мгновенная загрузка системы за 7 секунд благодаря скоростному NVMe диску.",
    ),

    # --- КОМПЛЕКТУЮЩИЕ ---
    dict(
        title="Видеокарта Palit GeForce RTX 4070 Dual 12GB",
        category="components",
        brand="Palit",
        short="12GB GDDR6X, поддержка DLSS 3, трассировка лучей и тихий кулер",
        price=56000,
        old_price=61000,
        featured=True,
        demo=False,
        image_name="rtx-4070-dual.jpg",
        warranty="24 месяца",
        use=["games", "video", "design"],
        specs=[
            ("Видеокарта", "NVIDIA GeForce RTX 4070 12GB GDDR6X"),
            ("Порты и интерфейсы", "3x DisplayPort 1.4a, 1x HDMI 2.1a"),
            ("Блок питания", "Рекомендуемый БП от 650 Вт"),
            ("Охлаждение", "Два вентилятора 95 мм с технологией 0-dB"),
        ],
        desc="Современная видеокарта на архитектуре NVIDIA Ada Lovelace. Поддержка генерации кадров DLSS 3 удваивает плавность в играх. 12 ГБ быстрой памяти GDDR6X позволяют играть на ультра-настройках в 2K разрешении.",
    ),
    dict(
        title="SSD накопитель Kingston KC3000 1TB M.2 PCIe 4.0",
        category="components",
        brand="Kingston",
        short="Скорость чтения до 7000 МБ/с, графеновый радиатор, память 3D TLC",
        price=8900,
        old_price=9800,
        featured=False,
        demo=False,
        image_name="ssd-kingston-kc3000.jpg",
        warranty="36 месяцев",
        use=["games", "video", "programming"],
        specs=[
            ("Накопитель", "1024 ГБ M.2 NVMe PCIe 4.0 x4"),
            ("Процессор", "Контроллер Phison E18"),
        ],
        desc="Один из быстрейших твердотельных накопителей PCIe 4.0 на рынке. Скорость чтения до 7000 МБ/с, ресурс записи 800 TBW. Игры и тяжелые проекты монтируются и загружаются мгновенно.",
    ),
    dict(
        title="Процессор AMD Ryzen 7 7800X3D AM5 OEM",
        category="components",
        brand="AMD",
        short="Король игровых процессоров с 96 МБ 3D V-Cache",
        price=38500,
        old_price=41000,
        featured=False,
        demo=False,
        image_name="cpu-ryzen-7800x3d.jpg",
        warranty="12 месяцев",
        use=["games", "video"],
        specs=[
            ("Процессор", "AMD Ryzen 7 7800X3D (8 ядер / 16 потоков, до 5.0 ГГц)"),
        ],
        desc="Лучший игровой процессор в мире для сокета AM5. Огромный кэш L3 96 МБ обеспечивает стабильный и высокий FPS даже в самых процессорозависимых играх (Tarkov, Rust, MSFS 2024, CS2, Cyberpunk).",
    ),
]


class Command(BaseCommand):
    help = "Fill the catalog with realistic products, laptops, PC builds, and components."

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Delete products and exit.")

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Product.objects.all().delete()
            self.stdout.write(f"Deleted all products: {deleted}")
            return

        # Pre-create all necessary SpecTypes
        spec_names = [
            "Процессор", "Видеокарта", "Оперативная память", "Накопитель", "Экран",
            "Операционная система", "Материнская плата", "Блок питания", "Корпус",
            "Охлаждение", "Аккумулятор", "Порты и интерфейсы", "Вес", "Сокет", "Чипсет",
        ]
        spec_dict = {}
        for order, name in enumerate(spec_names, start=1):
            st, _ = SpecType.objects.get_or_create(name=name, defaults={"order": order})
            spec_dict[name] = st

        categories = {c.slug: c for c in Category.objects.all()}
        use_cases = {u.slug: u for u in UseCase.objects.all()}

        # If products already exist and we aren't clearing, update or insert
        media_products_dir = settings.BASE_DIR / "media" / "products"

        for item in DEMO_PRODUCTS:
            brand = None
            if item["brand"]:
                brand, _ = Brand.objects.get_or_create(
                    name=item["brand"], defaults={"slug": item["brand"].lower().replace(" ", "-")}
                )

            category = categories.get(item["category"])
            if not category:
                continue

            product, created = Product.objects.get_or_create(
                title=item["title"],
                defaults=dict(
                    category=category,
                    brand=brand,
                    short_description=item["short"],
                    description=item.get("desc", ""),
                    price=item["price"],
                    old_price=item.get("old_price"),
                    warranty=item.get("warranty", "12 месяцев"),
                    is_featured=item["featured"],
                    is_demo=item["demo"],
                    is_published=True,
                )
            )

            # Update existing if already created
            if not created:
                product.short_description = item["short"]
                product.description = item.get("desc", "")
                product.price = item["price"]
                product.old_price = item.get("old_price")
                product.warranty = item.get("warranty", "12 месяцев")
                product.is_featured = item["featured"]
                product.is_demo = item["demo"]
                product.save()

            product.use_cases.set([use_cases[s] for s in item["use"] if s in use_cases])

            # Specs
            product.specs.all().delete()
            for order, (s_name, s_val) in enumerate(item["specs"]):
                s_type = spec_dict.get(s_name) or SpecType.objects.get_or_create(name=s_name)[0]
                ProductSpec.objects.create(
                    product=product, spec_type=s_type, value=s_val, order=order
                )

            # Image attachment
            image_name = item.get("image_name")
            if image_name:
                local_path = media_products_dir / image_name
                if local_path.exists() and not product.images.exists():
                    ProductImage.objects.create(
                        product=product,
                        image=f"products/{image_name}",
                        alt=product.title,
                        order=0,
                    )

        self.stdout.write(self.style.SUCCESS(f"Catalog populated with {len(DEMO_PRODUCTS)} products!"))
