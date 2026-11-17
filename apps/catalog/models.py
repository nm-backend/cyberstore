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


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Адрес (slug)", unique=True, max_length=120)
    parent = models.ForeignKey(
        "self", verbose_name="Родительская категория", null=True, blank=True,
        on_delete=models.CASCADE, related_name="children",
        help_text="Например: «Видеокарты» внутри «Комплектующие». Для основных разделов оставьте пустым.",
    )
    icon = models.CharField("Иконка (эмодзи)", max_length=8, blank=True)
    description = models.CharField("Короткое описание", max_length=200, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.parent.name} / {self.name}" if self.parent_id else self.name

    def get_absolute_url(self):
        return reverse("catalog:category", args=[self.slug])


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
    icon = models.CharField("Иконка (эмодзи)", max_length=8, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Для чего подходит"
        verbose_name_plural = "Для чего подходит"

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
    installment_available = models.BooleanField("Можно в рассрочку", default=True)
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
    def discount_percent(self):
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
    order = models.PositiveSmallIntegerField("Порядок", default=0, help_text="Первые 4 строки видны в карточке товара.")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return f"{self.spec_type.name}: {self.value}"
