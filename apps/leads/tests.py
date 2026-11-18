from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product
from apps.leads.models import Lead


class LeadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Ноутбуки", slug="laptops")
        cls.product = Product.objects.create(
            title="Dell Test", category=category, price=99000
        )

    def post(self, **extra):
        data = {"name": "Азиз", "phone": "+996 555 123 456", "product_id": self.product.pk, "next": "/"}
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

    def test_open_redirect_is_blocked(self):
        response = self.client.post(
            reverse("leads:create"),
            {"name": "A", "phone": "+996555123456", "next": "https://evil.example/"},
        )
        self.assertEqual(response["Location"], "/")
