"""One command that brings every list of Signal apps in line with apps.yaml.

apps.yaml is the only place an app is listed. This writes everything derived from it:

In this repo
    signal-theme/signal_theme.py      the APPS block (prefix, family, repo, tagline)
    requirements-apps.txt             release-tag pins (and local-apps.txt for sibling clones)
    README.md                         the per-family app tables and the suite size ("Twenty small apps")
    docs/github/profile-README.md     the suite size on the GitHub profile
    docs/github/set_repo_metadata.ps1 repo descriptions and topics for the GitHub CLI
    signal-theme/topics.txt           the topic list per repo

In the sibling clones (skipped when a clone is missing, e.g. on CI)
    <app>/README.md                   the "Where this fits in Signal" table (scripts/sync_readme_suite.py)
    <app>/src/<pkg>/ui/...            the theme copy, marks, banner, social preview, .streamlit (scripts/sync_theme.py)
    UlrikErlingsen/README.md          the profile README

Usage (from the signal-hub folder; app clones sit next to it):

    python scripts/sync_suite.py              # write everything
    python scripts/sync_suite.py --check      # list stale files, exit 1 if any
    python scripts/sync_suite.py --hub-only   # only this repo (what CI and tests check)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

import yaml

HUB = Path(__file__).resolve().parents[1]
CLONES = HUB.parent
sys.path.insert(0, str(HUB))

from hub.registry import FAMILIES, GITHUB, App, by_family, count_word, load  # noqa: E402
from scripts import gen_requirements, sync_readme_suite, sync_theme  # noqa: E402

THEME = HUB / "signal-theme" / "signal_theme.py"
PROFILE_REPO = CLONES / "UlrikErlingsen" / "README.md"
APPS_START = "<!-- signal-apps:start (generated from apps.yaml by scripts/sync_suite.py) -->"
APPS_END = "<!-- signal-apps:end -->"
_APPS_BLOCK = re.compile(r"<!-- signal-apps:start[^>]*-->.*?<!-- signal-apps:end -->", re.DOTALL)
_THEME_BLOCK = re.compile(r"# key: \(prefix, family, repo, tagline\)[^\n]*\nAPPS = \{\n.*?\n\}\n", re.DOTALL)
_COUNT = re.compile(r"\b[A-Z][a-z]+(?:-[a-z]+)?(?= small apps)")
_COUNT_LOWER = re.compile(r"(?<=all )[a-z]+(?:-[a-z]+)?(?= Signal tools)")
SUITE_TOPICS = ("signal-suite", "streamlit", "local-first")
HUB_METADATA = ('gh repo edit UlrikErlingsen/signal-hub --description "Signal Hub: every Signal marketing-evidence tool '
                'behind one link. Open-source, local-first." --homepage "https://ulrikerlingsen.com" --add-topic '
                "signal-suite --add-topic streamlit --add-topic local-first --add-topic marketing-analytics "
                "--add-topic portfolio")


def _same(current: bytes, wanted: bytes) -> bool:
    crlf, lf = bytes([13, 10]), bytes([10])
    return current == wanted or current.replace(crlf, lf) == wanted.replace(crlf, lf)


def _counted(text: str, n: int) -> str:
    text = _COUNT.sub(count_word(n), text)
    return _COUNT_LOWER.sub(count_word(n).lower(), text)


def theme_block(apps: list[App]) -> str:
    width = max(len(a.key) for a in apps) + 4
    rows = []
    for a in apps:
        values = [a.prefix, a.family.lower(), a.repo, a.slogan]
        key = f'"{a.key}":'.ljust(width)
        rows.append(f"    {key}({', '.join(json.dumps(v, ensure_ascii=False) for v in values)}),")
    return ("# key: (prefix, family, repo, tagline). Generated from signal-hub/apps.yaml by scripts/sync_suite.py.\n"
            "APPS = {\n" + "\n".join(rows) + "\n}\n")


def readme_block(apps: list[App]) -> str:
    from hub.theme import fam

    parts = [APPS_START]
    for family, members in by_family(apps).items():
        if not members:
            continue
        parts += ["", f'## <img src="https://img.shields.io/badge/-%20-{fam(family)["600"][1:]}?style=flat-square" '
                      f'height="14" alt=""> {family}', "", "| | App | Question | Repo |", "|---|---|---|---|"]
        for a in members:
            mark = f'<img src="signal-theme/assets/marks/{a.key}signal-mark-64.png" width="28" alt="">'
            repo = f"[{a.repo}]({GITHUB}/{a.repo})" if a.public else "private until v1"
            parts.append(f"| {mark} | **{a.product}** | {a.question} | {repo} |")
    parts += ["", APPS_END]
    return "\n".join(parts)


def hub_readme(text: str, apps: list[App]) -> str:
    block = readme_block(apps)
    if _APPS_BLOCK.search(text):
        text = _APPS_BLOCK.sub(lambda _: block, text, count=1)
    else:  # first run: replace the hand-written family sections
        start = text.index('## <img src="https://img.shields.io/badge/-%20-')
        end = text.index("## How the apps fit together")
        text = text[:start] + block + "\n\n" + text[end:]
    return _counted(text, len(apps))


def theme_module(text: str, apps: list[App]) -> str:
    if not _THEME_BLOCK.search(text):
        raise ValueError("signal_theme.py has no APPS block")
    return _THEME_BLOCK.sub(lambda _: theme_block(apps), text, count=1)


def topics_txt(apps: list[App]) -> str:
    lines = ["# gh repo edit UlrikErlingsen/<repo> --add-topic <t> …  (generated from apps.yaml by scripts/sync_suite.py)",
             "signal-hub: signal-suite, streamlit, local-first"]
    lines += [f"{a.repo}: signal-suite, signal-{a.family.lower()}, streamlit, local-first"
              + "".join(f", {t}" for t in a.topics) for a in apps if a.public]
    return "\n".join(lines) + "\n"


def metadata_ps1(apps: list[App]) -> str:
    lines = ["# Repo descriptions, topics and social previews. Needs the GitHub CLI: https://cli.github.com (gh auth login).",
             "# Run from PowerShell. Safe to re-run. Social previews must be uploaded by hand (see REPO_SETTINGS.md).",
             "# Generated from apps.yaml by scripts/sync_suite.py.", "", HUB_METADATA]
    for a in apps:
        if not a.public:
            continue
        question = a.question[0].lower() + a.question[1:]
        topics = [*SUITE_TOPICS[:1], f"signal-{a.family.lower()}", *SUITE_TOPICS[1:], *a.topics]
        lines.append(f'gh repo edit UlrikErlingsen/{a.repo} --description "{a.product}: {question} Open-source, '
                     f'local-first Streamlit app." --homepage "{GITHUB}/signal-hub"'
                     + "".join(f" --add-topic {t}" for t in topics))
    return "\n".join(lines) + "\n"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def plan(hub_only: bool = False) -> dict[Path, bytes]:
    """Every derived file and the bytes it should hold."""
    apps = load()
    files: dict[Path, str | bytes] = {
        THEME: theme_module(_read(THEME), apps),
        HUB / "README.md": hub_readme(_read(HUB / "README.md"), apps),
        HUB / "docs" / "github" / "profile-README.md": _counted(_read(HUB / "docs" / "github" / "profile-README.md"),
                                                                len(apps)),
        HUB / "docs" / "github" / "set_repo_metadata.ps1": metadata_ps1(apps),
        HUB / "signal-theme" / "topics.txt": topics_txt(apps),
        **gen_requirements.render(),
    }
    if not hub_only:
        if PROFILE_REPO.exists():
            files[PROFILE_REPO] = _counted(_read(PROFILE_REPO), len(apps))
        entries = {e["slug"]: e for e in yaml.safe_load(_read(HUB / "apps.yaml"))}
        for a in apps:
            repo = CLONES / a.repo
            if not repo.exists():
                continue
            readme = repo / "README.md"
            if readme.exists():
                try:
                    files[readme] = sync_readme_suite.rewrite(_read(readme), sync_readme_suite.block(apps, a))
                except ValueError as exc:
                    print(f"skip   {a.repo}/README.md: {exc}")
            # The theme copy carries the APPS block generated above, not the file on disk.
            planned = sync_theme.planned_files(entries[a.slug], theme_text=files[THEME])
            files.update(planned)
    return {path: data if isinstance(data, bytes) else data.encode("utf-8") for path, data in files.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Bring every list of Signal apps in line with apps.yaml.")
    parser.add_argument("--check", action="store_true", help="list stale files and exit 1 if any")
    parser.add_argument("--hub-only", action="store_true", help="only files in this repo")
    args = parser.parse_args()
    stale = 0
    for path, data in plan(hub_only=args.hub_only).items():
        if path.exists() and _same(path.read_bytes(), data):
            continue
        stale += 1
        where = path.relative_to(CLONES)
        if args.check:
            print(f"stale  {where}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"wrote  {where}")
    if args.check and stale:
        print(f"{stale} file(s) out of date; run python scripts/sync_suite.py")
        return 1
    if not stale:
        print(f"All lists match apps.yaml ({len(load())} apps, {len(FAMILIES)} families).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
