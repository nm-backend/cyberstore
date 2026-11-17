from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product, ProductSpec, SpecType, make_unique_slug


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.laptops = Category.objects.get(slug="laptops")  # created by the data migration
        cls.cheap = Product.objects.create(
            title="Тестовый ноутбук", category=cls.laptops, price=30000, old_price=40000,
        )
        cls.pricey = Product.objects.create(title="Gaming Pro", category=cls.laptops, price=150000)
        cls.hidden = Product.objects.create(title="Скрытый", category=cls.laptops, price=1, is_published=False)
        ProductSpec.objects.create(
            product=cls.pricey, spec_type=SpecType.objects.get(name="Процессор"), value="Ryzen 9"
        )

    def test_slug_is_transliterated_and_unique(self):
        self.assertEqual(self.cheap.slug, "testovyy-noutbuk")
        self.assertEqual(make_unique_slug(Product, "Тестовый ноутбук"), "testovyy-noutbuk-2")

    def test_discount_percent(self):
        self.assertEqual(self.cheap.discount_percent, 25)
        self.assertEqual(self.pricey.discount_percent, 0)

    def test_list_hides_unpublished(self):
        response = self.client.get(reverse("catalog:list"))
        self.assertContains(response, "Gaming Pro")
        self.assertNotContains(response, "Скрытый")

    def test_price_filter(self):
        response = self.client.get(reverse("catalog:list"), {"price_max": 50000})
        self.assertContains(response, "Тестовый ноутбук")
        self.assertNotContains(response, "Gaming Pro")

    def test_search_by_spec_value(self):
        response = self.client.get(reverse("catalog:list"), {"q": "Ryzen"})
        self.assertContains(response, "Gaming Pro")
        self.assertNotContains(response, "Тестовый ноутбук")

    def test_bad_filter_values_do_not_crash(self):
        response = self.client.get(reverse("catalog:list"), {"price_min": "abc", "sort": "evil", "page": "x"})
        self.assertEqual(response.status_code, 200)

    def test_detail_has_whatsapp_link_with_product(self):
        response = self.client.get(self.pricey.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://wa.me/996220053059?text=")
        self.assertContains(response, "Gaming%20Pro")
        self.assertContains(response, "150%20000")

    def test_unpublished_detail_is_404(self):
        self.assertEqual(self.client.get(self.hidden.get_absolute_url()).status_code, 404)

    def test_price_on_request(self):
        product = Product.objects.create(title="Без цены", category=self.laptops)
        self.assertContains(self.client.get(product.get_absolute_url()), "Цена по запросу")

    def test_ready_pc_specs_in_whatsapp(self):
        pc_cat = Category.objects.get(slug="pc")
        pc = Product.objects.create(title="Cyber PC Ultra", category=pc_cat, price=95000)
        cpu_type = SpecType.objects.get(name="Процессор")
        gpu_type = SpecType.objects.get(name="Видеокарта")
        ProductSpec.objects.create(product=pc, spec_type=cpu_type, value="Core i5-13400F", order=1)
        ProductSpec.objects.create(product=pc, spec_type=gpu_type, value="RTX 4060 8GB", order=2)
        response = self.client.get(pc.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cyber%20PC%20Ultra")
        self.assertContains(response, "Core%20i5-13400F")
