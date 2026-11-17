from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.models import SiteSettings


class CoreTests(TestCase):
    def test_pages_open(self):
        for name in ["core:home", "core:installment", "core:delivery", "core:contacts", "catalog:list"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_defaults_from_client_brief(self):
        site = SiteSettings.load()
        self.assertEqual(site.address, "Айни 31")
        self.assertEqual(site.city, "Бишкек")
        self.assertIn("9:00", site.work_hours)
        self.assertEqual(site.whatsapp_url(), "https://wa.me/996220053059")

    def test_settings_is_singleton(self):
        SiteSettings.objects.create(shop_name="Другой")
        SiteSettings.objects.create(shop_name="Ещё один")
        self.assertEqual(SiteSettings.objects.count(), 1)
        SiteSettings.load().delete()
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_address_change_shows_on_site(self):
        site = SiteSettings.load()
        site.address = "Чуй 100"
        site.save()
        response = self.client.get(reverse("core:contacts"))
        self.assertContains(response, "Чуй 100")
        self.assertNotContains(response, "Айни 31")

    def test_admin_settings_opens_directly(self):
        user = get_user_model().objects.create_superuser("boss", "", "pass12345")
        self.client.force_login(user)
        response = self.client.get(reverse("admin:core_sitesettings_changelist"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Айни 31")

    def test_404_page(self):
        self.assertEqual(self.client.get("/no-such-page/").status_code, 404)
