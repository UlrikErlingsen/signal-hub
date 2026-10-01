"""Signal Hub front page (design: Claude Design 'Signal Hub Page')."""

from __future__ import annotations

from html import escape

import streamlit as st

from hub import theme
from hub.registry import App, FAMILIES, by_family

sig = theme.sig
GITHUB_PROFILE = "https://github.com/UlrikErlingsen"
HUB_REPO = "https://github.com/UlrikErlingsen/signal-hub"
FREDDO_DEMO = "https://freddo.ulrikerlingsen.com"
FEATURED = ("worth", "choice", "experiment")
ASKS = [
    ("What are my customers worth?", "worth"),
    ("What should I charge?", "tag"),
    ("Did my test work?", "experiment"),
    ("Where should the budget go?", "alloc"),
    ("Is the brand growing?", "track"),
    ("Who are my segments?", "segment"),
    ("What are people saying?", "text"),
    ("Which companies should I call?", "prospect"),
]
STEPS = [
    ("brand", "Bring your data", "Excel, CSV or JSON. Or start from the fictional demo that is already loaded."),
    ("market", "Check the contract", "The app validates columns, sizes and definitions, and says plainly what it rejects."),
    ("customer", "Estimate with intervals", "A named method, with the uncertainty and any warnings next to the number."),
    ("decide", "Export the evidence", "Download results as Excel or JSON, ready to show and to question."),
]
_WORDS = {10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen", 15: "Fifteen", 16: "Sixteen",
          17: "Seventeen", 18: "Eighteen", 19: "Nineteen", 20: "Twenty", 21: "Twenty-one", 22: "Twenty-two"}


def _number(n: int) -> str:
    return _WORDS.get(n, str(n))


def _slug(app: App) -> str:
    return f"{app.key}signal"


def _href(app: App) -> str:
    """Relative link to the app's page inside the Hub (url_path = slug)."""
    return f"./{app.slug}"


def _hero(apps: list[App]) -> None:
    chips = "".join(theme.chip(f, theme.fam(f)["600"]) for f in FAMILIES)
    st.markdown(
        f"""<section class="hub-hero">
<div><div class="hub-row" style="gap:12px">{theme.mark("signalhub", 44)}<span class="hub-eyebrow">Signal Hub</span></div>
<h1>{_number(len(apps))} decisions, <span class="hl">one question each.</span></h1></div>
<div><p>Open-source, local-first marketing tools that show their uncertainty instead of hiding it. Each one names its
method, says what it cannot tell you, and runs on fictional demo data the moment you open it.</p>
<div class="hub-row" style="margin-bottom:1rem">
<a class="hub-btn primary" href="{HUB_REPO}" target="_blank" rel="noopener noreferrer">Signal Hub on GitHub</a>
<a class="hub-btn" href="https://github.com/topics/signal-suite" target="_blank" rel="noopener noreferrer">All repos</a></div>
<div class="hub-row">{chips}</div></div></section>""",
        unsafe_allow_html=True,
    )


def _featured(apps: dict[str, App]) -> None:
    st.markdown(
        '<div class="hub-section-head"><div><div class="hub-eyebrow">Start here</div><h2>Three apps to try first.</h2>'
        "</div><p>One from Customer, Research and Decide. Each opens with a fictional demo dataset already loaded.</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    cards = []
    for slug in FEATURED:
        a = apps[slug]
        f = theme.fam(a.family)
        tags = "".join(f'<span class="hub-tag">{escape(m)}</span>' for m in a.methods)
        source = (f'<a href="{a.repo_url}" target="_blank" rel="noopener noreferrer" style="color:{f["700"]}">'
                  "Source ↗</a>") if a.repo_url else ""
        cards.append(
            f'<article class="hub-feat" style="background:{f["200"]}"><div class="ring" style="background:{f["300"]}">'
            f'</div><div style="position:relative">{theme.mark(_slug(a), 72)}</div><div class="body">'
            f'<p class="q" style="color:{f["700"]}">{escape(a.question)}</p>'
            f'<h3>{escape(a.prefix)} <span style="color:{f["700"]}">Signal</span></h3>'
            f'<p class="d">{escape(a.one_liner)}</p><div class="hub-row" style="gap:6px">{tags}</div>'
            f'<div class="hub-links"><a href="{_href(a)}" target="_self" style="color:{f["800"]}">Open the app →</a>'
            f"{source}</div></div></article>"
        )
    st.markdown(f'<div class="hub-featured">{"".join(cards)}</div>', unsafe_allow_html=True)


def _hub_panel(apps: list[App]) -> None:
    live = sum(a.mode == "embedded" for a in apps)
    points = [
        (sig.FAMILIES["brand"]["600"], "One link", "Every tool behind one menu. No hunting through repos."),
        (sig.FAMILIES["customer"]["600"], "Same rules", "No account, no telemetry, no external AI calls. Uploads "
         "stay in your session's memory."),
        (sig.FAMILIES["decide"]["600"], "Released versions", "Each tool is its own repo and package. The Hub pins "
         "released tags, so unfinished work never lands here."),
    ]
    html = "".join(f'<div class="hub-point"><span class="hub-dot" style="background:{c}"></span><b>{t}</b>'
                   f'<span class="d">{d}</span></div>' for c, t, d in points)
    st.markdown(
        f'<section class="hub-panel"><div class="hub-eyebrow">The Signal Hub app</div>'
        f"<h2>{_number(live)} tools live. <span class='hl'>One app.</span></h2>"
        f'<p class="lead">Signal Hub brings the suite into a single Streamlit app with the same look and the same '
        f"evidence rules throughout. The Norwegian-market tools join as they reach v1.</p>"
        f'<div class="hub-points">{html}</div></section>',
        unsafe_allow_html=True,
    )


def _find(apps: dict[str, App]) -> None:
    st.markdown('<div class="hub-section-head"><div><div class="hub-eyebrow">Find your app</div>'
                "<h2>What do you need to know?</h2></div></div>", unsafe_allow_html=True)
    labels = [label for label, _ in ASKS]
    choice = st.pills("Question", labels, default=labels[0], key="hub:ask", label_visibility="collapsed")
    slug = dict(ASKS).get(choice or labels[0], "worth")
    a = apps[slug]
    f = theme.fam(a.family)
    if a.mode == "embedded":
        cta = f'<a class="hub-btn light" href="{_href(a)}" target="_self">Open {escape(a.product)} →</a>'
    else:
        cta = '<span class="hub-btn light" style="opacity:.85">Coming with v1</span>'
    st.markdown(
        f'<div class="hub-pick" style="background:{f["800"]}"><div class="ring" style="background:{f["700"]}"></div>'
        f"<div>{theme.mark(_slug(a), 104)}</div><div>"
        f'<span class="q" style="color:{f["300"]}">{escape(a.family)} · {escape(a.question)}</span>'
        f'<h3>{escape(a.prefix)} <span style="color:{f["300"]}">Signal</span></h3>'
        f'<p style="color:{f["200"]}">{escape(a.one_liner)}</p>{cta}</div></div>',
        unsafe_allow_html=True,
    )


def _steps() -> None:
    rows = []
    for n, (family, title, body) in enumerate(STEPS, start=1):
        f = sig.FAMILIES[family]
        rows.append(f'<div class="hub-step" style="background:{f["300"]}"><span class="n" style="background:{f["700"]}">'
                    f'{n}</span><span><b>{title}</b><span class="d">{body}</span></span></div>')
    st.markdown(
        f'<section class="hub-panel dark"><div class="hub-eyebrow" style="color:{sig.FAMILIES["market"]["300"]}">'
        f"How every app works</div><h2>Same four steps, whichever question you bring.</h2>"
        f'<div class="hub-steps">{"".join(rows)}</div></section>',
        unsafe_allow_html=True,
    )


def _suite(apps: list[App]) -> None:
    columns = []
    for family, members in by_family(apps).items():
        f = theme.fam(family)
        rows = []
        for a in members:
            name = f'<b>{escape(a.prefix)} <span style="color:{f["700"]}">Signal</span></b>'
            if a.mode == "embedded":
                rows.append(f'<a class="hub-app" href="{_href(a)}" target="_self">{theme.mark(_slug(a), 40)}'
                            f"<span>{name}<small>{escape(a.question)}</small></span></a>")
            else:
                rows.append(f'<div class="hub-app">{theme.mark(_slug(a), 40)}<span>{name}'
                            f'<span class="hub-soon">Coming with v1</span><small>{escape(a.question)}</small></span></div>')
        columns.append(f'<div class="hub-fam"><h3><span class="hub-dot" style="background:{f["600"]};width:14px;'
                       f'height:14px;margin-right:10px"></span>{family}</h3>{"".join(rows)}</div>')
    st.markdown(f'<section class="hub-panel"><h2 style="font-size:clamp(1.8rem,2.8vw,2.6rem) !important">The full suite'
                f'</h2><div class="hub-suite">{"".join(columns)}</div></section>', unsafe_allow_html=True)


def _practice_and_build() -> None:
    m = sig.FAMILIES["market"]
    st.markdown(
        f"""<section class="hub-panel" style="background:{m['200']}">
<div class="hub-eyebrow" style="color:{m['800']}">Customers in practice</div>
<h2>From a market list to <span style="color:{m['700']}">managed customers.</span></h2>
<p class="lead">Prospect Signal finds the companies that fit, from open Brønnøysund data. Export the shortlist as CSV.
Freddo CRM, a separate product, then manages those customers and their follow-ups. Freddo is not part of the Hub.</p>
<div class="hub-row"><a class="hub-btn dark" href="{FREDDO_DEMO}" target="_blank" rel="noopener noreferrer">
See the Freddo CRM demo ↗</a></div></section>
<section class="hub-two">
<div><h2>How it's built.</h2><p>Every tool is its own repository and Python package. The Hub installs released
versions only and contains no business logic, data processing or database. There is no telemetry and no account.
The suite is built with AI-assisted development: Ulrik Erlingsen specifies, reviews and ships every release. It is
new, and it has no real-user or traction claims to make yet.</p></div>
<div><h2>The apps hand off instead of overlapping.</h2><p>A tracking change in Track Signal is not a causal effect,
so it points to Experiment Signal. Construct scores need Measure Signal evidence first. Every app names its siblings
under "Read this first". Want one on your own machine? Each repo has a double-click launcher.</p></div>
</section>
<footer class="hub-foot"><span>Signal · by <a href="https://ulrikerlingsen.com" target="_blank"
rel="noopener noreferrer">Ulrik Erlingsen</a> · <a href="{GITHUB_PROFILE}" target="_blank" rel="noopener noreferrer">
GitHub</a></span><span>All data in the demos is fictional · AGPL-3.0-or-later</span></footer>""",
        unsafe_allow_html=True,
    )


def render(apps: list[App]) -> None:
    index = {a.slug: a for a in apps}
    _hero(apps)
    _featured(index)
    _hub_panel(apps)
    _find(index)
    _steps()
    _suite(apps)
    _practice_and_build()
