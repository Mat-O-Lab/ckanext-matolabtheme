[![Tests](https://github.com/Mat-O-Lab/ckanext-matolabtheme/actions/workflows/test.yml/badge.svg)](https://github.com/Mat-O-Lab/ckanext-matolabtheme/actions/workflows/test.yml)
# ckanext-matolabtheme

CKAN theme of the Mat-O-Lab Project, changes landing Page and add alternative Data Privacy Act in English and German.  

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.9 and earlier | not tested    |
| 2.10            | yes           |
| 2.11            | yes           |

Suggested values:

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Installation

To install the extension:

1. Activate your CKAN virtual environment, for example:
```bash
. /usr/lib/ckan/default/bin/activate
```
2. Use pip to install package
```bash
pip install ckanext-matolabtheme
```
3. Add `matolabtheme` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example, if you've deployed CKAN with Apache on Ubuntu:
```bash
sudo service apache2 reload
```

## Config settings

```bash
CKANINI__CKANEXT__MATOLABTHEME__CONTACT_URL=<url to contact site>
CKANINI__CKANEXT__MATOLABTHEME__LEGAL_PERSON_MD=<Legal Body Address in Markdown>
CKANINI__CKANEXT__MATOLABTHEME__LEGAL_NOTICE_URL=<Url to your legal notice information>
CKANINI__CKANEXT__MATOLABTHEME__DSVGO_CONTACT_MD=<Contact to adress with dsvgo conflicts in markdown>
CKANINI__CKANEXT__MATOLABTHEME__CONTACT_DP_COMMISSIONER_EMAIL_MD="[datenprotection_commissioner@example.de](mailto:datenschutzbeauftragte@example.de?subject=dataprotection ${CKAN_HOST})"
CKANINI__CKAN__FAVICON=/img/favicon.png
```
or ckan.ini parameters.
```bash
ckan.matolabtheme.contact_url = <url to contact site>
ckan.matolabtheme.legal_person_md = <Legal Body Address in Markdown>
ckan.matolabtheme.legal_notice_url = <Url to your legal notice information>
ckan.matolabtheme.dsvgo_contact_md = <Contact to adress with dsvgo conflicts in markdown>
ckan.matolabtheme.dsvgo_contact_md = "[datenprotection_commissioner@example.de](mailto:datenschutzbeauftragte@example.de?subject=dataprotection]"
ckan.favicon = /img/favicon.png
```
If no contact_url is given, it will relate to the about page!


## Developer installation

To install ckanext-csvtocsvw for development, activate your CKAN virtualenv and
do:
```bash
git clone https://github.com/Mat-O-Lab/ckanext-matolabtheme.git
cd ckanext-matolabtheme
python setup.py develop
pip install -r dev-requirements.txt
```

## Tests

To run the tests, do:
```bash
pytest --ckan-ini=test.ini
```

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
