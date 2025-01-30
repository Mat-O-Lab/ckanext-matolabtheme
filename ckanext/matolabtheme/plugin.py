import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.config.declaration import Declaration, Key
from ckanext.matolabtheme import helpers, views, action, auth


class MatolabthemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigDeclaration)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IAuthFunctions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "matolabtheme")

    def update_config_schema(self, schema):

        ignore_missing = toolkit.get_validator("ignore_missing")
        unicode_safe = toolkit.get_validator("unicode_safe")

        schema.update(
            {
                # This is an existing CKAN core configuration option, we are just
                # making it available to be editable at runtime
                "ckanext.matolabtheme.banner_top": [
                    ignore_missing,
                    unicode_safe,
                ],
                "ckanext.matolabtheme.banner_bottom": [
                    ignore_missing,
                    unicode_safe,
                ],
                "ckanext.matolabtheme.banner_top_upload": [
                    ignore_missing,
                    unicode_safe,
                ],
                "ckanext.matolabtheme.banner_bottom_upload": [
                    ignore_missing,
                    unicode_safe,
                ],
                "ckanext.matolabtheme.clear_banner_top_upload": [
                    ignore_missing,
                    unicode_safe,
                ],
                "ckanext.matolabtheme.clear_banner_bottom_upload": [
                    ignore_missing,
                    unicode_safe,
                ],
            }
        )

        return schema

    # IConfigDeclaration

    def declare_config_options(self, declaration: Declaration, key: Key):

        declaration.annotate("matolabtheme")
        group = key.ckanext.matolabtheme
        declaration.declare(group.banner_top, "/static/banner-top.png")
        declaration.declare(group.banner_top_upload, "")
        declaration.declare(group.clear_banner_top_upload, "")
        declaration.declare(group.banner_bottom, "/static/banner-bottom.png")
        declaration.declare(group.banner_bottom_upload, "")
        declaration.declare(group.clear_banner_bottom_upload, "")

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
