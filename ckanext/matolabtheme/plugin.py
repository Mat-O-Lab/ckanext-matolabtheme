import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.matolabtheme import helpers


class MatolabthemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "matolabtheme")

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "parent_site_url": helpers.parent_site_url,
            "modify_geojson": helpers.modify_geojson,
            "check_ckan_version": toolkit.check_ckan_version,
        }
