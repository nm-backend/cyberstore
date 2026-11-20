import json
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from apps.catalog.models import Category, Product
from apps.leads.models import Lead


class LeadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Ноутбуки для заявок", slug="lead-test-laptops")
        cls.product = Product.objects.create(
            title="Dell Test", category=category, price=99000
        )

    def post(self, **extra):
        data = {
            "name": "Азиз", "phone": "+996 555 123 456", "consent": "1",
            "product_id": self.product.pk, "next": "/",
        }
        data.update(extra)
        return self.client.post(reverse("leads:create"), data, follow=True)

    def test_lead_saved_with_product(self):
        response = self.post(wants_installment="on")
        self.assertContains(response, "Заявка принята")
        lead = Lead.objects.get()
        self.assertEqual(lead.product, self.product)
        self.assertEqual(lead.product_title, "Dell Test")
        self.assertTrue(lead.wants_installment)

    def test_bad_phone_rejected(self):
        response = self.post(phone="12")
        self.assertContains(response, "Заявка не отправлена")
        self.assertEqual(Lead.objects.count(), 0)

    def test_honeypot_blocks_bots(self):
        self.post(website="http://spam.example")
        self.assertEqual(Lead.objects.count(), 0)

    def test_second_lead_too_fast_is_blocked(self):
        self.post()
        self.post(name="Бот")
        self.assertEqual(Lead.objects.count(), 1)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(reverse("leads:create")).status_code, 405)

    def test_consent_is_required(self):
        response = self.client.post(
            reverse("leads:create"),
            {"name": "Азиз", "phone": "+996 555 123 456", "next": "/"},
            follow=True,
        )
        self.assertContains(response, "Заявка не отправлена")
        self.assertEqual(Lead.objects.count(), 0)

    def test_invalid_form_keeps_values_for_modal(self):
        response = self.client.post(
            reverse("leads:create"),
            {"name": "Азиз", "phone": "abc", "consent": "1", "next": self.product.get_absolute_url()},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "value=\"Азиз\"")
        self.assertContains(response, "Введите номер телефона")
        self.assertContains(response, "data-open-on-load")
        self.assertEqual(Lead.objects.count(), 0)

    def test_bad_product_id_is_ignored(self):
        response = self.post(product_id="abc")
        self.assertContains(response, "Заявка принята")
        self.assertIsNone(Lead.objects.get().product)

    def test_open_redirect_is_blocked(self):
        response = self.client.post(
            reverse("leads:create"),
            {"name": "A", "phone": "+996555123456", "next": "https://evil.example/"},
        )
        self.assertEqual(response["Location"], "/")


class LeadApiThrottleTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(enforce_csrf_checks=False)

    def test_sixth_request_per_minute_is_rejected(self):
        data = {"name": "Азиз", "phone": "+996 555 123 456"}
        for _ in range(5):
            response = self.client.post("/api/leads/", data, format="json")
            self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.post("/api/leads/", data, format="json").status_code, 429)


@override_settings(TELEGRAM_BOT_TOKEN="123:abc", TELEGRAM_CHAT_ID="-100500")
class LeadNotificationTests(TestCase):
    def post(self):
        data = {
            "name": "Азиз", "phone": "+996 555 123 456", "consent": "1",
            "comment": "Позвонить после 18:00", "next": "/",
        }
        return self.client.post(reverse("leads:create"), data, follow=True)

    def test_telegram_message_sent_for_new_lead(self):
        with patch("apps.leads.notifications.request.urlopen") as urlopen:
            self.post()
        urlopen.assert_called_once()
        telegram_request = urlopen.call_args[0][0]
        self.assertIn("123:abc", telegram_request.full_url)
        body = json.loads(telegram_request.data.decode("utf-8"))
        self.assertEqual(body["chat_id"], "-100500")
        self.assertEqual(body["parse_mode"], "HTML")
        self.assertIn("+996 555 123 456", body["text"])
        self.assertIn("Позвонить после 18:00", body["text"])

    @override_settings(TELEGRAM_BOT_TOKEN="123:abc", TELEGRAM_CHAT_ID="111, -222")
    def test_message_sent_to_each_recipient(self):
        with patch("apps.leads.notifications.request.urlopen") as urlopen:
            self.post()
        self.assertEqual(urlopen.call_count, 2)
        sent = [json.loads(call[0][0].data.decode("utf-8"))["chat_id"] for call in urlopen.call_args_list]
        self.assertEqual(sent, ["111", "-222"])

    @override_settings(TELEGRAM_BOT_TOKEN="123:abc", TELEGRAM_CHAT_ID="bad, -222")
    def test_one_broken_recipient_does_not_block_others(self):
        with patch("apps.leads.notifications.request.urlopen", side_effect=[URLError("boom"), MagicMock()]):
            self.post()
        self.assertEqual(Lead.objects.count(), 1)

    def test_failed_telegram_request_does_not_break_lead(self):
        with patch("apps.leads.notifications.request.urlopen", side_effect=URLError("boom")):
            response = self.post()
        self.assertEqual(Lead.objects.count(), 1)
        self.assertContains(response, "Заявка принята")

    @override_settings(TELEGRAM_BOT_TOKEN="", TELEGRAM_CHAT_ID="")
    def test_no_request_without_settings(self):
        with patch("apps.leads.notifications.request.urlopen") as urlopen:
            self.post()
        urlopen.assert_not_called()
        self.assertEqual(Lead.objects.count(), 1)
