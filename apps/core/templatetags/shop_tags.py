from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def price(value):
    """113000 -> '113 000 сом'. Empty price -> 'Цена по запросу'."""
    if value in (None, ""):
        return "Цена по запросу"
    try:
        return f"{int(value):,}".replace(",", "\u00a0") + "\u00a0сом"
    except (TypeError, ValueError):
        return ""


@register.simple_tag(takes_context=True)
def whatsapp_product(context, product):
    """WhatsApp link with a ready-made message specifying the exact product, price, and key specs."""
    request = context.get("request")
    site = context.get("site")
    if not site:
        return ""
    url = request.build_absolute_uri(product.get_absolute_url()) if request else ""
    
    category_name = getattr(product.category, "name", "").lower()
    icon = "💻" if "ноут" in category_name else ("🖥️" if "пк" in category_name or "комп" in category_name else "🔧")

    lines = [
        f"Здравствуйте! Заинтересовал {product.category.name if product.category_id else 'товар'}:",
        f"{icon} {product.title}",
    ]
    if product.price:
        lines.append(f"💰 Цена: {int(product.price):,}".replace(",", " ") + " сом")
    else:
        lines.append("💰 Цена: по запросу")

    specs = list(product.specs.all())[:4]
    if specs:
        lines.append("⚙️ Характеристики:")
        for s in specs:
            lines.append(f"  • {s.spec_type.name}: {s.value}")

    if url:
        lines.append(f"🔗 Ссылка: {url}")
    lines.append("Подскажите, есть ли в наличии и как оформить?")

    return site.whatsapp_url("\n".join(lines))


@register.simple_tag(takes_context=True)
def whatsapp_generic(context, text="Здравствуйте! Хочу получить консультацию по выбору ноутбука или ПК."):
    return context["site"].whatsapp_url(text)


@register.simple_tag(takes_context=True)
def canonical(context):
    request = context["request"]
    return request.build_absolute_uri(request.path)


@register.simple_tag(takes_context=True)
def absolute(context, url):
    return context["request"].build_absolute_uri(url)
