from streamlit.testing.v1 import AppTest


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
    for expected in ("Nineteen decisions", "Three apps to try first", "What do you need to know?",
                     "Same four steps", "The full suite", "Customers in practice", "How it's built",
                     "freddo.ulrikerlingsen.com", "AGPL-3.0-or-later", "fictional"):
        assert expected in text, expected
    assert "Creator Signal" not in text


def test_front_page_is_honest_about_traction_and_ai() -> None:
    app = AppTest.from_function(_home, default_timeout=60)
    app.run()
    text = _markdown(app)
    assert "AI-assisted development" in text
    assert "no real-user or traction claims" in text
    assert "no telemetry" in text.lower()


def test_question_picker_switches_the_card() -> None:
    app = AppTest.from_function(_home, default_timeout=60)
    app.run()
    assert "Open Worth Signal" in _markdown(app)
    app.session_state["hub:ask"] = "Did my test work?"
    app.run()
    assert "Open Experiment Signal" in _markdown(app)


def test_private_apps_show_no_source_link() -> None:
    app = AppTest.from_function(_placeholder, default_timeout=60)
    app.run()
    assert not app.exception
    text = _markdown(app)
    assert "Coming to the Hub with its v1 release" in text
    assert "github.com/UlrikErlingsen/b2b-prospecting" not in text
