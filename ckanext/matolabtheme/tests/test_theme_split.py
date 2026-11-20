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


COLOUR_ONLY = re.compile(r"(^|-)color$|^background|^--(?!.*(font|line-height|gradient))|^fill$|^stroke$|^box-shadow$|^text-shadow$|^border(-[a-z]+)*-color$")
OWN_AREAS = re.compile(r"\.site-footer|\.homepage|footer|\.navbar")


def _props_by_selector(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i = {}, 0
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
            for sel, props in _props_by_selector(body).items():
                out.setdefault(sel, set()).update(props)
        elif not head.startswith("@"):
            props = set(re.findall(r"(--[\w-]+|[a-z-]+)\s*:", body))
            for sel in (re.sub(r"\s+", " ", x.strip()) for x in head.split(",") if x.strip()):
                out.setdefault(sel, set()).update(props)
        i = k
    return out


def test_generic_rules_keep_only_colours_in_the_common_css():
    """midnight-blue does layout and typography of generic components itself. Where a selector exists in both
    files, the common file may only carry its colour/background declarations; layout parts are default-only."""
    common, default = _props_by_selector(read("style.css")), _props_by_selector(read("style-default.css"))
    assert default, "style-default.css must contain the default-theme overrides"
    for sel in set(common) & set(default):
        if OWN_AREAS.search(sel):
            continue
        layout = {p for p in common[sel] if not COLOUR_ONLY.search(p)}
        assert not layout, "%s: layout declarations %s must live in style-default.css" % (sel, sorted(layout))


def test_font_tokens_are_default_only():
    """midnight-blue ships Noto Sans; overriding the font tokens changed every text on the site."""
    common, default = read("style.css"), read("style-default.css")
    for token in ("--bs-font-sans-serif", "--bs-body-font-family"):
        assert token not in common, token
        assert token in default, token


def test_own_navigation_keeps_its_layout_on_every_theme():
    """The header navigation is our own markup: without its layout the items run together."""
    props = _props_by_selector(read("style.css"))[".navbar-nav li a"]
    assert {"display", "padding"} <= props


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


def test_midnight_sticky_footer_and_hover():
    css = read("style-midnight.css")
    # short pages (login...) must keep the footer at the bottom; the homepage has its own layout
    assert "body:not(.homepage)" in css and "min-height: 100vh" in css
    assert "body:not(.homepage) > .site-footer" in css and "margin-top: auto" in css
    # the light outline buttons on the teal hero/footer invert on hover instead of turning charcoal
    assert ".btn-outline-light:hover" in css and "color: var(--bs-primary) !important" in css


def test_midnight_royal_blue_is_mapped_to_our_primary():
    css = read("style-midnight.css")
    for needle in ("--bs-link-color: var(--bs-primary)", ".form-label", ".btn-primary", ".pagination"):
        assert needle in css, needle
