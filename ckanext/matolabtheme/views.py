import os
from flask import Blueprint
from flask.views import MethodView
import ckan.lib.base as base

log = __import__("logging").getLogger(__name__)

blueprint = Blueprint("matolabtheme", __name__)

HOST = os.environ.get("CKAN_HOST", "CKAN")
LEGAL_PERSON = os.environ.get(
    "CKANINI__CKANEXT__MATOLABTHEME__LEGAL_PERSON_MD", "NAME LEGAL PERSON RESPONSIBLE"
)
DSVGO_CONTACT = os.environ.get(
    "CKANINI__CKANEXT__MATOLABTHEME__DSVGO_CONTACT_MD", "CONTACT FOR DSVGO CONFLICTS"
)


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


def get_blueprint():
    return blueprint
