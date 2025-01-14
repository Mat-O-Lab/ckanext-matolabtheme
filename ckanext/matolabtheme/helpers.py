from ckan.common import config
import ckan.plugins.toolkit as toolkit
import urllib.request, json, os
from typing import Union, Any
from markupsafe import Markup
from ckan.lib.helpers import _link_to, _link_active

CONTACT_URL = os.environ.get("CKANINI__CKANEXT__MATOLABTHEME__CONTACT_URL", "/about")


def parent_site_url():
    """
    Return the URL of the parent site (eg, if this instance
    is running in a CKAN + CMS config). Returns the setting
    ckan.parent_site_url, or value of h.url('home') if that
    setting is missing
    """
    return toolkit.h.url("home")


def contact_url():
    return CONTACT_URL


def custom_build_nav_main(
    *args: Union[
        tuple[str, str],
        tuple[str, str, list[str]],
        tuple[str, str, list[str], str],
    ]
) -> Markup:
    """Build a set of menu items.

    Outputs ``<li><a href="...">title</a></li>``

    :param args: tuples of (menu type, title) eg ('login', _('Login')).
        Third item specifies controllers which should be used to
        mark link as active.
        Fourth item specifies auth function to check permissions against.
    :type args: tuple[str, str, Optional[list], Optional[str]]

    :rtype: str
    """
    output: Markup = toolkit.h.literal("")
    for item in args:
        padding: Any = (None,) * 4
        menu_item, title, highlight_controllers, auth_function = (item + padding)[:4]
        if auth_function and not toolkit.h.check_access(auth_function):
            continue
        output += _make_nav_item(
            menu_item, title, highlight_controllers=highlight_controllers
        )
    return output


def _make_nav_item(menu_item: str, title: str, **kw: Any) -> Markup:
    """build a navigation item used for example breadcrumbs

    outputs <li><a href="..."></i> title</a></li>

    :param menu_item: the name of the defined menu item defined in
    config/routing as the named route of the same name
    :type menu_item: string
    :param title: text used for the link
    :type title: string
    :param **kw: additional keywords needed for creating url eg id=...

    :rtype: HTML literal

    This function is called by wrapper functions.
    """
    controller, action = menu_item.split(".")
    item = {"action": action, "controller": controller}
    item.update(kw)
    active = _link_active(item)
    # Remove highlight controllers so that they won't appear in generated urls.
    item.pop("highlight_controllers", False)

    link = _link_to(
        title, menu_item, suppress_active_class=True, class_="nav-link", **item
    )
    if active:
        return (
            toolkit.h.literal('<li class="nav-item active">')
            + link
            + toolkit.h.literal("</li>")
        )
    return (
        toolkit.h.literal('<li class="nav-item active">')
        + link
        + toolkit.h.literal("</li>")
    )


def get_helpers():
    return {
        "parent_site_url": parent_site_url,
        "custom_build_nav_main": custom_build_nav_main,
        "contact_url": contact_url,
    }
