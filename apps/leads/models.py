from django.db import models


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        DONE = "done", "Продано"
        CANCELLED = "cancelled", "Отказ"

    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=30)
    product = models.ForeignKey(
        "catalog.Product", verbose_name="Товар", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="leads",
    )
    product_title = models.CharField("Название товара на момент заявки", max_length=200, blank=True)
    wants_installment = models.BooleanField("Интересует рассрочка", default=False)
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField("Статус", max_length=12, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} — {self.phone}"
