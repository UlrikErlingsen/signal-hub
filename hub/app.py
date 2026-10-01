"""Signal Hub entry point: page config, theme and navigation built from apps.yaml."""

from __future__ import annotations

import os

# Keep Arrow serialization stable on macOS. This must be set before Streamlit imports Arrow.
os.environ.setdefault("ARROW_DEFAULT_MEMORY_POOL", "system")

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hub import home, theme  # noqa: E402
from hub.pages import page_function  # noqa: E402
from hub.registry import by_family, load  # noqa: E402

st.set_page_config(**theme.page_config())
APPS = load()

st.logo(str(theme.HUB_ICON), size="large", link="https://github.com/UlrikErlingsen/signal-hub")
sections: dict[str, list] = {
    "": [st.Page(lambda: home.render(APPS), title="Home", icon=":material/home:", url_path="home", default=True)]
}
for family, members in by_family(APPS).items():
    sections[family] = [
        st.Page(page_function(app), title=app.product + ("" if app.mode == "embedded" else " · soon"),
                url_path=app.slug)
        for app in members
    ]
current = st.navigation(sections)

theme.apply()
current.run()
