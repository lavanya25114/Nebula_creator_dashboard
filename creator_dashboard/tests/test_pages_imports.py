"""Smoke tests to ensure each page module imports and exposes `render_page()`.

These are quick checks to catch broken imports or missing public functions.
"""

import importlib

PAGES = [
    "pages.dashboard",
    "pages.profile",
    "pages.campaigns",
    "pages.collaborations",
    "pages.analytics",
    "pages.earnings",
    "pages.tasks",
    "pages.messages",
    "pages.notifications",
    "pages.settings",
]


def test_pages_have_render():
    for mod in PAGES:
        m = importlib.import_module(mod)
        assert hasattr(m, "render_page"), f"{mod} missing render_page"
