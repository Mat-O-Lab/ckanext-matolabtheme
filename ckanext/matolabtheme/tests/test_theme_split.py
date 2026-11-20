"""The CSS is split so that the CKAN midnight-blue theme (which styles forms, navigation,
links, ... itself) does not get our overrides of the default theme."""

import os
import re

import pytest
import yaml
from ckan.plugins import toolkit as tk

from ckanext.matolabtheme import helpers

ASSETS = os.path.join(os.path.dirname(helpers.__file__), "assets")
TEMPLATES = os.path.join(os.path.dirname(helpers.__file__), "templates")
read = lambda p: open(os.path.join(ASSETS, p), encoding="utf-8").read()


def _selectors(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    sels, i = set(), 0
    while i < len(css):
        j = css.find("{", i)
        if j < 0:
            break
        head, depth, k = css[i:j].strip(), 1, j + 1
        while k < len(css) and depth:
            depth += (css[k] == "{") - (css[k] == "}")
            k += 1
        body = css[j + 1:k - 1]
        if head.startswith(("@media", "@supports")):
            sels |= _selectors(body)
        elif not head.startswith("@") or ":root" in head:
            sels |= {re.sub(r"\s+", " ", s.strip()) for s in head.replace('@charset "UTF-8";', "").split(",") if s.strip()}
        i = k
    return sels


@pytest.mark.parametrize("value, expected", [
    ("templates-midnight-blue", True),
    ("templates", False),
    (None, False),
])
def test_is_midnight_blue(monkeypatch, value, expected):
    if value is None:
        monkeypatch.delitem(tk.config, "ckan.base_templates_folder", raising=False)
    else:
        monkeypatch.setitem(tk.config, "ckan.base_templates_folder", value)
    assert helpers.is_midnight_blue() is expected
    assert helpers.get_helpers()["matolabtheme_is_midnight_blue"]() is expected


def test_default_overrides_are_not_in_the_common_css():
    common, default = _selectors(read("style.css")), _selectors(read("style-default.css"))
    assert default, "style-default.css must contain the default-theme overrides"
    assert not (common & default), sorted(common & default)


def test_overrides_that_clash_with_midnight_blue_are_default_only():
    """These selectors set colours/backgrounds that midnight-blue defines itself."""
    default = _selectors(read("style-default.css"))
    for sel in ("a", "body", ".form-control", ".form-select", ".nav-link", ".dropdown-menu"):
        assert sel in default, sel
        assert sel not in _selectors(read("style.css")), sel


def test_midnight_fix_restores_counter_colour():
    css = read("style-midnight.css")
    assert ".homepage .counter-row h1" in css and "color: inherit" in css


def test_webassets_bundles_point_at_existing_files():
    bundles = yaml.safe_load(read("webassets.yml"))
    for name in ("style", "style-default", "style-midnight"):
        for f in bundles[name]["contents"]:
            assert os.path.isfile(os.path.join(ASSETS, f)), f


def test_base_template_loads_the_right_bundle():
    html = open(os.path.join(TEMPLATES, "base.html"), encoding="utf-8").read()
    assert "matolabtheme_is_midnight_blue()" in html
    assert html.index("style-midnight") < html.index("{% else %}") < html.index("style-default")
    # dark mode only exists for the default theme
    assert html.index("style-default") < html.index("matolabtheme/dark")


def test_midnight_format_badges_get_readable_text_colours():
    """midnight-blue colours .badge[data-format] text for its own pale badges; our solid backgrounds need
    their own text colour."""
    css = read("style-midnight.css")
    common = read("style.css")
    for fmt in ("csv", "json", "pdf", "rdf", "zip"):
        assert '.badge[data-format*="%s"]' % fmt in common      # we give it a background...
        assert '.badge[data-format*="%s"]' % fmt in css         # ...so we must also set the text colour
