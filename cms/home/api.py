from django.http import JsonResponse
from wagtail.models import Page

from home.models import ContentPage, FunctionalPage, HomePage, PricingPage


def _get_url_path(page, home_path):
    """Strip the HomePage prefix from a page's url_path to get the frontend path."""
    path = page.url_path
    if path.startswith(home_path):
        path = path[len(home_path) - 1 :]  # keep leading /
    # Remove trailing slash for cleaner URLs
    return path.rstrip("/") or "/"


def _serialize_page(page, home_path):
    """Serialize a page to a navigation item dict."""
    specific = page.specific if not isinstance(page, (ContentPage, FunctionalPage, PricingPage)) else page

    data = {
        "id": page.pk,
        "title": page.title,
        "title_en": getattr(specific, "title_en", ""),
        "slug": page.slug,
        "icon": getattr(specific, "icon", ""),
        "url_path": _get_url_path(page, home_path),
        "page_type": f"home.{type(specific).__name__}",
        "vue_route_name": getattr(specific, "vue_route_name", None),
        "children": [],
    }
    return data


def navigation_view(request):
    """Return the full navigation tree as nested JSON."""
    try:
        home = HomePage.objects.live().first()
    except HomePage.DoesNotExist:
        return JsonResponse({"items": []})

    if not home:
        return JsonResponse({"items": []})

    home_path = home.url_path  # e.g. "/home/"

    # Get all live descendant pages that should appear in menu
    pages = (
        Page.objects.live()
        .descendant_of(home)
        .specific()
        .order_by("path")
    )

    # Filter for show_in_menu (all our custom types have it)
    menu_pages = []
    for p in pages:
        if getattr(p, "show_in_menu", True):
            menu_pages.append(p)

    # Build tree: group by depth
    # home.depth is the root depth, direct children are home.depth + 1
    home_depth = home.depth

    # Create lookup: page_id -> serialized item
    items_by_id = {}
    for p in menu_pages:
        items_by_id[p.pk] = _serialize_page(p, home_path)

    # Build parent-child relationships
    # Wagtail pages have a get_parent() but we can use path-based logic
    # Sort by menu_order within each level
    top_level = []
    for p in menu_pages:
        serialized = items_by_id[p.pk]
        if p.depth == home_depth + 1:
            top_level.append((getattr(p, "menu_order", 0), serialized))
        else:
            # Find parent: the page at depth - 1 in same branch
            parent = p.get_parent()
            if parent.pk in items_by_id:
                items_by_id[parent.pk]["children"].append(
                    (getattr(p, "menu_order", 0), serialized)
                )

    # Sort by menu_order
    top_level.sort(key=lambda x: x[0])
    result = [item for _, item in top_level]

    # Sort children too
    for item in items_by_id.values():
        if item["children"]:
            item["children"].sort(key=lambda x: x[0])
            item["children"] = [child for _, child in item["children"]]

    return JsonResponse({"items": result})
