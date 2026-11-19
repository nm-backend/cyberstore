from collections import defaultdict

from django.db.models import Count

from .models import Category, Product


class CategoryTree:
    """Active categories with published-product totals, built in one pass.

    Used by the nav menu, category tiles and the category index so every
    counter comes from the database and includes nested subcategories.
    """

    def __init__(self):
        self.categories = list(Category.objects.filter(is_active=True).order_by("order", "name"))
        own_counts = dict(
            Product.objects.published()
            .values("category_id")
            .annotate(n=Count("id"))
            .values_list("category_id", "n")
        )
        self.children = defaultdict(list)
        for category in self.categories:
            self.children[category.parent_id].append(category)
        self.totals = {}

        def total(category):
            if category.pk not in self.totals:
                self.totals[category.pk] = own_counts.get(category.pk, 0) + sum(
                    total(child) for child in self.children[category.pk]
                )
            return self.totals[category.pk]

        for category in self.categories:
            total(category)

        self.roots = self.children[None]
        self.flat = []

        def flatten(category, depth):
            self.flat.append((category, depth))
            for child in self.children[category.pk]:
                flatten(child, depth + 1)

        for root in self.roots:
            flatten(root, 0)

    def descendants(self, category):
        for child in self.children[category.pk]:
            yield child
            yield from self.descendants(child)

    def root_of(self, category):
        node = category
        while node.parent_id:
            node = node.parent
        return node

    def is_within(self, category, root):
        """True when category is root itself or one of its descendants."""
        node = category
        while node:
            if node.pk == root.pk:
                return True
            node = node.parent
        return False
