from pathlib import Path

from streamlit.testing.v1 import AppTest

from hub.registry import FAMILIES, load

ROOT = Path(__file__).resolve().parents[1]


def _home() -> None:
    from hub import home, theme
    from hub.registry import load

    theme.apply()
    home.render(load())


def _placeholder() -> None:
    from dataclasses import replace

    from hub import theme
    from hub.pages import page_function
    from hub.registry import load

    theme.apply()
    # Every app is embedded today; check the coming-soon card with a private, not-yet-released copy of one entry.
    app = replace(next(a for a in load() if a.slug == "prospect"), mode="coming_soon", tag=None, public=False)
    page_function(app)()


def _markdown(app: AppTest) -> str:
    return "\n".join(str(item.value) for item in app.markdown)


def test_front_page_renders_every_section() -> None:
    app = AppTest.from_function(_home, default_timeout=60)
    app.run()
    assert not app.exception, [e.value for e in app.exception]
    text = _markdown(app)
    for expected in ("Nineteen decisions", "How every app works", "Customers in practice", "How it's built",
                     "freddo.ulrikerlingsen.com", "AGPL-3.0-or-later", "fictional"):
        assert expected in text, expected
    assert text.count('class="hub-tool ') == len(load())  # one card per app, all linked
    assert "Creator Signal" not in text


def test_front_page_is_honest_about_traction_and_ai() -> None:
    app = AppTest.from_function(_home, default_timeout=60)
    app.run()
    text = _markdown(app)
    assert "AI-assisted development" in text
    assert "no real-user or traction claims" in text
    assert "no telemetry" in text.lower()


def test_search_filters_the_cards() -> None:
    app = AppTest.from_function(_home, default_timeout=60)
    app.run()
    app.text_input(key="hub:q").set_value("conjoint").run()
    text = _markdown(app)
    assert 'href="./choice"' in text
    assert 'href="./track"' not in text
    app.text_input(key="hub:q").set_value("no such method").run()
    assert "No tool matches" in _markdown(app)


def test_family_pills_filter_the_groups() -> None:
    app = AppTest.from_function(_home, default_timeout=60)
    app.run()
    app.session_state["hub:family"] = "Decide"
    app.run()
    text = _markdown(app)
    assert 'href="./experiment"' in text
    assert 'href="./worth"' not in text


def test_hub_sidebar_lists_every_app_by_family() -> None:
    app = AppTest.from_file(str(ROOT / "hub" / "app.py"), default_timeout=60)
    app.run()
    assert not app.exception, [e.value for e in app.exception]
    assert [e.label for e in app.sidebar.expander] == list(FAMILIES)
    sidebar = " ".join(str(m.value) for m in app.sidebar.markdown)
    assert "19 marketing evidence tools" in sidebar
    assert "freddo.ulrikerlingsen.com" in sidebar
    app.sidebar.text_input(key="hub:find").set_value("conjoint").run()
    assert [e.label for e in app.sidebar.expander] == ["Research"]


def test_private_apps_show_no_source_link() -> None:
    app = AppTest.from_function(_placeholder, default_timeout=60)
    app.run()
    assert not app.exception
    text = _markdown(app)
    assert "Coming to the Hub with its v1 release" in text
    assert "github.com/UlrikErlingsen/b2b-prospecting" not in text
