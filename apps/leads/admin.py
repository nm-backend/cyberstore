import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "phone", "product_title", "wants_installment", "status")
    list_editable = ("status",)
    list_filter = ("status", "wants_installment", "created_at")
    search_fields = ("name", "phone", "product_title", "comment")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    actions = ["export_csv"]

    @admin.action(description="Скачать выбранные заявки (CSV для Excel)")
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
        response["Content-Disposition"] = 'attachment; filename="leads.csv"'
        writer = csv.writer(response, delimiter=";")
        writer.writerow(["Дата", "Имя", "Телефон", "Товар", "Рассрочка", "Статус", "Комментарий"])
        for lead in queryset:
            writer.writerow([
                lead.created_at.strftime("%d.%m.%Y %H:%M"), lead.name, lead.phone,
                lead.product_title, "да" if lead.wants_installment else "нет",
                lead.get_status_display(), lead.comment,
            ])
        return response
