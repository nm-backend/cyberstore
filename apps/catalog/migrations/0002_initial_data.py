from django.db import migrations

USE_CASES = [
    ("games", "Игры", "🎮", 1),
    ("study", "Учёба", "📚", 2),
    ("office", "Офис и работа", "💼", 3),
    ("design", "Дизайн и графика", "🎨", 4),
    ("video", "Видеомонтаж", "🎬", 5),
    ("programming", "Программирование", "⌨️", 6),
]

SPEC_TYPES = [
    "Процессор", "Видеокарта", "Оперативная память", "Накопитель", "Экран",
    "Операционная система", "Материнская плата", "Блок питания", "Корпус",
    "Охлаждение", "Аккумулятор", "Порты и интерфейсы", "Вес",
]


def load(apps, schema_editor):
    UseCase = apps.get_model("catalog", "UseCase")
    SpecType = apps.get_model("catalog", "SpecType")

    for slug, name, icon, order in USE_CASES:
        UseCase.objects.get_or_create(slug=slug, defaults={"name": name, "icon": icon, "order": order})
    for order, name in enumerate(SPEC_TYPES, start=1):
        SpecType.objects.get_or_create(name=name, defaults={"order": order})


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]
    operations = [migrations.RunPython(load, migrations.RunPython.noop)]
