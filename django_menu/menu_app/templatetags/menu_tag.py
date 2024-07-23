"""
Template tag for build nav tree.
"""
from django import template
from django.db.models import QuerySet
from django.template import RequestContext
from menu_app.models import Menu, MenuItem

register = template.Library()


def get_menu_items(
        menu_name: str,
        current_path: str
) -> list[MenuItem]:
    """
    Get items by menu name, and return tree.

    :param menu_name: 
    :param current_path: 
    :return: list[Queryset]
    :except: DoesNotExist rises if menu not found
    """
    try:
        menu = Menu.objects.get(name=menu_name)
        menu_items = (MenuItem.objects.filter(menu=menu)
                      .prefetch_related('parent'))
        item_dict = {item.id: item for item in menu_items}
        return get_tree(item_dict, current_path)
    except Menu.DoesNotExist:
        return []


def get_tree(
        items: dict[int, MenuItem],
        current_path: str,
) -> list[MenuItem]:
    """
    Get tree by menu items.

    :param items:
    :param current_path:
    :return: list[MenuItem]
    """
    tree = []
    for item in items.values():
        item.active = item.get_url() == current_path
        if item.parent_id:
            parent = items.get(item.parent_id)
            parent.active = item.active or parent.active
            if not hasattr(parent, 'children_items'):
                parent.children_items = []
            parent.children_items.append(item)
        else:
            tree.append(item)
    return tree


@register.inclusion_tag('main/menu.html', takes_context=True)
def draw_menu(
        context: RequestContext,
        menu_name: str
):
    """
    Tag with context to draw menu. May be loads in to template.

    :param context: Django RequestContext
    :param menu_name: Search menu by name
    """
    request = context.get('request')
    current_path = request.path
    menu_items = get_menu_items(menu_name, current_path)
    return {'menu_items': menu_items, 'current_path': current_path}
