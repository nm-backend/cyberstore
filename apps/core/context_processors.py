from apps.catalog.tree import CategoryTree

from .models import SiteSettings


def site(request):
    tree = CategoryTree()
    roots = [root for root in tree.roots if tree.totals.get(root.pk, 0)]
    nav_menu = [
        {
            "category": category,
            "count": tree.totals[category.pk],
            "children": [
                {
                    "category": child,
                    "count": tree.totals[child.pk],
                    "children": [
                        {"category": grandchild, "count": tree.totals[grandchild.pk]}
                        for grandchild in tree.children[child.pk]
                    ],
                }
                for child in tree.children[category.pk]
                if tree.totals.get(child.pk, 0)
            ],
        }
        for category in roots
    ]
    return {
        "site": SiteSettings.load(),
        "nav_categories": roots,
        "nav_menu": nav_menu,
        "nav_total": sum(tree.totals[category.pk] for category in roots),
    }
