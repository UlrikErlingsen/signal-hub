"""One wrapper per app: slim Hub header, then the app's own ui.render(). A crashing app never takes the Hub down."""

from __future__ import annotations

from collections.abc import Callable
from html import escape
import importlib
import os
import traceback

import streamlit as st

from hub import theme
from hub.registry import App

DEBUG = os.getenv("SIGNALHUB_DEBUG") == "1"


def load_ui(app: App):
    """Import <package>.ui and check the contract. Raises ImportError/AttributeError with a clear message."""
    module = importlib.import_module(f"{app.package}.ui")
    if not callable(getattr(module, "render", None)):
        raise AttributeError(f"{app.package}.ui has no render() function")
    info = getattr(module, "APP_INFO", None)
    if not isinstance(info, dict) or "version" not in info:
        raise AttributeError(f"{app.package}.ui has no APP_INFO with a version")
    return module


def _header(app: App, version: str | None) -> None:
    parts = [f"<b>{escape(app.product)}</b>"]
    if version:
        parts.append(f"v{escape(version)}")
    parts.append("Fictional demo data, preloaded")
    if app.repo_url:
        parts.append(f'<a href="{app.repo_url}" target="_blank" rel="noopener noreferrer">Source on GitHub ↗</a>')
    if app.demo_url:
        parts.append(f'<a href="{escape(app.demo_url)}" target="_blank" rel="noopener noreferrer">Standalone demo ↗</a>')
    dot = '<span class="hub-dot" style="background:var(--sg-a600);width:6px;height:6px"></span>'
    st.markdown(f'<div class="hub-apphead">{dot.join(parts)}</div>', unsafe_allow_html=True)


def _problem(app: App, title: str, body: str, exc: BaseException | None = None) -> None:
    link = (f' <a href="{app.repo_url}" target="_blank" rel="noopener noreferrer">Open the repo ↗</a>'
            if app.repo_url else "")
    st.markdown(f'<div class="hub-card"><div class="hub-eyebrow">{escape(app.product)}</div><h2>{escape(title)}</h2>'
                f'<p>{escape(body)}{link}</p></div>', unsafe_allow_html=True)
    if exc is not None and DEBUG:
        with st.expander("Technical details"):
            st.code("".join(traceback.format_exception(exc)))


def render_app(app: App) -> None:
    """Draw one embedded app inside the Hub."""
    try:
        module = load_ui(app)
    except Exception as exc:  # not installed, or not refactored to the contract yet
        _problem(app, "This tool is not available in this build.",
                 "The Hub could not load it. The other tools still work.", exc)
        return
    _header(app, str(module.APP_INFO.get("version", "")))
    try:
        module.render()
    except Exception as exc:  # pragma: no cover - depends on the app
        if type(exc).__name__ in {"StopException", "RerunException"}:  # Streamlit control flow, not an error
            raise
        _problem(app, "Something went wrong in this tool.",
                 "The error stayed inside this page. Try reloading, or open another tool from the menu.", exc)


def render_placeholder(app: App) -> None:
    """Card for an app that is not embedded (yet)."""
    f = theme.fam(app.family)
    if app.mode == "link" and app.demo_url:
        cta = (f'<a class="hub-btn primary" href="{escape(app.demo_url)}" target="_blank" '
               f'rel="noopener noreferrer">Open the standalone demo ↗</a>')
        status = "Runs as its own demo for now."
    else:
        cta = ""
        status = "Coming to the Hub with its v1 release."
    st.markdown(
        f'<div class="hub-card" style="background:{f["200"]}"><div style="display:flex;gap:16px;align-items:center">'
        f'{theme.mark(app.key + "signal", 64)}<div><div class="hub-eyebrow">Signal · {escape(app.family)}</div>'
        f'<h2 style="margin:.2rem 0 0 !important">{escape(app.prefix)} <span style="color:{f["700"]}">Signal</span></h2>'
        f'</div></div><p style="font-size:1.1rem;font-weight:700;margin:1.2rem 0 .4rem">{escape(app.question)}</p>'
        f'<p style="color:#474238;line-height:1.6">{escape(app.one_liner)}</p>'
        f'<p style="color:{f["800"]};font-weight:700">{status}</p><div class="hub-row">{cta}</div></div>',
        unsafe_allow_html=True,
    )


def page_function(app: App) -> Callable[[], None]:
    def page() -> None:
        if app.mode == "embedded":
            render_app(app)
        else:
            render_placeholder(app)

    page.__name__ = f"page_{app.slug}"
    return page
