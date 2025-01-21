# import ckanext.datastore.logic.auth as auth
import ckan.plugins.toolkit as toolkit
from typing import Any

if toolkit.check_ckan_version("2.10"):
    from ckan.types import Context
else:

    class Context(dict):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)


def theme_stats(context: Context, data_dict: dict[str, Any]):
    # List of all active packages are visible by default
    return {"success": True}


def get_auth_functions():
    return {
        "theme_stats": theme_stats,
    }
