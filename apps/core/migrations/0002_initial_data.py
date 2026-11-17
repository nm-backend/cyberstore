from django.db import migrations


def load(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    InstallmentOption = apps.get_model("core", "InstallmentOption")

    SiteSettings.objects.get_or_create(pk=1)
    if not InstallmentOption.objects.exists():
        InstallmentOption.objects.create(
            title="Рассрочка с банком", badge="18+", order=1,
            description="Оформление через Айыл Банк. Нужен только паспорт.",
        )
        InstallmentOption.objects.create(
            title="Рассрочка без банка", badge="18+", order=2,
            description="Рассрочка без участия банка. Нужен только паспорт.",
        )


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [migrations.RunPython(load, migrations.RunPython.noop)]
