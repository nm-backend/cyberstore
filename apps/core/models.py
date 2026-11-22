import re
from urllib.parse import quote, quote_plus

from django.core.validators import RegexValidator
from django.db import models

from .storage import video_storage


class SiteSettings(models.Model):
    """Single row with everything the owner may want to change without a developer."""

    shop_name = models.CharField("Название магазина", max_length=100, default="CyberStore")
    tagline = models.CharField(
        "Слоган", max_length=200, default="Ноутбуки, готовые ПК и комплектующие"
    )

    phone = models.CharField("Телефон (как показывать)", max_length=30, default="+996 220 053 059")
    whatsapp_number = models.CharField(
        "Номер WhatsApp",
        max_length=15,
        default="996220053059",
        validators=[RegexValidator(r"^\d{10,15}$", "Только цифры, с кодом страны, без плюса.")],
        help_text="Только цифры с кодом страны, например 996220053059. Сюда уходят все заказы.",
    )
    instagram_url = models.URLField(
        "Instagram", blank=True, default="https://www.instagram.com/cyberstore_nout/"
    )

    city = models.CharField("Город", max_length=60, default="Бишкек")
    address = models.CharField(
        "Адрес", max_length=200, default="Айни 31",
        help_text="Если вы переезжаете, смените адрес здесь (например, «Айни 31»). Адрес, подвал и интерактивная карта обновятся на всём сайте автоматически.",
    )
    address_note = models.CharField(
        "Уточнение к адресу", max_length=100, blank=True, default="",
        help_text="Например: «Цокольный этаж» или «1 этаж, вход с торца». Пусто — не показывается.",
    )
    work_hours = models.CharField(
        "Часы работы", max_length=120, default="09:00 – 22:00, без выходных"
    )
    work_days = models.CharField(
        "Дни работы", max_length=60, default="Ежедневно",
        help_text="Например: «Ежедневно» или «Пн-Сб».",
    )
    telegram_url = models.URLField(
        "Telegram", blank=True, default="",
        help_text="Ссылка на Telegram аккаунт или канал магазина. Пусто — значок не показывается.",
    )
    gis_url = models.URLField(
        "Ссылка на 2GIS", blank=True, default="",
        help_text="Прямая ссылка на филиал в 2GIS. Пусто — кнопка карты не показывается.",
    )

    catalog_title = models.CharField(
        "Название каталога", max_length=80, default="Каталог",
        help_text="Заголовок страницы /catalog/ и ссылки в меню.",
    )
    usd_rate = models.DecimalField(
        "Курс доллара, сом за 1 USD", max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Необязательно. Пока пусто — переключателя KGS/USD на сайте нет. Курс не придумывается автоматически.",
    )

    hero_title = models.CharField(
        "Заголовок на главной",
        max_length=120,
        default="Мощные игровые ПК и ноутбуки в Бишкеке",
    )
    hero_subtitle = models.CharField(
        "Подзаголовок на главной",
        max_length=250,
        blank=True,
        default="",
        help_text="Показывается под главным заголовком на первом экране. Пусто — не показывается.",
    )
    hero_video = models.FileField(
        "Видео на главной", upload_to="hero/", storage=video_storage, blank=True,
        help_text="Необязательно. Короткое видео (лучше до 15 МБ, mp4) на фоне главного экрана.",
    )
    hero_poster = models.ImageField(
        "Заставка видео / фон", upload_to="hero/", blank=True,
        help_text="Показывается, пока грузится видео, и на телефонах с экономией трафика.",
    )

    delivery_text = models.TextField(
        "Текст страницы «Доставка»",
        default=(
            "Бесплатная доставка по Кыргызстану.\n"
            "Сроки и детали доставки уточняйте у менеджера в WhatsApp."
        ),
        help_text="Каждая строка — отдельный абзац.",
    )
    installment_note = models.TextField(
        "Условия рассрочки (общий текст)",
        default=(
            "Нужен только паспорт. Возраст от 18 лет.\n"
            "Точные условия и сроки уточняйте у менеджера в WhatsApp."
        ),
        help_text="Каждая строка — отдельный абзац. Варианты рассрочки добавляются отдельно.",
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        kwargs["force_insert"] = False  # objects.create() must update the existing row, not fail
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # the single settings row must always exist

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def phone_tel(self):
        return re.sub(r"[^\d+]", "", self.phone)

    @property
    def full_address(self):
        return f"{self.address}, {self.city}"

    @property
    def city_prepositional(self):
        """Город в предложном падеже — для фраз вида «Купить в Бишкеке»."""
        known = {
            "бишкек": "Бишкеке",
            "ош": "Оше",
            "джалал-абад": "Джалал-Абаде",
            "каракол": "Караколе",
            "нарын": "Нарыне",
            "талас": "Таласе",
            "баткен": "Баткене",
            "токмок": "Токмоке",
            "кара-балта": "Кара-Балте",
        }
        city = (self.city or "").strip()
        return known.get(city.lower(), city)

    @property
    def hours_without_days(self):
        """Часы работы без уже показанных дней недели.

        Владелец может записать «Ежедневно с 9:00 до 22:00» в оба поля, тогда
        подпись «Ежедневно» повторялась бы. Если часы начинаются с тех же дней,
        что и подпись, лишний префикс убирается; иначе значение не меняется.
        """
        hours = re.sub(r"\s+", " ", self.work_hours or "").strip()
        days = re.sub(r"\s+", " ", self.work_days or "").strip()
        if not hours or not days:
            return hours
        days_pattern = re.escape(days).replace(r"\-", "[-–—]")
        match = re.match(rf"^{days_pattern}\b", hours, flags=re.IGNORECASE)
        if match is None:
            return hours
        tail = hours[match.end():].lstrip(" \t,.:;—-–—")
        return tail or hours

    @property
    def map_search_url(self):
        query = quote_plus(f"{self.full_address}, Кыргызстан")
        return f"https://www.google.com/maps/search/?api=1&query={query}"

    @property
    def map_embed_url(self):
        query = quote_plus(f"{self.full_address}, Кыргызстан")
        return f"https://maps.google.com/maps?q={query}&hl=ru&z=16&output=embed"

    @property
    def delivery_paragraphs(self):
        return [line.strip() for line in self.delivery_text.splitlines() if line.strip()]

    @property
    def installment_paragraphs(self):
        return [line.strip() for line in self.installment_note.splitlines() if line.strip()]

    def whatsapp_url(self, text=""):
        url = f"https://wa.me/{self.whatsapp_number}"
        return f"{url}?text={quote(text, safe='')}" if text else url


class InstallmentOption(models.Model):
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    badge = models.CharField("Пометка", max_length=40, blank=True, help_text="Например: 18+")
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Вариант рассрочки"
        verbose_name_plural = "Варианты рассрочки"

    def __str__(self):
        return self.title

    @property
    def whatsapp_text(self):
        """Сообщение для WhatsApp с уточнением именно этого варианта.

        «Рассрочка с банком» → «…условия рассрочки с банком.»,
        «Рассрочка без банка» → «…условия рассрочки без банка.».
        Если в названии нет уточнения, остаётся общий текст.
        """
        title = re.sub(r"\s+", " ", self.title or "").strip()
        detail = re.sub(r"^рассрочк\w*\s*", "", title, flags=re.IGNORECASE)
        detail = detail.strip(" -–—:,.")
        if detail:
            return f"Здравствуйте! Хочу уточнить условия рассрочки {detail}."
        return "Здравствуйте! Хочу уточнить условия рассрочки."
