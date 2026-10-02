"""Signal Hub entry point: page config, theme and navigation built from apps.yaml."""

from __future__ import annotations

import os

# Keep Arrow serialization stable on macOS. This must be set before Streamlit imports Arrow.
os.environ.setdefault("ARROW_DEFAULT_MEMORY_POOL", "system")
# Tells embedded apps they run inside the shared Hub: session-memory storage only, fictional demo data, no network
# calls or disk writes (docs/APP_CONTRACT.md, section 8).
os.environ["SIGNAL_HUB"] = "1"

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hub import home, sidebar, theme  # noqa: E402
from hub.pages import page_function  # noqa: E402
from hub.registry import load  # noqa: E402

st.set_page_config(**theme.page_config())
APPS = load()

home_page = st.Page(lambda: home.render(APPS), title="Home", icon=":material/home:", url_path="home", default=True)
app_pages = {
    app.slug: st.Page(page_function(app), title=app.product + ("" if app.mode == "embedded" else " · soon"),
                      url_path=app.slug)
    for app in APPS
}
# Hidden: the menu is the Hub's own sidebar (hub/sidebar.py), so entries can carry marks and fold by family.
current = st.navigation([home_page, *app_pages.values()], position="hidden")

theme.apply()
sidebar.render(APPS, home_page, app_pages, current=current.url_path if current.url_path in app_pages else None)
current.run()
sidebar.footer()
