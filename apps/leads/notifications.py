import json
import logging
import os
from html import escape
from urllib import error, request

from django.conf import settings
from django.urls import NoReverseMatch, reverse
from django.utils import timezone

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"
REQUEST_TIMEOUT = 5
MAX_COMMENT_LENGTH = 500


def _admin_url(lead):
    """Прямая ссылка на заявку в админке. Без известного хоста ссылки не будет."""
    host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
    if not host:
        return ""
    try:
        return f"https://{host}{reverse('admin:leads_lead_change', args=[lead.pk])}"
    except NoReverseMatch:
        return ""


def build_message(lead):
    lines = ["🔥 <b>@ заявка с сайта</b>", ""]
    if lead.product_title:
        lines.append(f"<b>Товар:</b> {escape(lead.product_title)}")
    lines.append(f"<b>Имя:</b> {escape(lead.name)}")
    lines.append(f"<b>Телефон:</b> {escape(lead.phone)}")
    lines.append(f"<b>Рассрочка:</b> {'да' if lead.wants_installment else 'нет'}")
    comment = lead.comment.strip()
    if comment:
        if len(comment) > MAX_COMMENT_LENGTH:
            comment = comment[:MAX_COMMENT_LENGTH] + "…"
        lines.append(f"<b>Комментарий:</b> {escape(comment)}")
    lines.append(f"<b>Когда:</b> {timezone.localtime(lead.created_at):%d.%m.%Y %H:%M}")

    admin_url = _admin_url(lead)
    if admin_url:
        lines += ["", f'<a href="{escape(admin_url, quote=True)}">Открыть в админке</a>']
    return "\n".join(lines)


def chat_ids():
    """Получатели уведомлений: один или несколько id через запятую."""
    raw = getattr(settings, "TELEGRAM_CHAT_ID", "")
    return [part.strip() for part in raw.split(",") if part.strip()]


def notify_managers_about_lead(lead):
    """Шлёт заявку всем получателям. Никогда не бросает исключение: заявка важнее уведомления."""
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    recipients = chat_ids()
    if not token or not recipients:
        # A silent skip looks exactly like a broken bot, so say it in the log.
        logger.warning(
            "Telegram notification for lead %s skipped: set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env",
            lead.pk,
        )
        return False

    text = build_message(lead)
    delivered = False
    for chat_id in recipients:
        payload = json.dumps(
            {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            }
        ).encode("utf-8")
        telegram_request = request.Request(
            TELEGRAM_API.format(token=token),
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(telegram_request, timeout=REQUEST_TIMEOUT):
                pass
        except (error.HTTPError, error.URLError, OSError, ValueError) as exc:
            logger.warning(
                "Telegram notification for lead %s to chat %s failed: %s", lead.pk, chat_id, exc
            )
            continue
        delivered = True
    return delivered
