"""Signal Hub contract: importable UI entry point, Streamlit only under ui/, slug-namespaced keys, Hub mode.

Written by signal-hub/scripts/scaffold_app.py. Extend it with the app's own pages; keep the checks.
"""

import ast
import os
from pathlib import Path
import subprocess
import sys

import pytest
from streamlit.testing.v1 import AppTest

from {{package}} import __version__

ROOT = Path(__file__).parents[1]
PACKAGE = ROOT / "src" / "{{package}}"
UI = PACKAGE / "ui"
UI_ONLY = {"streamlit", "plotly"}
RENDER = "from {{package}}.ui import render\n\nrender()\n"


def _imported_roots(path: Path) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module.split(".")[0])
    return roots


def test_app_info_matches_the_hub_registry() -> None:
    from {{package}}.ui import APP_INFO, render

    assert callable(render)
    assert APP_INFO == {"product": "{{Name}}", "version": __version__, "repo": "{{repo}}", "slug": "{{key}}"}


def test_only_the_ui_package_imports_streamlit_or_plotly() -> None:
    offenders = {str(p.relative_to(PACKAGE)): sorted(_imported_roots(p) & UI_ONLY)
                 for p in PACKAGE.rglob("*.py") if UI not in p.parents and _imported_roots(p) & UI_ONLY}
    assert not offenders, offenders


def test_core_imports_without_streamlit_in_a_fresh_interpreter() -> None:
    code = "\n".join([
        "import importlib, pkgutil, sys",
        f"sys.path.insert(0, {str(ROOT / 'src')!r})",
        "import {{package}}",
        "for m in pkgutil.iter_modules({{package}}.__path__):",
        "    if m.name != 'ui':",
        "        importlib.import_module('{{package}}.' + m.name)",
        "assert 'streamlit' not in sys.modules and 'plotly' not in sys.modules",
    ])
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr


def test_render_never_sets_page_config_or_navigation() -> None:
    for path in UI.rglob("*.py"):
        if path.name in {"signal_theme.py", "signal_font.py"}:
            continue
        source = path.read_text(encoding="utf-8")
        for call in ("st.set_page_config(", "st.navigation(", "st.Page("):
            assert call not in source, (path.name, call)


def _widgets(app: AppTest) -> list:
    return [*app.radio, *app.selectbox, *app.multiselect, *app.checkbox, *app.button, *app.slider,
            *app.number_input, *app.text_input, *app.text_area, *app.toggle, *app.date_input]


def test_render_runs_without_set_page_config_and_keys_are_namespaced() -> None:
    app = AppTest.from_string(RENDER, default_timeout=120).run()
    assert not app.exception, [e.value for e in app.exception]
    pages = app.sidebar.radio(key="{{key}}:page").options
    for page in pages:
        app.sidebar.radio(key="{{key}}:page").set_value(page).run()
        assert not app.exception, (page, [e.value for e in app.exception])
        unkeyed = [(type(w).__name__, w.label) for w in _widgets(app) if not (w.key or "").startswith("{{key}}:")]
        assert not unkeyed, (page, unkeyed)


def test_hub_mode_writes_nothing_and_makes_no_network_calls(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    import socket

    def no_network(*args, **kwargs):
        raise AssertionError("network call in Hub mode")

    monkeypatch.setenv("SIGNAL_HUB", "1")
    for name in ("HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "XDG_DATA_HOME", "XDG_CACHE_HOME"):
        monkeypatch.setenv(name, str(tmp_path / "home"))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(socket.socket, "connect", no_network)
    app = AppTest.from_string(RENDER, default_timeout=120).run()
    for page in app.sidebar.radio(key="{{key}}:page").options:
        app.sidebar.radio(key="{{key}}:page").set_value(page).run()
        assert not app.exception, (page, [e.value for e in app.exception])
    written = [p for p in tmp_path.rglob("*") if p.is_file()]
    assert not written, written
    assert os.environ["SIGNAL_HUB"] == "1"
