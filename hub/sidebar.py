"""The Hub's own sidebar (design: 'Signal Hub Home v2'): lockup, tool search, one collapsible group per family.

st.navigation runs hidden; this draws the menu with st.page_link so every entry can carry its app's mark. An
embedded app's own sidebar controls (page picker, uploads) follow below it, and footer() closes the sidebar after
the page has run.
"""

from __future__ import annotations

import streamlit as st

from hub import theme
from hub.registry import App, by_family

HUB_REPO = "https://github.com/UlrikErlingsen/signal-hub"
FREDDO_DEMO = "https://freddo.ulrikerlingsen.com"


def matches(app: App, query: str) -> bool:
    """Case-insensitive search over name, question, methods and family."""
    q = query.strip().lower()
    return not q or q in " ".join([app.product, app.question, " ".join(app.methods), app.family]).lower()


def css(apps: list[App], current: str | None = None) -> str:
    """Marks as CSS variables, then one rule per app and per family group (keyed containers: .st-key-<key>).

    st.page_link does not mark the current page in the DOM, so the open entry is highlighted from `current`.
    """
    c = theme.sig.CORE
    marks = "".join(f"--hub-m-{a.slug}:url('{theme.mark_uri(a.key + 'signal')}');" for a in apps)
    rules = []
    for a in apps:
        rules.append(f".st-key-hub-nav-{a.slug} a::before {{ background-image:var(--hub-m-{a.slug}); }}")
    for family, members in by_family(apps).items():
        f = theme.fam(family)
        slug = family.lower()
        stack = ",".join(f"var(--hub-m-{a.slug})" for a in members)
        offsets = ",".join(f"{i * 13}px 0" for i in range(len(members)))
        rules.append(
            f".st-key-hub-fam-{slug} summary::before {{ background:{f['600']}; }}"
            f".st-key-hub-fam-{slug} details:not([open]) summary::after {{ background-image:{stack};"
            f" background-position:{offsets}; width:{18 + 13 * (len(members) - 1)}px; }}"
        )
        rules.extend(f".st-key-hub-nav-{a.slug} a {{ background:{f['700']} !important; }}"
                     for a in members if a.slug == current)
    if current is None:
        rules.append(".st-key-hub-nav-home a { background:rgba(249,244,237,.14) !important; }")
    return f"""<style>
:root {{ {marks} }}
[data-testid="stSidebarHeader"] {{ position:absolute; top:0; right:0; z-index:3; height:auto; padding:22px 14px 0 0 !important; }}
[data-testid="stLogoSpacer"] {{ display:none; }}
[data-testid="stSidebarUserContent"] {{ padding-top:20px; }}
.hub-lockup {{ display:flex; align-items:center; gap:10px; margin:0 0 .2rem; padding-right:2rem; }}
.hub-lockup svg {{ flex:none; }}
.hub-lockup .name {{ font-size:1.2rem; font-weight:800; letter-spacing:-.035em; line-height:1; color:{c['sidebar_text']}; }}
.hub-lockup .name span {{ color:{theme.fam('Brand')['300']} !important; }}
.hub-lockup .sub {{ font-size:.74rem; color:{c['sidebar_muted']} !important; margin-top:4px; }}
.st-key-hub-find [data-testid="stTextInputRootElement"] {{ height:38px; border-radius:999px;
  background:rgba(249,244,237,.07) !important; border:1px solid rgba(249,244,237,.12) !important; }}
.st-key-hub-find [data-testid="stTextInputRootElement"] * {{ background:transparent !important; }}
.st-key-hub-find input {{ color:{c['sidebar_text']} !important; background:transparent !important; font-size:.88rem; }}
.st-key-hub-find input::placeholder {{ color:{c['sidebar_muted']}; opacity:1; }}
.st-key-hub-find [data-testid="stTextInputIcon"], .st-key-hub-find [data-testid="stTextInputIcon"] * {{
  color:{c['sidebar_muted']} !important; }}
[class*="st-key-hub-nav-"] a {{ display:flex; align-items:center; gap:10px; min-height:34px; padding:0 10px !important;
  border-radius:12px !important; background:transparent; }}
[class*="st-key-hub-nav-"] a:hover {{ background:rgba(249,244,237,.1) !important; }}
[class*="st-key-hub-nav-"] a::before {{ content:""; width:22px; height:22px; flex:none; background:center/contain no-repeat; }}
[class*="st-key-hub-nav-"] a p, [class*="st-key-hub-nav-"] a span {{ color:{c['sidebar_text']} !important;
  font-size:.9rem !important; font-weight:600; }}
.st-key-hub-nav-home a::before {{ display:none; }}
.st-key-hub-nav-home a {{ height:36px; }}
.st-key-hub-nav-home [data-testid="stPageLink"] {{ position:relative; }}
.st-key-hub-nav-home [data-testid="stPageLink"]::after {{ content:"{len(apps)}"; position:absolute; right:12px; top:50%;
  transform:translateY(-50%); font-size:.75rem; color:{c['sidebar_muted']}; pointer-events:none; }}
[class*="st-key-hub-fam-"] [data-testid="stExpander"] {{ border:0 !important; background:transparent !important; }}
[class*="st-key-hub-fam-"] details {{ border:0 !important; border-radius:14px; background:transparent; }}
[class*="st-key-hub-fam-"] details[open] {{ background:rgba(249,244,237,.04); }}
[class*="st-key-hub-fam-"] summary {{ display:flex; align-items:center; gap:10px; min-height:40px; padding:0 10px !important;
  border-radius:14px; }}
[class*="st-key-hub-fam-"] summary {{ background:transparent !important; }}
[class*="st-key-hub-fam-"] summary:hover {{ background:rgba(249,244,237,.06) !important; }}
[class*="st-key-hub-fam-"] summary > span {{ display:contents; }}
[class*="st-key-hub-fam-"] summary > span > div {{ order:1; flex:1; min-width:0; }}
[class*="st-key-hub-fam-"] summary > span > span {{ order:3; }}
[class*="st-key-hub-fam-"] summary::before {{ content:""; width:10px; height:10px; margin:0 6px; border-radius:50%; flex:none;
  order:0; }}
[class*="st-key-hub-fam-"] summary::after {{ content:""; height:18px; flex:none; order:2;
  background-repeat:no-repeat; background-size:18px 18px; }}
[class*="st-key-hub-fam-"] details[open] summary::after {{ display:none; }}
[class*="st-key-hub-fam-"] summary p, [class*="st-key-hub-fam-"] summary span {{ font-size:.9rem !important; font-weight:700;
  color:{c['sidebar_text']} !important; }}
[class*="st-key-hub-fam-"] summary [data-testid="stIconMaterial"] {{ color:{c['sidebar_muted']} !important; }}
[class*="st-key-hub-fam-"] [data-testid="stExpanderDetails"] {{ padding:0 4px 6px !important; }}
[class*="st-key-hub-fam-"] [data-testid="stVerticalBlock"] {{ gap:2px; }}
.st-key-hub-groups {{ gap:2px; }}
.hub-sidefoot {{ display:flex; flex-direction:column; gap:6px; padding:12px 6px 4px; margin-top:.6rem;
  border-top:1px solid rgba(249,244,237,.1); font-size:.8rem; }}
.hub-sidefoot div {{ display:flex; gap:16px; }}
.hub-sidefoot a {{ color:{c['sidebar_text']} !important; text-decoration:none !important; }}
.hub-sidefoot a:hover {{ color:{theme.fam('Brand')['300']} !important; }}
.hub-sidefoot span {{ color:{c['sidebar_muted']} !important; font-size:.74rem; }}
{chr(10).join(rules)}
</style>"""


def render(apps: list[App], home: st.Page, pages: dict[str, st.Page], current: str | None) -> None:
    """Draw the menu. current: the open app's slug, or None on the home page."""
    with st.sidebar:
        st.markdown(css(apps, current), unsafe_allow_html=True)
        st.markdown(
            f'<div class="hub-lockup">{theme.mark("signalhub", 34)}<div><div class="name">Signal <span>Hub</span></div>'
            f'<div class="sub">{len(apps)} marketing evidence tools</div></div></div>',
            unsafe_allow_html=True,
        )
        query = st.text_input("Find a tool", key="hub:find", placeholder="Find a tool", type="search", live=True,
                              icon=":material/search:",
                              label_visibility="collapsed") or ""
        with st.container(key="hub-nav-home"):
            st.page_link(home, label="All tools", icon=":material/grid_view:")
        found = False
        with st.container(key="hub-groups"):
            for family, members in by_family(apps).items():
                shown = [a for a in members if matches(a, query)]
                if not shown:
                    continue
                found = True
                is_open = bool(query.strip()) or any(a.slug == current for a in shown)
                with st.container(key=f"hub-fam-{family.lower()}"):
                    with st.expander(family, expanded=is_open):
                        for a in shown:
                            with st.container(key=f"hub-nav-{a.slug}"):
                                st.page_link(pages[a.slug], label=a.prefix + ("" if a.mode == "embedded" else " · soon"))
        if not found:
            st.caption(f"No tool matches “{query.strip()}”.")


def footer() -> None:
    """Links at the end of the sidebar, after the open app's own controls."""
    st.sidebar.markdown(
        f'<div class="hub-sidefoot"><div><a href="{HUB_REPO}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>'
        f'<a href="{FREDDO_DEMO}" target="_blank" rel="noopener noreferrer">Freddo CRM ↗</a></div>'
        f"<span>All demo data is fictional</span></div>",
        unsafe_allow_html=True,
    )

