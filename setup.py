# -*- coding: utf-8 -*-
from codecs import open  # To use a consistent encoding
from os import path, environ

from setuptools import find_packages, setup  # Always prefer setuptools over distutils

here = path.abspath(path.dirname(__file__))


# Get the long description from the relevant file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here,"requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name="""ckanext-matolabtheme""",
    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    version=environ.get('VERSION', '0.0.0'),
    description="""CKAN theme of the Mat-O-Lab Project, changes landing Page and add alternative Data Privacy Act in English and German.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    # The project's main homepage.
    url="https://github.com/Mat-O-Lab/ckanext-matolabtheme",
    # Author details
    author="""Thomas Hanke""",
    author_email="""thomas.hanke@iwm.fraunhofer.de""",
    # Choose your license
    license="AGPL",
    packages=find_packages(),
    include_package_data=True,
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    },
    entry_points="""
        [ckan.plugins]
        matolabtheme=ckanext.matolabtheme.plugin:MatolabthemePlugin
    """,
    
)
