import os
from flask import Blueprint
from flask.views import MethodView
import ckan.lib.base as base
import ckan.plugins.toolkit as toolkit

log = __import__("logging").getLogger(__name__)

blueprint = Blueprint("matolabtheme", __name__)

HOST = os.environ.get("CKAN_HOST", "CKAN")
LEGAL_PERSON = os.environ.get(
    "CKANINI__CKANEXT__MATOLABTHEME__LEGAL_PERSON_MD", "NAME LEGAL PERSON RESPONSIBLE"
)
DSVGO_CONTACT = os.environ.get(
    "CKANINI__CKANEXT__MATOLABTHEME__DSVGO_CONTACT_MD", "CONTACT FOR DSVGO CONFLICTS"
)

import ckan.logic.schema
from ckan.common import config, request, current_user
import ckan.lib.navl.dictization_functions as dict_fns
from ckan.views.home import CACHE_PARAMETERS
import ckan.logic as logic
from typing import Any, Union
from flask.wrappers import Response
from ckan.lib.helpers import helper_functions as h


import ckan.model as model
from ckan.common import request
import ckan.lib.uploader as uploader


class BannerConfigView(MethodView):
    def post(self) -> Union[str, Response]:
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
            del data_dict["save"]
            # data = logic.get_action("config_option_update")(
            #     {"user": current_user.name}, data_dict
            # )

            # Handle banner uploads AFTER calling CKAN’s function
            upload = uploader.get_uploader("admin")
            for key in list(data_dict.keys()):
                if key == "ckanext.matolabtheme.banner_top":
                    upload.update_data_dict(
                        data_dict,
                        "ckanext.matolabtheme.banner_top",
                        "ckanext.matolabtheme.banner_top_upload",
                        "ckanext.matolabtheme.clear_banner_top_upload",
                    )
                    upload.upload(uploader.get_max_image_size())
                    value = data_dict[key]
                    if upload.filepath:
                        static_url = upload.filepath.split("storage", 1)[-1]
                        value = h.url_for_static(static_url)
                        # Update CKAN's `config` object
                    model.set_system_info(key, value)
                    config[key] = value
                elif key == "ckanext.matolabtheme.banner_bottom":
                    upload.update_data_dict(
                        data_dict,
                        "ckanext.matolabtheme.banner_bottom",
                        "ckanext.matolabtheme.banner_bottom_upload",
                        "ckanext.matolabtheme.clear_banner_bottom_upload",
                    )
                    upload.upload(uploader.get_max_image_size())
                    value = data_dict[key]
                    if upload.filepath:
                        static_url = upload.filepath.split("storage", 1)[-1]
                        value = h.url_for_static(static_url)
                    model.set_system_info(key, value)
                    config[key] = value
                elif key == "ckanext.matolabtheme.attribution_logo":
                    upload.update_data_dict(
                        data_dict,
                        "ckanext.matolabtheme.attribution_logo",
                        "ckanext.matolabtheme.attribution_logo_upload",
                        "ckanext.matolabtheme.clear_attribution_logo_upload",
                    )
                    upload.upload(uploader.get_max_image_size())
                    value = data_dict[key]
                    if upload.filepath:
                        static_url = upload.filepath.split("storage", 1)[-1]
                        value = h.url_for_static(static_url)
                    model.set_system_info(key, value)
                    config[key] = value

        except logic.ValidationError as e:
            data = request.form
            errors = e.error_dict
            error_summary = e.error_summary
            vars = dict(data=data, errors=errors, error_summary=error_summary)
            return base.render("matolabtheme/banner_config.html", extra_vars=vars)

        return h.redirect_to("matolabtheme.banner_config")

    def get(self) -> str:
        schema = ckan.logic.schema.update_configuration_schema()
        data = {}
        for key in schema:
            data[key] = config.get(key)
        vars: dict[str, Any] = dict(data=data, errors={})
        return base.render("matolabtheme/banner_config.html", extra_vars=vars)


class DataProtectionView(MethodView):
    def get(self):
        return base.render(
            "matolabtheme/dataprotection.html",
            extra_vars={
                "host": HOST,
                "legal_person_address_md": LEGAL_PERSON,
                "dsvgo_contact_md": DSVGO_CONTACT,
            },
        )


blueprint.add_url_rule(
    "/dataprotection", view_func=DataProtectionView.as_view(str("dataprotection"))
)
blueprint.add_url_rule(
    "/admin/banner_config", view_func=BannerConfigView.as_view(str("banner_config"))
)


def get_blueprint():
    return blueprint
