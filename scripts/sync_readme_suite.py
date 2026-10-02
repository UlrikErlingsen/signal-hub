"""Rewrite the suite table under "## Where this fits in Signal" in every app README from apps.yaml.

Each README keeps its own hand-off paragraph(s) at the top of the section. Everything from the suite table to the
end of the section is generated between markers, so the apps, families, questions and links stay identical across
the suite:

    <!-- signal-suite:start -->  ...  <!-- signal-suite:end -->

The first run replaces the hand-copied table (and the closing "maintained public suite" line); later runs replace
only the marked block.

Usage (from the signal-hub folder; app clones sit next to it):

    python scripts/sync_readme_suite.py               # all apps
    python scripts/sync_readme_suite.py track worth   # selected slugs
    python scripts/sync_readme_suite.py --check       # exit 1 if any README is out of date
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

HUB = Path(__file__).resolve().parents[1]
CLONES = HUB.parent
sys.path.insert(0, str(HUB))

from hub.registry import FAMILIES, GITHUB, App, load

HEADING = "## Where this fits in Signal"
START = "<!-- signal-suite:start (generated from signal-hub/apps.yaml by scripts/sync_readme_suite.py) -->"
END = "<!-- signal-suite:end -->"
_MARKED = re.compile(r"<!-- signal-suite:start[^>]*-->.*?<!-- signal-suite:end -->", re.DOTALL)
_SUITE_LINE = re.compile(r"^(The maintained public suite|All .* apps run side by side).*$", re.MULTILINE)


def block(apps: list[App], current: App) -> str:
    order = {family: i for i, family in enumerate(FAMILIES)}
    rows = []
    for app in sorted(apps, key=lambda a: order[a.family]):
        name = f"**{app.product}** (this app)" if app.slug == current.slug else f"[{app.product}]({GITHUB}/{app.repo})"
        rows.append(f"| {app.family} | {name} | {app.question} |")
    return "\n".join([
        START,
        "| Family | App | Asks |",
        "|---|---|---|",
        *rows,
        "",
        f"All {len(apps)} apps run side by side in [Signal Hub]({GITHUB}/signal-hub), each opening with fictional demo "
        "data. Every repo carries the [`signal-suite`](https://github.com/topics/signal-suite) topic, and the suite is "
        "listed at [ulrikerlingsen.com](https://ulrikerlingsen.com). Freddo CRM is a separate product.",
        END,
    ])


def rewrite(text: str, generated: str) -> str:
    """Return the README text with the generated block in its Where-this-fits section."""
    if _MARKED.search(text):
        return _MARKED.sub(lambda _: generated, text, count=1)
    start = text.find(HEADING)
    if start < 0:
        raise ValueError(f"no '{HEADING}' section")
    body_start = start + len(HEADING)
    nxt = text.find("\n## ", body_start)
    end = len(text) if nxt < 0 else nxt + 1
    section = text[body_start:end]
    table = re.search(r"^\|[^\n]*\|\s*\n\|[-| :]+\|\s*\n(?:\|[^\n]*\|\s*\n?)*", section, re.MULTILINE)
    if table is None:
        raise ValueError("no suite table in the section")
    head = section[: table.start()].rstrip()
    tail = _SUITE_LINE.sub("", section[table.end():]).strip()
    parts = [head, generated] + ([tail] if tail else [])
    return text[:body_start] + "\n\n".join(parts).rstrip() + "\n\n" + text[end:]


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync the suite table into every app README.")
    parser.add_argument("slugs", nargs="*")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    apps = load()
    targets = [a for a in apps if not args.slugs or a.slug in set(args.slugs)]
    stale = 0
    for app in targets:
        readme = CLONES / app.repo / "README.md"
        if not readme.exists():
            print(f"skip {app.slug}: no clone")
            continue
        text = readme.read_text(encoding="utf-8")
        new = rewrite(text, block(apps, app))
        if new.replace("\r\n", "\n") == text.replace("\r\n", "\n"):
            continue
        stale += 1
        if args.check:
            print(f"stale  {app.repo}/README.md")
        else:
            readme.write_text(new, encoding="utf-8")
            print(f"wrote  {app.repo}/README.md")
    if args.check and stale:
        print(f"{stale} README(s) out of date; run scripts/sync_readme_suite.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
