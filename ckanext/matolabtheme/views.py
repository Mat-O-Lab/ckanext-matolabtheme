import ckan.lib.base as base
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from flask.views import MethodView

from typing import Any, Union

import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.uploader as uploader
import ckan.logic as logic
import ckan.logic.schema
from ckan.common import _, config, current_user, request
from ckan.lib.helpers import helper_functions as h
from ckan.views.home import CACHE_PARAMETERS
from flask.wrappers import Response

log = __import__("logging").getLogger(__name__)

blueprint = Blueprint("matolabtheme", __name__)

if toolkit.check_ckan_version(min_version="2.10"):
    from ckan.types import Context
else:

    class Context(dict):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)


class ThemeConfigView(MethodView):
    def post(self) -> Union[str, Response]:
        try:
            context: Context = {
                "user": current_user.name,
                "auth_user_obj": current_user,
            }
            logic.check_access("sysadmin", context)
        except logic.NotAuthorized:
            base.abort(403, _("Need to be system administrator to administer"))
        try:
            req = request.form.copy()
            req.update(request.files.to_dict())
            data_dict = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(
                        logic.parse_params(req, ignore_keys=CACHE_PARAMETERS)
                    )
                )
            )
            
            # Set dark_mode based on whether the checkbox was checked
            data_dict["ckanext.matolabtheme.dark_mode"] = (
                "ckanext.matolabtheme.dark_mode" in req
            )
            del data_dict["ckanext.matolabtheme.dark_mode"]
            del data_dict["save"]
            
            # Handle uploads
            upload_fields=["banner_top","banner_bottom", "favicon", "attribution_logo"]
            #upload_fields=["ckanext.matolabtheme.banner_top"]
            extention_prefix="ckanext.matolabtheme."
            for key in upload_fields:
                config_key=extention_prefix+key
                if config_key in data_dict.keys():
                        upload = uploader.get_uploader("admin")
                        upload.update_data_dict(
                            data_dict,
                            config_key,
                            config_key+"_upload",
                            extention_prefix+"clear_"+key+"_upload",
                        )
                        upload.upload(uploader.get_max_image_size())
                        value = data_dict[config_key]
                        # # Set full Logo url
                        if value and not value.startswith('http') and not value.startswith('/'):
                            image_path = 'uploads/admin/'
                            value = h.url_for_static('{0}{1}'.format(image_path, value))
                        data_dict[config_key]=value   
            #set defaults if empty
            if "ckanext.matolabtheme.banner_top" in data_dict.keys() and not data_dict["ckanext.matolabtheme.banner_top"]:
                data_dict["ckanext.matolabtheme.banner_top"]="/static/banner_top.png"
            if "ckanext.matolabtheme.banner_bottom" in data_dict.keys() and not data_dict["ckanext.matolabtheme.banner_bottom"]:
                data_dict["ckanext.matolabtheme.banner_bottom"]="/static/banner_bottom.png"
            if "ckanext.matolabtheme.favicon" in data_dict.keys() and not data_dict["ckanext.matolabtheme.favicon"]:
                data_dict["ckanext.matolabtheme.favicon"]="/static/favicon.png"
            if "ckanext.matolabtheme.attribution_logo" in data_dict.keys() and not data_dict["ckanext.matolabtheme.attribution_logo"]:
                data_dict["ckanext.matolabtheme.attribution_logo"]="/static/favicon.png"
            data = logic.get_action("config_option_update")(
                {"user": current_user.name}, data_dict
            )

        except logic.ValidationError as e:
            data = request.form
            errors = e.error_dict
            error_summary = e.error_summary
            vars = dict(data=data, errors=errors, error_summary=error_summary)
            return base.render("matolabtheme/theme_config.html", extra_vars=vars)
        return h.redirect_to("matolabtheme.theme_config")

    def get(self) -> str:
        try:
            context: Context = {
                "user": current_user.name,
                "auth_user_obj": current_user,
            }
            logic.check_access("sysadmin", context)
        except logic.NotAuthorized:
            base.abort(403, _("Need to be system administrator to administer"))
        # dark_mode = toolkit.config.get("ckanext.matolabtheme.dark_mode")
        schema = ckan.logic.schema.update_configuration_schema()
        data = {}
        for key in schema:
            data[key] = config.get(key)
        vars: dict[str, Any] = dict(data=data, errors={})
        return base.render("matolabtheme/theme_config.html", extra_vars=vars)


class DataPrivacyView(MethodView):
    def get(self):
        return base.render(
            "matolabtheme/dataprivacy.html",
            extra_vars={
                "host": h.get_site_protocol_and_host()[-1],
                "legal_person_address_md": toolkit.config.get(
                    "ckanext.matolabtheme.legal_person_md"
                ),
                "dsvgo_contact_md": toolkit.config.get(
                    "ckanext.matolabtheme.dsvgo_contact_md"
                ),
                "contact_dp_commissioner_email_md": toolkit.config.get(
                    "ckanext.matolabtheme.contact_dp_commissioner_email_md"
                ),
            },
        )


blueprint.add_url_rule(
    "/dataprotection", view_func=DataPrivacyView.as_view(str("dataprotection"))
)
blueprint.add_url_rule(
    "/admin/theme_config", view_func=ThemeConfigView.as_view(str("theme_config"))
)


def get_blueprint():
    return blueprint
