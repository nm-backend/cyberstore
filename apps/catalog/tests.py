from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import (
    Brand, Category, CategoryFilter, CategoryQuickLink, Product, ProductSpec, SpecType,
    UseCase, make_unique_slug,
)
from apps.core.models import SiteSettings


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.laptops = Category.objects.create(name="Ноутбуки", slug="laptops", icon="💻", order=1)
        cls.pc = Category.objects.create(name="Настольные ПК", slug="pc", icon="🖥️", order=2)
        cls.gaming = Category.objects.create(name="Игровые", slug="gaming", parent=cls.laptops, order=1)
        cls.brand = Brand.objects.create(name="TestBrand", slug="testbrand")
        cls.cheap = Product.objects.create(
            title="Тестовый ноутбук", category=cls.laptops, price=30000, old_price=40000,
            brand=cls.brand, condition="new", delivery="free", location="Бишкек",
        )
        cls.pricey = Product.objects.create(title="Gaming Pro", category=cls.gaming, price=150000)
        cls.hidden = Product.objects.create(title="Скрытый", category=cls.laptops, price=1, is_published=False)
        cls.cpu = SpecType.objects.get(name="Процессор")
        ProductSpec.objects.create(product=cls.pricey, spec_type=cls.cpu, value="Ryzen 9")
        ProductSpec.objects.create(product=cls.cheap, spec_type=cls.cpu, value="Ryzen 5")

    def test_slug_is_transliterated_and_unique(self):
        self.assertEqual(self.cheap.slug, "testovyy-noutbuk")
        self.assertEqual(make_unique_slug(Product, "Тестовый ноутбук"), "testovyy-noutbuk-2")

    def test_discount_percent(self):
        self.assertEqual(self.cheap.discount_percent, 25)
        self.assertEqual(self.pricey.discount_percent, 0)

    def test_new_product_defaults(self):
        product = Product.objects.create(title="Новый", category=self.laptops)
        self.assertFalse(product.installment_available)
        self.assertEqual(product.condition, "")
        self.assertEqual(product.delivery, "")
        self.assertEqual(product.location, "")

    def test_root_shows_category_tiles(self):
        response = self.client.get(reverse("catalog:list"))
        self.assertContains(response, "Ноутбуки")
        self.assertContains(response, "Настольные ПК")
        self.assertNotContains(response, "Gaming Pro")

    def test_category_shows_nested_products_and_subcategory_tiles(self):
        response = self.client.get(self.laptops.get_absolute_url())
        self.assertContains(response, "Gaming Pro")
        self.assertContains(response, "Тестовый ноутбук")
        self.assertContains(response, "Игровые")

    def test_list_hides_unpublished(self):
        response = self.client.get(self.laptops.get_absolute_url())
        self.assertContains(response, "Gaming Pro")
        self.assertNotContains(response, "Скрытый")

    def test_price_filter(self):
        response = self.client.get(self.laptops.get_absolute_url(), {"price_max": 50000})
        self.assertContains(response, "Тестовый ноутбук")
        self.assertNotContains(response, "Gaming Pro")

    def test_search_by_spec_value(self):
        response = self.client.get(reverse("catalog:list"), {"q": "Ryzen 9"})
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
        pc = Product.objects.create(title="Cyber PC Ultra", category=self.pc, price=95000)
        gpu_type = SpecType.objects.get(name="Видеокарта")
        ProductSpec.objects.create(product=pc, spec_type=self.cpu, value="Core i5-13400F", order=1)
        ProductSpec.objects.create(product=pc, spec_type=gpu_type, value="RTX 4060 8GB", order=2)
        response = self.client.get(pc.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cyber%20PC%20Ultra")
        self.assertContains(response, "Core%20i5-13400F")

    def test_spec_filter_group_and_selection(self):
        row = CategoryFilter.objects.create(
            category=self.laptops, source="spec", spec_type=self.cpu, title="Процессор"
        )
        response = self.client.get(self.laptops.get_absolute_url())
        self.assertContains(response, "Процессор")
        self.assertContains(response, "Ryzen 9")
        self.assertContains(response, "Ryzen 5")
        self.assertEqual(response.content.decode().count('class="filter-count"'), 2)

        response = self.client.get(self.laptops.get_absolute_url(), {f"spec_{row.pk}": "Ryzen 9"})
        self.assertContains(response, "Gaming Pro")
        self.assertNotContains(response, "Тестовый ноутбук")

    def test_empty_filter_group_shows_placeholder(self):
        CategoryFilter.objects.create(category=self.laptops, source="installment")
        response = self.client.get(self.laptops.get_absolute_url())
        self.assertContains(response, "Пока нет вариантов")

    def test_filter_values_sort_numerically(self):
        ram = SpecType.objects.create(name="Объём ОЗУ")
        CategoryFilter.objects.create(category=self.pc, source="spec", spec_type=ram)
        small = Product.objects.create(title="Восемь", category=self.pc, price=1000)
        big = Product.objects.create(title="Шестнадцать", category=self.pc, price=2000)
        ProductSpec.objects.create(product=small, spec_type=ram, value="8 ГБ")
        ProductSpec.objects.create(product=big, spec_type=ram, value="16 ГБ")

        html = self.client.get(self.pc.get_absolute_url()).content.decode()
        self.assertLess(html.index("8 ГБ"), html.index("16 ГБ"))

    def test_usd_switch_hidden_without_rate_and_filters_by_rate(self):
        CategoryFilter.objects.create(category=self.laptops, source="price")
        response = self.client.get(self.laptops.get_absolute_url())
        self.assertNotContains(response, "Доллар (USD)")

        site = SiteSettings.load()
        site.usd_rate = 80
        site.save()
        response = self.client.get(self.laptops.get_absolute_url())
        self.assertContains(response, "Доллар (USD)")

        response = self.client.get(
            self.laptops.get_absolute_url(), {"price_max": 1000, "currency": "usd"}
        )
        self.assertContains(response, "Тестовый ноутбук")
        self.assertNotContains(response, "Gaming Pro")

    def test_subcategory_inherits_nearest_filters(self):
        CategoryFilter.objects.create(
            category=self.laptops, source="spec", spec_type=self.cpu, title="Процессор"
        )
        response = self.client.get(self.gaming.get_absolute_url())
        self.assertContains(response, 'filter-group-title">Процессор')

        CategoryFilter.objects.create(category=self.gaming, source="brand", title="Бренд")
        response = self.client.get(self.gaming.get_absolute_url())
        self.assertContains(response, 'filter-group-title">Бренд')
        self.assertNotContains(response, 'filter-group-title">Процессор')

    def test_quick_link_enables_use_case_filter(self):
        games = UseCase.objects.get(slug="games")
        link = CategoryQuickLink.objects.create(category=self.laptops, label="Для игр")
        link.use_cases.add(games)
        self.pricey.use_cases.add(games)

        response = self.client.get(self.laptops.get_absolute_url())
        self.assertContains(response, "Для игр")
        self.assertContains(response, "use_case=games")

        response = self.client.get(self.laptops.get_absolute_url(), {"use_case": "games"})
        self.assertContains(response, "Gaming Pro")
        self.assertNotContains(response, "Тестовый ноутбук")
        self.assertNotContains(response, "Для игр")

    def test_tiles_only_mode_hides_products_until_filter(self):
        self.laptops.display_mode = Category.DisplayMode.TILES
        self.laptops.save()
        response = self.client.get(self.laptops.get_absolute_url())
        self.assertContains(response, "Игровые")
        self.assertNotContains(response, "Gaming Pro")

        response = self.client.get(self.laptops.get_absolute_url(), {"stock": "1"})
        self.assertContains(response, "Gaming Pro")

    def test_pagination_keeps_filters(self):
        for index in range(13):
            Product.objects.create(title=f"Товар {index}", category=self.pc, price=1000 + index)
        response = self.client.get(self.pc.get_absolute_url(), {"sort": "price_asc"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "sort=price_asc")
