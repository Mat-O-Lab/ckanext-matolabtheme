[![Tests](https://github.com/Mat-O-Lab/ckanext-matolabtheme/actions/workflows/test.yml/badge.svg)](https://github.com/Mat-O-Lab/ckanext-matolabtheme/actions/workflows/test.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19088706.svg)](https://doi.org/10.5281/zenodo.19088706)

# ckanext-matolabtheme

A CKAN extension that transforms a CKAN instance into a **product catalog UI**.
It includes configurable branding (logo, banner, favicon), GDPR-compliant
privacy pages in English and German, and a product-oriented landing page
suitable for materials science research data repositories.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.9 and earlier | not tested    |
| 2.10            | ✓ CI tested   |
| 2.11            | ✓ CI tested   |


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

## Theming

### Banners
Header (`banner_top.svg`) and footer (`banner_bottom.svg`) banners are crisp
SVG files — a deep-navy gradient with a subtle hexagonal lattice pattern.
Upload replacements or set an external URL via **Admin → Theme Config**.

### Colors
On first load the plugin seeds `ckan.site_custom_css` with a default navy
CSS variable palette (if no custom CSS is already configured):

```css
:root {
  --bs-primary: #1a3d5c;
  --bs-primary-rgb: 26, 61, 92;
  --bs-secondary: #4a7fa5;
  --bs-secondary-rgb: 74, 127, 165;
  --bs-body-bg: #f0f4f7;
  --bs-body-bg-rgb: 240, 244, 247;
}
```

To customise colors go to **Admin → Config → Custom CSS** and override any
CSS variable — no restart or code change required. Clearing the field restores
the plugin defaults on the next restart.

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

To install ckanext-matolabtheme for development, activate your CKAN virtualenv and do:
```bash
git clone https://github.com/Mat-O-Lab/ckanext-matolabtheme.git
cd ckanext-matolabtheme
pip install -e ".[dev]"
```

## Tests

To run the tests, do:
```bash
pytest --ckan-ini=test.ini
```

## Citation

If you use this software, please cite it. GitHub shows a **"Cite this repository"** button (top right of the repo page) that exports the [CITATION.cff](CITATION.cff) in APA or BibTeX format.

After the first Zenodo release, a DOI-specific BibTeX entry will be available on the Zenodo record. Until then:

```bibtex
@software{hanke_ckanext_matolabtheme,
  author       = {Hanke, Thomas},
  title        = {ckanext-matolabtheme},
  url          = {https://github.com/Mat-O-Lab/ckanext-matolabtheme},
  license      = {AGPL-3.0-or-later},
}
```

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
