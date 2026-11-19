from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import (
    Brand, Category, CategoryFilter, CategoryQuickLink, Product, ProductSpec, SpecOption,
    SpecType, UseCase, make_unique_slug,
)
from apps.core.models import SiteSettings


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.laptops = Category.objects.create(name="Тестовые ноутбуки", slug="test-laptops", order=1)
        cls.pc = Category.objects.create(name="Тестовые ПК", slug="test-pc", order=2)
        cls.gaming = Category.objects.create(name="Тестовый подраздел", slug="test-gaming", parent=cls.laptops, order=1)
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
        self.assertContains(response, "Тестовые ноутбуки")
        self.assertContains(response, "Тестовые ПК")
        self.assertNotContains(response, "Gaming Pro")

    def test_category_shows_nested_products_and_subcategory_tiles(self):
        response = self.client.get(self.laptops.get_absolute_url())
        self.assertContains(response, "Gaming Pro")
        self.assertContains(response, "Тестовый ноутбук")
        self.assertContains(response, "Тестовый подраздел")

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
        group = next(item for item in response.context["filter_groups"] if item["title"] == "Процессор")
        counts = {option["label"]: option["count"] for option in group["options"]}
        self.assertEqual(counts["Ryzen 9"], 1)
        self.assertEqual(counts["Ryzen 5"], 1)

        response = self.client.get(self.laptops.get_absolute_url(), {f"spec_{row.pk}": "Ryzen 9"})
        self.assertContains(response, "Gaming Pro")
        self.assertNotContains(response, "Тестовый ноутбук")

    def test_empty_filter_group_is_hidden(self):
        empty = SpecType.objects.create(name="Пустая тестовая характеристика")
        CategoryFilter.objects.create(category=self.laptops, source="spec", spec_type=empty)
        response = self.client.get(self.laptops.get_absolute_url())
        self.assertNotContains(response, "Пустая тестовая характеристика")
        self.assertNotContains(response, "Пока нет вариантов")

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

        self.pricey.brand = self.brand
        self.pricey.save()
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
        self.assertContains(response, "Тестовый подраздел")
        self.assertNotContains(response, "Gaming Pro")

        response = self.client.get(self.laptops.get_absolute_url(), {"stock": "1"})
        self.assertContains(response, "Gaming Pro")

    def test_pagination_keeps_filters(self):
        for index in range(13):
            Product.objects.create(title=f"Товар {index}", category=self.pc, price=1000 + index)
        response = self.client.get(self.pc.get_absolute_url(), {"sort": "price_asc"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "sort=price_asc")


class CatalogStructureTests(TestCase):
    def test_four_main_categories_and_all_pages_open(self):
        roots = Category.objects.filter(parent__isnull=True, is_active=True)
        self.assertEqual(roots.count(), 4)
        self.assertEqual(
            list(roots.order_by("order").values_list("name", flat=True)),
            ["Настольные ПК", "Комплектующие для ПК", "Мониторы", "Ноутбуки"],
        )
        for category in Category.objects.filter(is_active=True):
            response = self.client.get(category.get_absolute_url())
            self.assertEqual(response.status_code, 200, category.slug)
        self.assertEqual(self.client.get(reverse("catalog:categories")).status_code, 200)

    def test_nav_has_catalog_menu_with_four_categories(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "nav-drop-menu")
        for name in ("Настольные ПК", "Комплектующие для ПК", "Мониторы", "Ноутбуки"):
            self.assertContains(response, name)

    def test_category_counts_are_real(self):
        laptops = Category.objects.get(slug="laptops")
        self.assertEqual(laptops.products.count(), 0)
        response = self.client.get(reverse("catalog:categories"))
        self.assertContains(response, "0 товаров")


class CatalogFacetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Фасетные ПК", slug="facet-pc", order=90)
        cls.brand_a = Brand.objects.create(name="Alpha", slug="alpha")
        cls.brand_b = Brand.objects.create(name="Beta", slug="beta")
        cls.processor = SpecType.objects.get(name="Процессор")
        CategoryFilter.objects.create(category=cls.category, source="brand", title="Бренд", order=1)
        CategoryFilter.objects.create(category=cls.category, source="condition", title="Состояние", order=2)
        cls.spec_filter = CategoryFilter.objects.create(
            category=cls.category, source="spec", spec_type=cls.processor, title="Процессор", order=3
        )
        cls.i5, _ = SpecOption.objects.get_or_create(spec_type=cls.processor, name="Intel Core i5")
        cls.i7, _ = SpecOption.objects.get_or_create(spec_type=cls.processor, name="Intel Core i7")
        cls.p1 = Product.objects.create(
            title="Альфа Новый i5", category=cls.category, brand=cls.brand_a,
            condition="new", price=30000, location="Бишкек",
        )
        cls.p2 = Product.objects.create(
            title="Альфа БУ i7", category=cls.category, brand=cls.brand_a,
            condition="used", price=10000, location="Ош",
        )
        cls.p3 = Product.objects.create(
            title="Бета Новый i7", category=cls.category, brand=cls.brand_b,
            condition="new", price=20000, location="Бишкек",
        )
        for product, option in ((cls.p1, cls.i5), (cls.p2, cls.i7), (cls.p3, cls.i7)):
            ProductSpec.objects.create(
                product=product, spec_type=cls.processor, option=option,
                value=option.name, filter_value=option.name,
            )

    def _group(self, response, title):
        return next(group for group in response.context["filter_groups"] if group["title"] == title)

    def _option(self, response, title, label):
        return next(option for option in self._group(response, title)["options"] if option["label"] == label)

    def test_or_inside_group_and_and_across_groups(self):
        response = self.client.get(self.category.get_absolute_url(), {"brand": "alpha"})
        self.assertEqual(response.context["result_count"], 2)
        self.assertEqual(self._option(response, "Процессор", "Intel Core i5")["count"], 1)
        self.assertEqual(self._option(response, "Процессор", "Intel Core i7")["count"], 1)
        self.assertEqual(self._option(response, "Состояние", "Новый")["count"], 1)
        self.assertEqual(self._option(response, "Состояние", "Б/у")["count"], 1)

        response = self.client.get(self.category.get_absolute_url(), {"brand": "alpha", "condition": "new"})
        self.assertEqual(response.context["result_count"], 1)
        self.assertEqual(self._option(response, "Процессор", "Intel Core i5")["count"], 1)
        self.assertEqual(self._option(response, "Процессор", "Intel Core i7")["count"], 0)

        response = self.client.get(self.category.get_absolute_url(), {
            f"spec_{self.spec_filter.pk}": ["Intel Core i5", "Intel Core i7"],
        })
        self.assertEqual(response.context["result_count"], 3)

    def test_counts_match_result_and_show_button(self):
        response = self.client.get(self.category.get_absolute_url(), {"brand": "alpha"})
        self.assertEqual(response.context["result_count"], 2)
        self.assertContains(response, "Показать (2)")
        self.assertContains(response, "Товаров: <strong>2</strong>", html=False)

    def test_sort_really_reorders_products(self):
        response = self.client.get(self.category.get_absolute_url(), {"sort": "price_asc"})
        html = response.content.decode()
        self.assertLess(html.index("Альфа БУ i7"), html.index("Бета Новый i7"))
        self.assertLess(html.index("Бета Новый i7"), html.index("Альфа Новый i5"))

        response = self.client.get(self.category.get_absolute_url(), {"sort": "price_desc"})
        html = response.content.decode()
        self.assertLess(html.index("Альфа Новый i5"), html.index("Альфа БУ i7"))

        response = self.client.get(self.category.get_absolute_url(), {"sort": "new"})
        html = response.content.decode()
        self.assertLess(html.index("Бета Новый i7"), html.index("Альфа Новый i5"))

    def test_disabled_option_hides_from_filter_but_product_keeps_spec(self):
        self.i5.is_active = False
        self.i5.save()
        response = self.client.get(self.category.get_absolute_url())
        labels = [option["label"] for option in self._group(response, "Процессор")["options"]]
        self.assertNotIn("Intel Core i5", labels)
        self.assertIn("Intel Core i7", labels)
        self.assertContains(self.client.get(self.p1.get_absolute_url()), "Intel Core i5")

    def test_new_value_appears_in_filter_without_code_changes(self):
        new_option = SpecOption.objects.create(spec_type=self.processor, name="AMD Ryzen 9 NEW")
        ProductSpec.objects.create(
            product=self.p3, spec_type=self.processor, option=new_option,
            value=new_option.name, filter_value=new_option.name,
        )
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(self._option(response, "Процессор", "AMD Ryzen 9 NEW")["count"], 1)

    def test_search_matches_spec_option_name(self):
        response = self.client.get(self.category.get_absolute_url(), {"q": "Intel Core i5"})
        self.assertContains(response, "Альфа Новый i5")
        self.assertNotContains(response, "Альфа БУ i7")
        self.assertNotContains(response, "Бета Новый i7")

    def test_installment_off_filter(self):
        self.p1.installment_available = True
        self.p1.save()
        response = self.client.get(self.category.get_absolute_url(), {"installment": "0"})
        self.assertEqual(response.context["result_count"], 2)
        self.assertNotContains(response, "Альфа Новый i5")

    def test_category_switch_and_chip(self):
        response = self.client.get(reverse("catalog:list"), {"category": "facet-pc"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 3)
        self.assertContains(response, "Категория: Фасетные ПК")

    def test_brand_tiles_show_real_counts(self):
        self.category.show_brand_tiles = True
        self.category.save()
        response = self.client.get(self.category.get_absolute_url())
        counts = {item["brand"].name: item["count"] for item in response.context["brand_tiles"]}
        self.assertEqual(counts, {"Alpha": 2, "Beta": 1})
        self.assertContains(response, "brand-tile")

    def test_category_index_search(self):
        response = self.client.get(reverse("catalog:categories"), {"q": "Фасетные"})
        self.assertContains(response, "Фасетные ПК")
        names = [group["root"].name for group in response.context["groups"]]
        self.assertEqual(names, ["Фасетные ПК"])

    def test_new_spec_type_bound_to_category_is_filterable(self):
        refresh = SpecType.objects.create(name="Частота обновления тест", data_type="number_unit", unit="Гц")
        refresh.categories.set([self.category])
        CategoryFilter.objects.create(category=self.category, source="spec", spec_type=refresh, title="Герцовка")
        ProductSpec.objects.create(product=self.p1, spec_type=refresh, value="144 Гц")

        response = self.client.get(self.category.get_absolute_url())
        self.assertContains(response, "144 Гц")
        response = self.client.get(Category.objects.get(slug="laptops").get_absolute_url())
        self.assertNotContains(response, "Герцовка")


class CatalogAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser("catalog-boss", "", "pass12345")
        cls.category = Category.objects.create(name="Админские ПК", slug="admin-pc", order=91)
        cls.processor = SpecType.objects.get(name="Процессор")
        cls.option = SpecOption.objects.create(spec_type=cls.processor, name="Intel Core i5 ADMIN")
        cls.product = Product.objects.create(title="Админский товар", category=cls.category, price=1000)
        ProductSpec.objects.create(
            product=cls.product, spec_type=cls.processor, option=cls.option,
            value=cls.option.name, filter_value=cls.option.name,
        )

    def setUp(self):
        self.client.force_login(self.admin)

    def test_admin_pages_open(self):
        for name in (
            "admin:catalog_specoption_changelist",
            "admin:catalog_spectype_changelist",
            "admin:catalog_brand_changelist",
            "admin:catalog_product_changelist",
            "admin:catalog_category_changelist",
        ):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_admin_created_spec_type_gets_filter_row(self):
        response = self.client.post(reverse("admin:catalog_spectype_add"), {
            "name": "Частота обновления ADMIN",
            "data_type": "number_unit",
            "unit": "Гц",
            "order": 0,
            "is_active": "on",
            "categories": [self.category.pk],
            "options-TOTAL_FORMS": "0",
            "options-INITIAL_FORMS": "0",
            "options-MIN_NUM_FORMS": "0",
            "options-MAX_NUM_FORMS": "1000",
        })
        self.assertEqual(response.status_code, 302)
        spec_type = SpecType.objects.get(name="Частота обновления ADMIN")
        self.assertTrue(
            CategoryFilter.objects.filter(category=self.category, spec_type=spec_type).exists()
        )

    def test_admin_can_add_processor_value(self):
        response = self.client.post(reverse("admin:catalog_specoption_add"), {
            "spec_type": self.processor.pk,
            "name": "AMD Ryzen 9 ADMIN",
            "order": 0,
            "is_active": "on",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SpecOption.objects.filter(name="AMD Ryzen 9 ADMIN").exists())

    def test_admin_cannot_delete_value_used_by_products(self):
        response = self.client.post(
            reverse("admin:catalog_specoption_delete", args=[self.option.pk]), {"post": "yes"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SpecOption.objects.filter(pk=self.option.pk).exists())

    def test_admin_can_delete_unused_value(self):
        unused = SpecOption.objects.create(spec_type=self.processor, name="Intel Core i3 ADMIN")
        response = self.client.post(
            reverse("admin:catalog_specoption_delete", args=[unused.pk]), {"post": "yes"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(SpecOption.objects.filter(pk=unused.pk).exists())

    def test_disabling_value_keeps_old_product_spec(self):
        self.option.is_active = False
        self.option.save()
        self.assertContains(self.client.get(self.product.get_absolute_url()), "Intel Core i5 ADMIN")
