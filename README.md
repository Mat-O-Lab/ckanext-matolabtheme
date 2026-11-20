[![Tests](https://github.com/Mat-O-Lab/ckanext-matolabtheme/actions/workflows/test.yml/badge.svg)](https://github.com/Mat-O-Lab/ckanext-matolabtheme/actions/workflows/test.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19088706.svg)](https://doi.org/10.5281/zenodo.19088706)

# ckanext-matolabtheme

A CKAN extension providing the Mat-O-Lab theme for data portals. It includes
configurable branding (logo, banner, favicon), GDPR-compliant privacy pages in
English and German, and a customisable landing page suitable for materials
science research data repositories. It works with both CKAN base themes, the
default one and the opt-in **midnight-blue** theme (the default of CKAN 3.0).

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.9 and earlier | not tested    |
| 2.10            | ✓ CI tested   |
| 2.11            | ✓ CI tested   |
| 2.12            | ✓ CI tested   |


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

### CKAN base themes: default and midnight-blue
CKAN 2.12 ships an opt-in **midnight-blue** theme. Enable it in `ckan.ini`:

```ini
ckan.base_public_folder = public-midnight-blue
ckan.base_templates_folder = templates-midnight-blue
```

(in Docker: `CKANINI__CKAN__BASE_PUBLIC_FOLDER` / `CKANINI__CKAN__BASE_TEMPLATES_FOLDER`). The plugin detects the active
theme (`ckan.base_templates_folder`) and loads matching styles:

| file | loaded | content |
| --- | --- | --- |
| `style.css` | always | Mat-O-Lab branding: palette tokens, our own markup (landing page, footer, header navigation, dataset items) and, for generic components, only colours and backgrounds |
| `style-default.css` | default theme only | layout, typography and spacing fixes of generic components (forms, navigation, links, ...) that the default theme needs |
| `style-midnight.css` | midnight-blue only | maps midnight's hard-coded blue (links, buttons, form labels, active navigation, facet headers, pagination) to `--bs-primary`, readable text on the format badges and the counters, hover style of the light outline buttons, spacing of the sidebar and a sticky footer for short pages |

midnight-blue does layout and typography of the generic components itself (including its own font), so none of that is
overridden there. The optional dark mode (`ckanext.matolabtheme.dark_mode`) is only available on the default theme. The
landing page, footer, header navigation and dataset item templates are ours and keep the Mat-O-Lab layout on both themes.

The helper `h.matolabtheme_is_midnight_blue()` returns the active theme if you want to branch in your own templates.

### Banners
Header (`banner_top.svg`) and footer (`banner_bottom.svg`) are crisp SVG files —
a teal gradient with flowing sinusoidal wave lines. Upload replacements or set
an external URL via **Admin → Theme Config**.

### Colors
On first load the plugin seeds `ckan.site_custom_css` with a default navy CSS
variable palette (if no custom CSS is already configured):

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

The same tokens are also set in `style.css`, so the palette applies even when the custom CSS field is used for
something else. To customise colors go to **Admin → Config → Custom CSS** and override any CSS variable — no restart
required. Clearing the field restores the plugin defaults on the next restart. On midnight-blue, `--bs-primary` also
drives links, buttons, form labels, active navigation items and facet headers, so one variable recolours the whole site.

## Config settings

All options are read from `ckan.ini` or from environment variables with the `CKANINI__` prefix
(`ckanext.matolabtheme.contact_url` becomes `CKANINI__CKANEXT__MATOLABTHEME__CONTACT_URL`):

| ckan.ini key | Default | Description |
| --- | --- | --- |
| `ckanext.matolabtheme.contact_url` | `https://github.com/Mat-O-Lab` | Target of the "Kontakt" button in the footer |
| `ckanext.matolabtheme.legal_notice_url` | `/legal_notice.html` | Target of the "Impressum" button in the footer |
| `ckanext.matolabtheme.legal_person_md` | | Legal body address (Markdown) for the privacy page |
| `ckanext.matolabtheme.dsvgo_contact_md` | | Contact for data protection conflicts (Markdown) |
| `ckanext.matolabtheme.contact_dp_commissioner_email_md` | | Data protection commissioner email (Markdown link) |
| `ckanext.matolabtheme.dark_mode` | `false` | Dark colour scheme (default theme only) |
| `ckanext.matolabtheme.banner_top` / `banner_bottom` | `/static/banner_top.svg` / `/static/banner_bottom.svg` | Header and footer banner |
| `ckanext.matolabtheme.favicon` | `/static/Logo.svg` | Favicon |
| `ckanext.matolabtheme.attribution_logo` | `/static/Logo.svg` | "Provided by" logo in the footer |

Banners, favicon and attribution logo can also be uploaded in **Admin → Theme Config**. Example `.env` for Docker:

```bash
CKANINI__CKANEXT__MATOLABTHEME__CONTACT_URL=<url to contact site>
CKANINI__CKANEXT__MATOLABTHEME__LEGAL_PERSON_MD=<Legal Body Address in Markdown>
CKANINI__CKANEXT__MATOLABTHEME__LEGAL_NOTICE_URL=<Url to your legal notice information>
CKANINI__CKANEXT__MATOLABTHEME__DSVGO_CONTACT_MD=<Contact to adress with dsvgo conflicts in markdown>
CKANINI__CKANEXT__MATOLABTHEME__CONTACT_DP_COMMISSIONER_EMAIL_MD="[datenprotection_commissioner@example.de](mailto:datenschutzbeauftragte@example.de?subject=dataprotection ${CKAN_HOST})"
CKANINI__CKAN__SITE_LOGO=/static/Logo.svg
CKANINI__CKAN__FAVICON=/static/favicon.png
```

If no contact_url is given, it will relate to the about page.

**Use relative paths for logos and icons** (`/static/Logo.svg`), not an absolute `https://<host>/static/Logo.svg` built
from the site URL. With an absolute URL the browser requests the image from another origin whenever you open the site
with a different scheme or hostname (for example `http://` while the site URL is `https://`), which fails with a
self-signed certificate, so the header logo shows as a broken image.


## Developer installation

To install ckanext-matolabtheme for development, activate your CKAN virtualenv and do:
```bash
git clone https://github.com/Mat-O-Lab/ckanext-matolabtheme.git
cd ckanext-matolabtheme
pip install -e ".[dev]"
```

## Tests

To run all tests (needs a CKAN test database, as in the CI workflow):
```bash
pytest --ckan-ini=test.ini ckanext/matolabtheme
```

`ckanext/matolabtheme/tests/test_theme_split.py` needs neither a database nor CKAN fixtures. It checks the split of the
stylesheets, the theme detection and the midnight-blue fixes, and can be run on its own:
```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest ckanext/matolabtheme/tests/test_theme_split.py
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
