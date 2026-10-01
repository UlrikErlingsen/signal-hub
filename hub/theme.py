"""Signal Hub's look: the shared signal_theme (Brand accent, as on the suite page) plus the Hub's own blocks."""

from __future__ import annotations

from functools import lru_cache
from html import escape
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
THEME_DIR = ROOT / "signal-theme"
if str(THEME_DIR) not in sys.path:
    sys.path.insert(0, str(THEME_DIR))

import signal_theme as sig  # noqa: E402

MARKS = THEME_DIR / "assets" / "marks"
HUB_ICON = MARKS / "signalhub-mark-64.png"
HUB_KEY = "track"  # any Brand-family key: the Hub's chrome uses the Brand accent, like the suite page
FAMILY_KEYS = {"Brand": "brand", "Market": "market", "Customer": "customer", "Research": "research", "Decide": "decide"}
_METADATA = re.compile(r"<metadata>.*?</metadata>", re.DOTALL)


def fam(family: str) -> dict:
    """Family ramp for a display family name ('Customer')."""
    return sig.FAMILIES[FAMILY_KEYS[family]]


@lru_cache(maxsize=64)
def _svg(slug: str) -> str:
    svg = (MARKS / f"{slug}-mark.svg").read_text(encoding="utf-8")
    return _METADATA.sub("", svg)  # drop the provenance manifest when inlining (it is ~7 kB per mark)


def mark(slug: str, size: int = 40) -> str:
    """Inline SVG mark. slug: 'signalhub' or an app slug such as 'worthsignal'."""
    return _svg(slug).replace("<svg ", f'<svg width="{size}" height="{size}" aria-hidden="true" ', 1)


def page_config() -> dict:
    return {"page_title": "Signal Hub | Open, local-first marketing evidence", "page_icon": str(HUB_ICON),
            "layout": "wide", "initial_sidebar_state": "expanded"}


def css() -> str:
    """Hub chrome and front-page blocks. Added after signal_theme's own CSS."""
    c = sig.CORE
    b = sig.FAMILIES["brand"]
    return f"""
<style>
[data-testid="stSidebarNav"] {{ padding-top:.4rem; }}
[data-testid="stSidebarNav"] a {{ border-radius:999px; }}
[data-testid="stSidebarNav"] a span {{ color:{c['sidebar_text']} !important; }}
[data-testid="stSidebarNav"] a:hover {{ background:rgba(249,244,237,.08); }}
[data-testid="stSidebarNav"] a[aria-current="page"] {{ background:rgba(249,244,237,.14); }}
[data-testid="stNavSectionHeader"] span, [data-testid="stSidebarNavSeparator"] {{ color:{c['sidebar_muted']} !important; }}
[data-testid="stSidebarNavSectionHeader"] {{ color:{c['sidebar_muted']} !important; letter-spacing:.12em;
  text-transform:uppercase; font-size:.7rem; font-weight:700; }}
.hub-eyebrow {{ font-size:.74rem; font-weight:700; letter-spacing:.16em; color:{c['muted']}; text-transform:uppercase; }}
.hub-hero {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr)); gap:2.4rem;
  align-items:end; padding:1rem 0 2.6rem; }}
.hub-hero h1 {{ font-size:clamp(2.6rem,6vw,5.6rem) !important; line-height:.95 !important; letter-spacing:-.05em !important;
  margin:1rem 0 0 !important; padding:0 !important; text-wrap:balance; }}
.hub-hero h1 .hl {{ color:{b['700']}; }}
.hub-hero p {{ font-size:1.12rem; line-height:1.6; color:#474238; margin:0 0 1.1rem; max-width:34rem; }}
.hub-row {{ display:flex; flex-wrap:wrap; gap:.55rem; align-items:center; }}
.hub-btn {{ padding:.7rem 1.35rem; border-radius:999px; font-weight:700; white-space:nowrap; text-decoration:none !important;
  border:1px solid {c['line']}; color:{c['text']} !important; }}
.hub-btn:hover {{ background:rgba(32,30,29,.07); }}
.hub-btn.primary {{ background:{b['600']}; border-color:transparent; color:{c['paper']} !important; }}
.hub-btn.primary:hover {{ background:{b['700']}; }}
.hub-btn.dark {{ background:{c['sidebar']}; border-color:transparent; color:{c['paper']} !important; }}
.hub-btn.light {{ background:{c['paper']}; border-color:transparent; color:{c['text']} !important; font-weight:800; }}
.hub-chip {{ display:inline-flex; align-items:center; gap:6px; white-space:nowrap; padding:.3rem .8rem; border-radius:999px;
  background:{c['paper']}; font-size:.85rem; color:{c['text']}; }}
.hub-dot {{ display:inline-block; width:10px; height:10px; border-radius:50%; flex:none; }}
.hub-panel {{ padding:clamp(1.6rem,3.6vw,3rem); border-radius:40px; background:{c['paper']}; margin:0 0 2.4rem; }}
.hub-panel.dark {{ background:{c['sidebar']}; color:{c['paper']}; }}
.hub-panel h2 {{ font-size:clamp(2rem,3.6vw,3.2rem) !important; line-height:1 !important; letter-spacing:-.045em !important;
  margin:.5rem 0 1rem !important; padding:0 !important; }}
.hub-panel.dark h2 {{ color:{c['paper']} !important; }}
.hub-panel h2 .hl {{ color:{b['700']}; }}
.hub-panel p.lead {{ font-size:1.08rem; line-height:1.65; color:#474238; max-width:40rem; margin:0 0 1.2rem; }}
.hub-points {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr)); gap:14px; margin:1.2rem 0; }}
.hub-point {{ display:flex; flex-direction:column; gap:6px; padding:18px 20px; border-radius:24px; background:{c['bg']}; }}
.hub-point b {{ font-size:1.08rem; }} .hub-point span.d {{ font-size:.94rem; line-height:1.45; color:{c['muted']}; }}
.hub-section-head {{ display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap:1rem 2rem;
  margin:1rem 0 1.2rem; }}
.hub-section-head h2 {{ font-size:clamp(2rem,3.6vw,3.2rem) !important; line-height:1 !important; letter-spacing:-.045em !important;
  margin:.5rem 0 0 !important; padding:0 !important; }}
.hub-section-head p {{ max-width:28rem; color:{c['muted']}; margin:0; line-height:1.55; }}
.hub-featured {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr)); gap:1.1rem; margin-bottom:.6rem; }}
.hub-feat {{ position:relative; overflow:hidden; min-height:24rem; display:flex; flex-direction:column; gap:1rem; padding:2rem;
  border-radius:32px; color:{c['text']}; }}
.hub-feat .ring {{ position:absolute; width:240px; height:240px; right:-90px; top:-100px; border-radius:50%; }}
.hub-feat .body {{ position:relative; margin-top:auto; display:flex; flex-direction:column; gap:.8rem; }}
.hub-feat .q {{ font-size:.74rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; margin:0; }}
.hub-feat h3 {{ font-size:clamp(1.9rem,2.8vw,2.6rem) !important; letter-spacing:-.045em !important; line-height:1 !important;
  margin:0 !important; padding:0 !important; }}
.hub-feat p.d {{ font-size:.97rem; line-height:1.55; color:#474238; margin:0; }}
.hub-tag {{ white-space:nowrap; padding:.26rem .72rem; border-radius:999px; font-size:.76rem; background:rgba(255,255,255,.6);
  color:#474238; }}
.hub-links {{ display:flex; flex-wrap:wrap; gap:1rem; font-weight:700; }}
.hub-links a {{ text-decoration:none !important; }}
.hub-steps {{ display:flex; flex-direction:column; gap:10px; }}
.hub-step {{ display:grid; grid-template-columns:52px minmax(0,1fr); gap:16px; align-items:center; padding:14px 20px 14px 14px;
  border-radius:26px; color:{c['text']}; }}
.hub-step .n {{ width:52px; height:52px; border-radius:50%; display:grid; place-items:center; color:{c['paper']};
  font-size:1.35rem; font-weight:800; }}
.hub-step b {{ font-size:1.08rem; display:block; }} .hub-step span.d {{ font-size:.93rem; line-height:1.45; color:#474238; }}
.hub-pick {{ position:relative; overflow:hidden; display:grid; grid-template-columns:auto minmax(0,1fr); gap:1.1rem 1.8rem;
  align-items:start; padding:clamp(1.6rem,3vw,2.6rem); border-radius:36px; color:{c['paper']}; margin:.4rem 0 .8rem; }}
.hub-pick .ring {{ position:absolute; width:300px; height:300px; right:-90px; bottom:-150px; border-radius:50%; }}
.hub-pick > * {{ position:relative; }}
.hub-pick h3 {{ font-size:clamp(1.9rem,3.2vw,2.8rem) !important; letter-spacing:-.045em !important; line-height:1 !important;
  margin:.35rem 0 .6rem !important; padding:0 !important; color:{c['paper']} !important; }}
.hub-pick .q {{ font-size:.74rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase; }}
.hub-pick p {{ margin:0 0 1rem; line-height:1.55; max-width:42rem; }}
.hub-suite {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr)); gap:2rem 2.6rem; }}
.hub-fam h3 {{ display:flex; align-items:center; gap:10px; font-size:1.3rem !important; margin:0 0 .5rem !important;
  padding:0 !important; letter-spacing:-.02em !important; }}
.hub-app {{ display:grid; grid-template-columns:40px minmax(0,1fr); gap:12px; align-items:center; padding:.55rem .6rem;
  border-radius:20px; color:{c['text']} !important; text-decoration:none !important; }}
a.hub-app:hover {{ background:#eee7db; }}
.hub-app b {{ font-weight:700; }} .hub-app small {{ display:block; font-size:.86rem; color:{c['muted']}; line-height:1.4; }}
.hub-soon {{ margin-left:.4rem; padding:.12rem .55rem; border-radius:999px; font-size:.7rem; font-weight:700;
  background:{c['warn_bg']}; color:{c['warn_text']}; white-space:nowrap; }}
.hub-two {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr)); gap:2.4rem; margin:2.4rem 0; }}
.hub-two h2 {{ font-size:clamp(1.6rem,2.4vw,2.2rem) !important; letter-spacing:-.04em !important; line-height:1.05 !important;
  margin:0 0 .8rem !important; padding:0 !important; }}
.hub-two p {{ line-height:1.6; color:#474238; }}
.hub-foot {{ display:flex; flex-wrap:wrap; justify-content:space-between; gap:1rem; padding:1.4rem 0 0; margin-top:2rem;
  border-top:1px solid {c['line']}; font-size:.85rem; color:{c['muted']}; }}
.hub-foot a {{ color:{c['muted']} !important; }}
.hub-apphead {{ display:flex; flex-wrap:wrap; align-items:center; gap:.5rem 1rem; margin:-2.4rem 0 1rem; font-size:.82rem;
  color:{c['muted']}; }}
.hub-apphead b {{ color:{c['text']}; }}
.hub-apphead a {{ font-weight:700; text-decoration:none !important; }}
.hub-card {{ padding:2rem; border-radius:32px; background:{c['paper']}; max-width:820px; }}
.hub-card h2 {{ margin:.6rem 0 .6rem !important; padding:0 !important; }}
</style>"""


def apply() -> None:
    import streamlit as st

    sig.apply(HUB_KEY)
    st.markdown(css(), unsafe_allow_html=True)


def chip(label: str, color: str) -> str:
    return f'<span class="hub-chip"><span class="hub-dot" style="background:{color}"></span>{escape(label)}</span>'
