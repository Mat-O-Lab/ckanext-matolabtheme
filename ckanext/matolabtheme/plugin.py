import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.config.declaration import Declaration, Key
from ckan.lib.plugins import DefaultTranslation

from ckanext.matolabtheme import action, auth, helpers, views


class MatolabthemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigDeclaration)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.ITranslation)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "matolabtheme")

    # IConfigDeclaration

    def declare_config_options(self, declaration: Declaration, key: Key):

        declaration.annotate("matolabtheme")
        group = key.ckanext.matolabtheme
        declaration.declare(group.contact_url, "https://github.com/Mat-O-Lab")
        declaration.declare(
            group.legal_notice_url, "/legal_notice.html"
        )
        declaration.declare(
            group.contact_dp_commissioner_email_md,
            "[datenprotection_commissioner@example.de](mailto:datenschutzbeauftragte@example.de?subject=dataprotection CKAN)",
        )
        declaration.declare(
            group.dsvgo_contact_md,
            "legal person name, street number, Zip city, country",
        )
        option = declaration.declare_bool(group.dark_mode, False)
        option.set_validators("not_missing boolean_validator")
        declaration.declare(group.banner_top, "/static/banner_top.png")
        declaration.declare(group.banner_top_upload, "")
        declaration.declare(group.clear_banner_top_upload, "")
        declaration.declare(group.banner_bottom, "/static/banner_bottom.png")
        declaration.declare(group.banner_bottom_upload, "")
        declaration.declare(group.clear_banner_bottom_upload, "")
        declaration.declare(group.favicon, "/static/favicon.png")
        declaration.declare(group.favicon_upload, "")
        declaration.declare(group.clear_favicon_upload, "")
        declaration.declare(group.attribution_logo, "/static/favicon.png")
        declaration.declare(group.attribution_logo_upload, "")
        declaration.declare(group.clear_attribution_logo_upload, "")

    def update_config_schema(self, schema):

        ignore_missing = toolkit.get_validator("ignore_missing")
        # bool_val = toolkit.get_validator("boolean_validator")
        unicode_safe = toolkit.get_validator("unicode_safe")
        # dark_mode = toolkit.config.get("ckanext.matolabtheme.dark_mode")
        schema.update(
            {
                # This is an existing CKAN core configuration option, we are just
                # making it available to be editable at runtime
                # "ckanext.matolabtheme.dark_mode": [
                #     ignore_missing, bool_val
                # ],
                "ckanext.matolabtheme.banner_top": [
                    ignore_missing,
                    unicode_safe,
                ],
                "ckanext.matolabtheme.banner_bottom": [
                    ignore_missing,
                    unicode_safe,
                ],
                "ckanext.matolabtheme.favicon": [
                    ignore_missing,
                    unicode_safe,
                ],
                "ckanext.matolabtheme.attribution_logo": [
                    ignore_missing,
                    unicode_safe,
                ],
            }
        )
        return schema

    # ITemplateHelpers

    def get_helpers(self):
        return helpers.get_helpers()

    # IActions

    def get_actions(self):
        actions = action.get_actions()
        return actions

    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprint()

    # IAuthFunctions

    def get_auth_functions(self):
        return auth.get_auth_functions()
