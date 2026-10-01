"""Smoke tests: every embedded app renders its demo inside the Hub wrapper. Needs all apps installed."""

import importlib.util

import pytest
from streamlit.testing.v1 import AppTest

from hub.registry import load

EMBEDDED = [a for a in load() if a.mode == "embedded"]
pytestmark = pytest.mark.apps


@pytest.mark.parametrize("app", EMBEDDED, ids=lambda a: a.slug)
def test_app_honours_the_contract(app) -> None:
    if importlib.util.find_spec(app.package) is None:
        pytest.fail(f"{app.dist} is not installed; pip install -r requirements.txt")
    from hub.pages import load_ui

    module = load_ui(app)
    assert module.APP_INFO["product"] == app.product
    assert f"v{module.APP_INFO['version']}" == app.tag, "apps.yaml tag and installed version differ"


def _run(slug: str) -> None:
    from hub import theme
    from hub.pages import render_app
    from hub.registry import load as load_registry

    theme.apply()
    render_app(next(a for a in load_registry() if a.slug == slug))


@pytest.mark.parametrize("app", EMBEDDED, ids=lambda a: a.slug)
def test_app_renders_its_demo_inside_the_hub(app) -> None:
    script = AppTest.from_function(_run, args=(app.slug,), default_timeout=180)
    script.run()
    assert not script.exception, [e.value for e in script.exception]
    text = "\n".join(str(m.value) for m in script.markdown)
    assert "not available in this build" not in text
    assert "Something went wrong in this tool" not in text
