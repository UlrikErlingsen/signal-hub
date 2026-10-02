"""Signal Hub front page (design: Claude Design 'Signal Hub Home v2').

Header, a sticky search and family filter, every tool as a card grouped by family, the four steps every app shares,
"Customers in practice" (Prospect Signal → Freddo CRM), "How it's built" and the footer.
"""

from __future__ import annotations

from html import escape

import streamlit as st

from hub import theme
from hub.registry import App, FAMILIES, by_family, count_word
from hub.sidebar import FREDDO_DEMO, HUB_REPO, matches

sig = theme.sig
GITHUB_PROFILE = "https://github.com/UlrikErlingsen"
ALL = "All"
STEPS = [
    ("brand", "Bring your data", "Excel, CSV or JSON. Or start from the fictional demo that is already loaded."),
    ("market", "Check the contract", "The app validates columns, sizes and definitions, and says plainly what it rejects."),
    ("customer", "Estimate with intervals", "A named method, with the uncertainty and any warnings next to the number."),
    ("decide", "Export the evidence", "Download results as Excel or JSON, ready to show and to question."),
]
def _href(app: App) -> str:
    """Relative link to the app's page inside the Hub (url_path = slug)."""
    return f"./{app.slug}"


def _header(apps: list[App]) -> None:
    st.markdown(
        f"""<section class="hub-head"><div>
<div class="hub-eyebrow">Signal Hub</div>
<h1>{count_word(len(apps))} decisions, <span class="hl">one question each.</span></h1>
<p>Open-source, local-first marketing tools that show their uncertainty instead of hiding it. Each one names its
method, says what it cannot tell you, and runs on fictional demo data the moment you open it.</p></div>
<div class="hub-row"><a class="hub-btn" href="{HUB_REPO}" target="_blank" rel="noopener noreferrer">Source on GitHub</a>
<a class="hub-btn" href="https://github.com/topics/signal-suite" target="_blank" rel="noopener noreferrer">All repos</a>
</div></section>""",
        unsafe_allow_html=True,
    )


def _filters(apps: list[App]) -> tuple[str, str]:
    """Search box and family pills. Returns (query, family or ALL)."""
    counts = {ALL: len(apps), **{f: len(m) for f, m in by_family(apps).items()}}
    with st.container(key="hub-filter", horizontal=True, vertical_alignment="center"):
        query = st.text_input("Search tools", key="hub:q", placeholder="Search by question, method or name",
                              type="search", live=True, icon=":material/search:", label_visibility="collapsed",
                              width=420) or ""
        family = st.pills("Family", [ALL, *FAMILIES], key="hub:family", default=ALL, required=True, wrap=True,
                          format_func=lambda f: f"{f}  {counts[f]}", label_visibility="collapsed")
    return query, family or ALL


def _card(a: App) -> str:
    f = theme.fam(a.family)
    tags = "".join(f'<span class="hub-mtag">{escape(m)}</span>' for m in a.methods)
    soon = "" if a.mode == "embedded" else '<span class="hub-soon">Coming with v1</span>'
    inner = (f'<div class="top">{theme.mark(a.key + "signal", 44)}<div class="nm">{escape(a.prefix)} '
             f'<span style="color:{f["700"]}">Signal</span>{soon}</div><span class="go" style="color:{f["700"]}">→</span>'
             f'</div><p>{escape(a.question)}</p><div class="tags">{tags}</div>')
    if a.mode != "embedded":
        return f'<div class="hub-tool">{inner}</div>'
    return f'<a class="hub-tool fam-{a.family.lower()}" href="{_href(a)}" target="_self">{inner}</a>'


def _groups(apps: list[App], query: str, family: str) -> None:
    sections = []
    for name, members in by_family(apps).items():
        if family not in (ALL, name):
            continue
        shown = [a for a in members if matches(a, query)]
        if not shown:
            continue
        f = theme.fam(name)
        count = "1 tool" if len(shown) == 1 else f"{len(shown)} tools"
        sections.append(
            f'<section class="hub-group"><div class="hub-group-head"><span class="hub-dot" style="background:{f["600"]}">'
            f'</span><h2>{name}</h2><span class="n">{count}</span></div>'
            f'<div class="hub-tools">{"".join(_card(a) for a in shown)}</div></section>'
        )
    if not sections:
        sections.append(f'<div class="hub-empty">No tool matches “{escape(query.strip())}”. Try a method such as CLV or '
                        "conjoint, or clear the search.</div>")
    st.markdown(f'<div class="hub-groups">{"".join(sections)}</div>', unsafe_allow_html=True)


def _steps() -> None:
    rows = []
    for n, (family, title, body) in enumerate(STEPS, start=1):
        f = sig.FAMILIES[family]
        rows.append(f'<div class="hub-step"><span class="n" style="background:{f["300"]}">{n}</span>'
                    f'<span><b>{title}</b><span class="d">{body}</span></span></div>')
    st.markdown(
        f'<section class="hub-band"><div class="hub-eyebrow" style="color:{sig.FAMILIES["market"]["300"]}">'
        f'How every app works</div><div class="hub-steps">{"".join(rows)}</div></section>',
        unsafe_allow_html=True,
    )


def _practice_and_build() -> None:
    m = sig.FAMILIES["market"]
    st.markdown(
        f"""<section class="hub-two">
<div><div class="hub-eyebrow" style="color:{m['800']}">Customers in practice</div>
<h3>From a market list to <span style="color:{m['700']}">managed customers.</span></h3>
<p>Prospect Signal finds the companies that fit, from open Brønnøysund data. Export the shortlist as CSV. Freddo CRM,
a separate product, then manages those customers and their follow-ups. Freddo is not part of the Hub.</p>
<a class="hub-link" href="{FREDDO_DEMO}" target="_blank" rel="noopener noreferrer" style="color:{m['700']}">See the
Freddo CRM demo ↗</a></div>
<div><div class="hub-eyebrow">How it's built</div>
<h3>The apps hand off instead of overlapping.</h3>
<p>Every tool is its own repository and Python package. The Hub installs released versions only and contains no
business logic, data processing or database. There is no telemetry and no account. The suite is built with
AI-assisted development: Ulrik Erlingsen specifies, reviews and ships every release. It is new, and it has
no real-user or traction claims to make yet.</p></div>
</section>
<footer class="hub-foot"><span>Signal · by <a href="https://ulrikerlingsen.com" target="_blank"
rel="noopener noreferrer">Ulrik Erlingsen</a> · <a href="{GITHUB_PROFILE}" target="_blank" rel="noopener noreferrer">
GitHub</a></span><span>All data in the demos is fictional · AGPL-3.0-or-later</span></footer>""",
        unsafe_allow_html=True,
    )


def render(apps: list[App]) -> None:
    _header(apps)
    query, family = _filters(apps)
    _groups(apps, query, family)
    _steps()
    _practice_and_build()
