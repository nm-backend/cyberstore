from django import template
from django.utils.html import format_html

from apps.catalog.models import IconKey

register = template.Library()

# The icon comes from the admin picker (IconKey); a blank value gets a neutral one.
def _section_icon(icon, fallback):
    return icon if icon in IconKey.values else fallback


def _icon_svg(key, css):
    return format_html(
        '<svg class="{}" aria-hidden="true" focusable="false"><use href="#i-{}"/></svg>',
        css,
        key,
    )


@register.simple_tag
def category_icon(category, css="ic"):
    return _icon_svg(_section_icon(category.icon, IconKey.GRID), css)


@register.simple_tag
def use_case_icon(use_case, css="ic"):
    return _icon_svg(_section_icon(use_case.icon, IconKey.TAG), css)


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

    category_title = f" ({product.category.name})" if product.category_id else ""
    lines = [
        f"Здравствуйте! Заинтересовал товар{category_title}:",
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
