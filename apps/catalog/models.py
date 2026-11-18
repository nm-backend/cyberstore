from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


_TRANSLIT = dict(zip(
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюяңөү",
    ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r",
     "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "yu", "ya", "n", "o", "u"],
))


def translit(text):
    return "".join(_TRANSLIT.get(ch, ch) for ch in text.lower())


def make_unique_slug(model, base, max_length=200):
    base = (slugify(translit(base)) or "product")[: max_length - 8]
    slug, counter = base, 2
    while model.objects.filter(slug=slug).exists():
        slug = f"{base}-{counter}"
        counter += 1
    return slug


class IconKey(models.TextChoices):
    """Keys of the stroke icons available in the storefront sprite (base.html)."""

    LAPTOP = "laptop", "Ноутбук"
    DESKTOP = "desktop", "Монитор / ПК"
    CHIP = "chip", "Комплектующие"
    GAMEPAD = "gamepad", "Игры"
    BOOK = "book", "Учёба"
    BRIEFCASE = "briefcase", "Офис и работа"
    PALETTE = "palette", "Дизайн и графика"
    FILM = "film", "Видео"
    CODE = "code", "Код и разработка"
    CART = "cart", "Корзина"
    GRID = "grid", "Папка"
    TAG = "tag", "Тег"
    CARD = "card", "Рассрочка"
    TRUCK = "truck", "Доставка"
    SHIELD = "shield", "Гарантия"
    STORE = "store", "Магазин"
    PIN = "pin", "Адрес"
    CLOCK = "clock", "Часы работы"
    PHONE = "phone", "Телефон"


class Category(models.Model):
    class DisplayMode(models.TextChoices):
        TILES = "tiles", "Плитки подразделов"
        PRODUCTS = "products", "Товары с фильтром"
        BOTH = "both", "И плитки, и товары"

    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Адрес (slug)", unique=True, max_length=120)
    parent = models.ForeignKey(
        "self", verbose_name="Родительская категория", null=True, blank=True,
        on_delete=models.CASCADE, related_name="children",
        help_text="Например: «Видеокарты» внутри «Комплектующие». Для основных разделов оставьте пустым.",
    )
    icon = models.CharField(
        "Иконка", max_length=20, blank=True, choices=IconKey.choices,
        help_text="Значок на плитке раздела. Пусто — покажем папку.",
    )
    image = models.ImageField(
        "Картинка для плитки", upload_to="categories/", blank=True,
        help_text="Необязательно. Без картинки на плитке будет иконка или аккуратная заглушка.",
    )
    description = models.CharField("Короткое описание", max_length=200, blank=True)
    display_mode = models.CharField(
        "Что показывать", max_length=10, choices=DisplayMode.choices, default=DisplayMode.BOTH,
        help_text="«Плитки подразделов» — только дочерние разделы. «Товары с фильтром» — сразу товары. «И плитки, и товары» — сначала подразделы, ниже товары.",
    )
    quick_links_title = models.CharField(
        "Заголовок быстрых ссылок", max_length=100, blank=True,
        help_text="Например: «ПК для любых задач». Пусто — блок быстрых ссылок не показывается.",
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.parent.name} / {self.name}" if self.parent_id else self.name

    def clean(self):
        node = self.parent
        while node:
            if node.pk == self.pk:
                raise ValidationError({"parent": "Нельзя вложить категорию в саму себя или в её подраздел."})
            node = node.parent

    def get_absolute_url(self):
        return reverse("catalog:category", args=[self.slug])

    def descendant_ids(self):
        """Own pk plus all nested subcategory pks, for product lookups."""
        ids, frontier = [self.pk], [self.pk]
        while frontier:
            frontier = list(
                Category.objects.filter(parent_id__in=frontier).values_list("pk", flat=True)
            )
            ids.extend(frontier)
        return ids


class Brand(models.Model):
    name = models.CharField("Название", max_length=80, unique=True)
    slug = models.SlugField("Адрес (slug)", unique=True, max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class UseCase(models.Model):
    """The «Подходит для» tags from the store's Instagram cards."""

    name = models.CharField("Название", max_length=60, unique=True)
    slug = models.SlugField("Адрес (slug)", unique=True, max_length=80)
    icon = models.CharField(
        "Иконка", max_length=20, blank=True, choices=IconKey.choices,
        help_text="Значок на плитке назначения. Пусто — покажем тег.",
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Назначение"
        verbose_name_plural = "Назначение"

    def __str__(self):
        return self.name


class SpecType(models.Model):
    """Dictionary of characteristic names: Процессор, Видеокарта, ОЗУ, ..."""

    name = models.CharField("Название характеристики", max_length=80, unique=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Тип характеристики"
        verbose_name_plural = "Типы характеристик"

    def __str__(self):
        return self.name


class CategoryFilter(models.Model):
    """One filter block on a category page. Subcategories inherit the nearest parent's rows."""

    class Source(models.TextChoices):
        PRICE = "price", "Цена"
        BRAND = "brand", "Бренд"
        SPEC = "spec", "Характеристика"
        USE_CASE = "use_case", "Назначение"
        INSTALLMENT = "installment", "Рассрочка"
        DELIVERY = "delivery", "Доставка"
        CONDITION = "condition", "Состояние"
        LOCATION = "location", "Местоположение"
        STOCK = "stock", "Наличие"

    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="filters")
    source = models.CharField("Источник", max_length=20, choices=Source.choices, default=Source.SPEC)
    spec_type = models.ForeignKey(
        SpecType, verbose_name="Характеристика", null=True, blank=True,
        on_delete=models.CASCADE, related_name="category_filters",
        help_text="Только для источника «Характеристика». Например: Процессор, Оперативная память.",
    )
    title = models.CharField(
        "Название фильтра", max_length=60, blank=True,
        help_text="Пусто — возьмём название источника или характеристики.",
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фильтр раздела"
        verbose_name_plural = "Фильтры раздела"

    def __str__(self):
        return f"{self.category.name}: {self.display_title}"

    def clean(self):
        if self.source == self.Source.SPEC and not self.spec_type:
            raise ValidationError({"spec_type": "Выберите характеристику для этого фильтра."})
        if self.source != self.Source.SPEC and self.spec_type:
            raise ValidationError({"spec_type": "Характеристика нужна только для источника «Характеристика»."})

    @property
    def display_title(self):
        if self.title:
            return self.title
        if self.source == self.Source.SPEC and self.spec_type:
            return self.spec_type.name
        return self.get_source_display()


class CategoryQuickLink(models.Model):
    """Tile above the products that turns on the «Назначение» filter."""

    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="quick_links")
    label = models.CharField("Подпись", max_length=60)
    use_cases = models.ManyToManyField(
        UseCase, verbose_name="Назначение", blank=True,
        help_text="Товары с любым из выбранных назначений. Например: «Игры».",
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Быстрая ссылка"
        verbose_name_plural = "Быстрые ссылки"

    def __str__(self):
        return f"{self.category.name}: {self.label}"

    def url_params(self):
        slugs = ",".join(self.use_cases.values_list("slug", flat=True))
        return f"use_case={slugs}" if slugs else ""


class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True, category__is_active=True)

    def with_cards(self):
        return self.select_related("category", "brand").prefetch_related(
            "images", "specs__spec_type"
        )


class Product(models.Model):
    class Status(models.TextChoices):
        IN_STOCK = "in_stock", "В наличии"
        PREORDER = "preorder", "Под заказ"
        OUT_OF_STOCK = "out", "Нет в наличии"

    class Condition(models.TextChoices):
        UNSET = "", "Не указано"
        NEW = "new", "Новый"
        USED = "used", "Б/у"

    class Delivery(models.TextChoices):
        UNSET = "", "Не указано"
        FREE = "free", "Бесплатная"
        PAID = "paid", "Платная"
        PICKUP = "pickup", "Самовывоз"

    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.PROTECT, related_name="products"
    )
    brand = models.ForeignKey(
        Brand, verbose_name="Бренд", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="products",
    )
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField("Адрес (slug)", unique=True, blank=True, max_length=220)
    short_description = models.CharField(
        "Короткое описание", max_length=220, blank=True, help_text="Одна строка под названием в карточке."
    )
    description = models.TextField("Полное описание", blank=True)

    price = models.PositiveIntegerField(
        "Цена, сом", null=True, blank=True, help_text="Пусто — на сайте будет «Цена по запросу»."
    )
    old_price = models.PositiveIntegerField(
        "Старая цена, сом", null=True, blank=True, help_text="Если заполнить, покажем скидку."
    )
    status = models.CharField("Наличие", max_length=10, choices=Status.choices, default=Status.IN_STOCK)
    installment_available = models.BooleanField(
        "Можно в рассрочку", default=False,
        help_text="Ставьте галочку, только если рассрочка действительно доступна для этого товара.",
    )
    condition = models.CharField(
        "Состояние", max_length=10, choices=Condition.choices, blank=True, default="",
        help_text="Новый или Б/у. Пусто — фильтр и карточка не показывают состояние.",
    )
    delivery = models.CharField(
        "Доставка", max_length=10, choices=Delivery.choices, blank=True, default="",
        help_text="Как доставляется именно этот товар. Пусто — не показываем.",
    )
    location = models.CharField(
        "Местоположение", max_length=80, blank=True,
        help_text="Город, например «Бишкек». Пусто — не показываем.",
    )
    warranty = models.CharField("Гарантия", max_length=100, blank=True, help_text="Например: 12 месяцев. Пусто — не показываем.")

    use_cases = models.ManyToManyField(UseCase, verbose_name="Подходит для", blank=True, related_name="products")

    is_published = models.BooleanField("Показывать на сайте", default=True)
    is_featured = models.BooleanField("Показывать на главной", default=False)
    is_demo = models.BooleanField(
        "Демо-данные", default=False, help_text="Отметка для примеров. Фильтром «Демо-данные» их легко найти и удалить."
    )

    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Изменён", auto_now=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = make_unique_slug(Product, self.title, 220)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:detail", args=[self.slug])

    @property
    def is_available(self):
        return self.status != self.Status.OUT_OF_STOCK

    @property
    def main_image(self):
        images = list(self.images.all())
        return images[0] if images else None

    @property
    def card_specs(self):
        return list(self.specs.all())[:4]

    @property
    def discount_percent(self) -> int:
        if self.price and self.old_price and self.old_price > self.price:
            return round((1 - self.price / self.old_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Фото", upload_to="products/")
    alt = models.CharField("Подпись", max_length=150, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0, help_text="Первое фото — главное.")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return f"{self.product.title} — фото {self.pk}"


class ProductSpec(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specs")
    spec_type = models.ForeignKey(SpecType, verbose_name="Характеристика", on_delete=models.PROTECT)
    value = models.CharField("Значение", max_length=200)
    filter_value = models.CharField(
        "Значение для фильтра", max_length=200, blank=True,
        help_text="Необязательно. Короткое общее значение, чтобы «16 ГБ» и «16GB» не дублировались. Пусто — берётся значение выше.",
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0, help_text="Первые 4 строки видны в карточке товара.")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return f"{self.spec_type.name}: {self.value}"
