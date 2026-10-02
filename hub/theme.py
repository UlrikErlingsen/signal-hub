"""Signal Hub's look: the shared signal_theme (Brand accent, as on the suite page) plus the Hub's own blocks."""

from __future__ import annotations

import base64
from functools import lru_cache
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


def mark_uri(slug: str) -> str:
    """The mark as a data URI, for CSS backgrounds (sidebar entries)."""
    return "data:image/svg+xml;base64," + base64.b64encode(_svg(slug).encode("utf-8")).decode("ascii")


def page_config() -> dict:
    return {"page_title": "Signal Hub | Open, local-first marketing evidence", "page_icon": str(HUB_ICON),
            "layout": "wide", "initial_sidebar_state": "auto"}


def css() -> str:
    """Hub chrome and front-page blocks. Added after signal_theme's own CSS."""
    c = sig.CORE
    b = sig.FAMILIES["brand"]
    pills = "".join(
        f".st-key-hub-filter button[data-variant='pills']:nth-of-type({i + 2})::before {{ background:{fam(f)['600']}; }}"
        f".st-key-hub-filter button[data-variant='pills']:nth-of-type({i + 2})[aria-checked='true'] {{ background:{fam(f)['700']}"
        f" !important; }}"
        f".st-key-hub-filter button[data-variant='pills']:nth-of-type({i + 2})[aria-checked='true']::before {{"
        f" background:{fam(f)['300']}; }}"
        f".hub-tool.fam-{f.lower()}:hover {{ background:{fam(f)['200']}; }}"
        for i, f in enumerate(FAMILY_KEYS)
    )
    return f"""
<style>
.hub-eyebrow {{ font-size:.74rem; font-weight:700; letter-spacing:.16em; color:{c['muted']}; text-transform:uppercase; }}
.hub-row {{ display:flex; flex-wrap:wrap; gap:.5rem; align-items:center; }}
.hub-btn {{ padding:.6rem 1.2rem; border-radius:999px; font-weight:700; font-size:.92rem; white-space:nowrap;
  text-decoration:none !important; border:1px solid {c['line']}; color:{c['text']} !important; }}
.hub-btn:hover {{ background:rgba(32,30,29,.07); }}
.hub-btn.primary {{ background:{b['600']}; border-color:transparent; color:{c['paper']} !important; }}
.hub-btn.primary:hover {{ background:{b['700']}; }}
.hub-dot {{ display:inline-block; width:10px; height:10px; border-radius:50%; flex:none; }}
.hub-head {{ display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap:1.2rem 2.4rem;
  padding:.4rem 0 1rem; }}
.hub-head > div:first-child {{ max-width:44rem; }}
.hub-head h1 {{ font-size:clamp(2rem,3.6vw,3.1rem) !important; line-height:1 !important; letter-spacing:-.045em !important;
  margin:.6rem 0 .8rem !important; padding:0 !important; font-weight:800 !important; text-wrap:balance; }}
.hub-head h1 .hl {{ color:{b['700']}; }}
.hub-head p {{ font-size:1.02rem; line-height:1.55; color:#474238; margin:0; text-wrap:pretty; }}
.st-key-hub-filter {{ position:sticky; top:3.75rem; z-index:5; background:{c['bg']}; padding:.6rem 0 .9rem; gap:.6rem 1rem; }}
.st-key-hub-filter [data-testid="stTextInputRootElement"] {{ height:44px; border-radius:999px; background:{c['paper']} !important;
  border:1px solid rgba(32,30,29,.1) !important; }}
.st-key-hub-filter [data-testid="stTextInputRootElement"] * {{ background:transparent !important; }}
.st-key-hub-filter input {{ font-size:.95rem; }}
.st-key-hub-filter button[data-variant="pills"] {{ height:36px; padding:0 14px; border-radius:999px !important;
  border:0 !important; background:{c['paper']}; gap:7px; }}
.st-key-hub-filter button[data-variant="pills"] p {{ font-size:.88rem; font-weight:600; white-space:pre; }}
.st-key-hub-filter button[data-variant="pills"]::before {{ content:""; width:8px; height:8px; border-radius:50%;
  background:{c['muted']}; flex:none; }}
.st-key-hub-filter button[data-variant="pills"][aria-checked="true"] {{ background:{c['sidebar']} !important; }}
.st-key-hub-filter button[data-variant="pills"][aria-checked="true"] p {{ color:{c['paper']} !important; }}
.st-key-hub-filter button[data-variant="pills"][aria-checked="true"]::before {{ background:{c['paper']}; }}
.hub-groups {{ display:flex; flex-direction:column; gap:1.8rem; padding-top:.2rem; }}
.hub-group-head {{ display:flex; align-items:center; gap:10px; margin:0 0 .7rem; }}
.hub-group-head h2 {{ margin:0 !important; padding:0 !important; font-size:1.15rem !important; font-weight:800 !important;
  letter-spacing:-.02em !important; }}
.hub-group-head .n {{ font-size:.82rem; color:{c['muted']}; }}
.hub-tools {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr)); gap:12px; }}
.hub-tool {{ display:flex; flex-direction:column; gap:10px; padding:16px 16px 14px; border-radius:24px; background:{c['paper']};
  text-decoration:none !important; color:{c['text']} !important; transition:background .15s; }}
.hub-tool .top {{ display:flex; align-items:center; gap:12px; }}
.hub-tool .top svg {{ flex:none; }}
.hub-tool .nm {{ flex:1; min-width:0; font-size:1.12rem; font-weight:800; letter-spacing:-.025em; }}
.hub-tool .go {{ font-size:1.2rem; font-weight:700; }}
.hub-tool p {{ margin:0; font-size:.92rem; line-height:1.45; color:#474238; text-wrap:pretty; min-height:2.9em; }}
.hub-tool .tags {{ display:flex; flex-wrap:wrap; gap:4px; margin-top:auto; }}
.hub-mtag {{ white-space:nowrap; padding:.2rem .6rem; border-radius:999px; font-size:.72rem; background:{c['bg']};
  color:{c['muted']}; }}
.hub-empty {{ padding:2.4rem; border-radius:24px; background:{c['paper']}; color:{c['muted']}; }}
.hub-band {{ margin-top:3rem; padding:clamp(1.2rem,2.6vw,2rem); border-radius:28px; background:{c['sidebar']};
  color:{c['paper']}; }}
.hub-steps {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,170px),1fr)); gap:18px 24px; margin-top:1rem; }}
.hub-step {{ display:grid; grid-template-columns:32px minmax(0,1fr); gap:12px; align-items:start; }}
.hub-step .n {{ width:32px; height:32px; border-radius:50%; display:grid; place-items:center; font-size:.95rem;
  font-weight:800; color:{c['text']}; }}
.hub-step b {{ display:block; font-size:.98rem; margin-top:5px; color:{c['paper']}; }}
.hub-step .d {{ display:block; font-size:.86rem; line-height:1.45; color:{c['sidebar_muted']}; margin-top:4px; }}
.hub-two {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr)); gap:1.6rem 2.4rem;
  margin:2.4rem 0 0; }}
.hub-two h3 {{ font-size:1.3rem !important; font-weight:800 !important; letter-spacing:-.03em !important;
  margin:.5rem 0 !important; padding:0 !important; }}
.hub-two p {{ font-size:.92rem; line-height:1.6; color:#474238; margin:0 0 .8rem; }}
.hub-link {{ font-weight:700; font-size:.92rem; text-decoration:none !important; }}
.hub-soon {{ margin-left:.4rem; padding:.12rem .55rem; border-radius:999px; font-size:.7rem; font-weight:700;
  background:{c['warn_bg']}; color:{c['warn_text']}; white-space:nowrap; letter-spacing:0; vertical-align:middle; }}
.hub-foot {{ display:flex; flex-wrap:wrap; justify-content:space-between; gap:1rem; padding:1.4rem 0 0; margin-top:2.4rem;
  border-top:1px solid {c['line']}; font-size:.85rem; color:{c['muted']}; }}
.hub-foot a {{ color:{c['muted']} !important; }}
.hub-apphead {{ display:flex; flex-wrap:wrap; align-items:center; gap:.5rem 1rem; margin:-2.4rem 0 1rem; font-size:.82rem;
  color:{c['muted']}; }}
.hub-apphead b, .hub-apphead a.back {{ color:{c['text']} !important; }}
.hub-apphead a {{ font-weight:700; text-decoration:none !important; }}
.hub-card {{ padding:2rem; border-radius:32px; background:{c['paper']}; max-width:820px; }}
.hub-card h2 {{ margin:.6rem 0 .6rem !important; padding:0 !important; }}
{pills}
</style>"""


def apply() -> None:
    import streamlit as st

    sig.apply(HUB_KEY)
    st.markdown(css(), unsafe_allow_html=True)

