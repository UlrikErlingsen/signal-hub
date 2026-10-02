"""Render an app's mark PNGs (32/64/512), README banner (2400x720) and social preview (1280x640) with a headless
Chromium browser.

The original PNGs came from Claude Design. Use this script when an app is added or renamed, so the new images
match the rest of the kit. Draw the mark first (assets/marks/<slug>-mark.svg, the suite style: family 600 circle,
#f9f4ed glyph, family 300 accent dot) and run scripts/sync_suite.py so signal_theme.APPS knows the app:

    python signal-theme/tools/render_brand_images.py shift
    python signal-theme/tools/render_brand_images.py influence --chips "Campaigns" "Creator results" "Ad labelling"

The banner chips default to the app's `methods:` in apps.yaml.

Needs Microsoft Edge or Google Chrome installed (set SIGNAL_BROWSER to override the path) (the font is embedded).
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from signal_theme import CORE, app  # noqa: E402

ASSETS = HERE.parent / "assets"
from signal_font import FIGTREE_WOFF2_B64  # noqa: E402

FONT_CSS = ("@font-face{font-family:Figtree;font-weight:400 800;"
            f"src:url(data:font/woff2;base64,{FIGTREE_WOFF2_B64}) format('woff2')" "}")
DOTS = ("brand", "market", "customer", "research", "decide")


def _browser() -> str:
    candidates = [
        os.getenv("SIGNAL_BROWSER", ""),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        shutil.which("chromium") or "",
        shutil.which("google-chrome") or "",
    ]
    for path in candidates:
        if path and Path(path).exists():
            return path
    raise SystemExit("No Chromium browser found. Set SIGNAL_BROWSER to Edge or Chrome.")


def _mark(a: dict) -> str:
    return (ASSETS / "marks" / f"{a['slug']}-mark.svg").as_uri()


def banner_html(a: dict, chips: list[str]) -> str:
    f = a["fam"]
    pills = "".join(f"<span>{c.upper()}</span>" for c in chips)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
html,body{{margin:0;width:2400px;height:720px;background:transparent;overflow:hidden}}
.b{{position:relative;width:2400px;height:720px;border-radius:48px;overflow:hidden;background:{CORE['sidebar']};
font-family:Figtree,sans-serif}}
.c1{{position:absolute;left:1840px;top:-420px;width:780px;height:800px;border-radius:50%;background:{f['800']}}}
.c2{{position:absolute;left:1722px;top:580px;width:356px;height:356px;border-radius:50%;background:{f['700']}}}
.m{{position:absolute;left:140px;top:200px;width:280px;height:280px}}
.t{{position:absolute;left:496px;top:172px}}
.e{{color:{f['300']};font-size:29px;font-weight:700;letter-spacing:.2em}}
h1{{margin:14px 0 0 -6px;color:{CORE['paper']};font-size:131px;font-weight:800;letter-spacing:-.045em;line-height:1.05}}
h1 em{{font-style:normal;color:{f['300']}}}
p{{margin:16px 0 0;color:#ece4d6;font-size:41px;line-height:1.3}}
.p{{display:flex;gap:16px;margin-top:46px}}
.p span{{padding:14px 32px;border-radius:999px;background:rgba(249,244,237,.1);color:{CORE['paper']};font-size:27px;
font-weight:700;letter-spacing:.06em}}
</style></head><body><div class="b"><div class="c1"></div><div class="c2"></div><img class="m" src="{_mark(a)}">
<div class="t"><div class="e">SIGNAL · {f['label'].upper()}</div><h1>{a['prefix']} <em>Signal</em></h1>
<p>{a['tagline']}</p><div class="p">{pills}</div></div></div></body></html>"""


def social_html(a: dict) -> str:
    f = a["fam"]
    from signal_theme import FAMILIES

    dots = "".join(f'<i style="background:{FAMILIES[k]["600"]}"></i>' for k in DOTS)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}
html,body{{margin:0;width:1280px;height:640px;overflow:hidden}}
.s{{position:relative;width:1280px;height:640px;overflow:hidden;background:{CORE['bg']};font-family:Figtree,sans-serif}}
.c1{{position:absolute;left:790px;top:40px;width:180px;height:180px;border-radius:50%;background:{f['300']}}}
.c2{{position:absolute;left:850px;top:290px;width:700px;height:700px;border-radius:50%;background:{f['600']}}}
.m{{position:absolute;left:72px;top:72px;width:120px;height:120px}}
h1{{position:absolute;left:68px;top:232px;margin:0;color:{CORE['text']};font-size:100px;font-weight:800;
letter-spacing:-.045em;line-height:1.05;white-space:nowrap}}
h1 em{{font-style:normal;color:{f['700']}}}
p{{position:absolute;left:72px;top:360px;margin:0;width:700px;color:#474238;font-size:36px;line-height:1.4}}
.f{{position:absolute;left:78px;top:548px;display:flex;align-items:center;gap:10px}}
.f i{{width:20px;height:20px;border-radius:50%}}
.f b{{margin-left:20px;color:{CORE['muted']};font-size:21px;font-weight:700;letter-spacing:.2em}}
</style></head><body><div class="s"><div class="c1"></div><div class="c2"></div><img class="m" src="{_mark(a)}">
<h1>{a['prefix']} <em>Signal</em></h1><p>{a['tagline']}</p><div class="f">{dots}<b>PART OF THE SIGNAL SUITE</b></div>
</div></body></html>"""


def mark_html(a: dict, size: int) -> str:
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;width:{size}px;'
            f'height:{size}px;background:transparent;overflow:hidden}}img{{display:block;width:{size}px;'
            f'height:{size}px}}</style></head><body><img src="{_mark(a)}"></body></html>')


def _methods(key: str) -> list[str]:
    import yaml

    entries = yaml.safe_load((HERE.parents[1] / "apps.yaml").read_text(encoding="utf-8"))
    return next((list(e.get("methods") or []) for e in entries if e["key"] == key), [])


def _shoot(html: str, out: Path, width: int, height: int, transparent: bool) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(html, encoding="utf-8")
        args = [_browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                f"--window-size={width},{height}", "--virtual-time-budget=4000", f"--screenshot={out}"]
        if transparent:
            args.append("--default-background-color=00000000")
        subprocess.run([*args, page.as_uri()], check=True, capture_output=True, timeout=120)
    print(f"wrote {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", help="signal_theme.APPS key, e.g. influence")
    parser.add_argument("--chips", nargs="+", default=None, help="2-3 method chips (default: apps.yaml methods)")
    args = parser.parse_args()
    a = app(args.key)
    if args.chips is None:
        args.chips = _methods(args.key)[:3]
    for size in (32, 64, 512):
        _shoot(mark_html(a, size), ASSETS / "marks" / f"{a['slug']}-mark-{size}.png", size, size, True)
    _shoot(banner_html(a, args.chips), ASSETS / "banners" / f"{a['slug']}-banner.png", 2400, 720, True)
    _shoot(social_html(a), ASSETS / "social" / f"{a['slug']}-social.png", 1280, 640, False)


if __name__ == "__main__":
    main()
