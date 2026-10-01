"""Copy the shared Signal look from signal-theme/ into every app clone listed in apps.yaml.

signal-theme/ in this repo is the master copy. Each app keeps a synced copy so it still runs on its own:

    <repo>/src/<package>/ui/signal_theme.py          the theme module (CSS, lockups, chart palette)
    <repo>/src/<package>/ui/assets/marks/<slug>-*     the app's own mark (SVG + 32/64 px PNG)
    <repo>/assets/<slug>-{banner,social}.png          README banner and GitHub social preview
    <repo>/assets/<slug>-mark{.svg,-32,-64,-512.png}   marks for README and favicons
    <repo>/.streamlit/config.toml                      native widget colours for the app's family

Usage (from the signal-hub folder; app clones sit next to it):

    python scripts/sync_theme.py              # all apps
    python scripts/sync_theme.py track worth  # selected slugs
    python scripts/sync_theme.py --check      # exit 1 if any app copy is out of date
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

HUB = Path(__file__).resolve().parents[1]
THEME = HUB / "signal-theme"
ASSETS = THEME / "assets"
CLONES = HUB.parent
HEADER = "# Synced from signal-hub/signal-theme/signal_theme.py. Edit it there, then run scripts/sync_theme.py.\n"

sys.path.insert(0, str(THEME))
from signal_theme import FAMILIES, app  # noqa: E402


def planned_files(entry: dict) -> dict[Path, bytes]:
    """Map destination path -> wanted bytes for one app."""
    a = app(entry["key"])
    slug = a["slug"]
    repo = CLONES / entry["repo"]
    ui = repo / "src" / entry["package"] / "ui"
    files: dict[Path, bytes] = {}
    files[ui / "signal_theme.py"] = (HEADER + (THEME / "signal_theme.py").read_text(encoding="utf-8")).encode("utf-8")
    for suffix in ("mark.svg", "mark-32.png", "mark-64.png"):
        files[ui / "assets" / "marks" / f"{slug}-{suffix}"] = (ASSETS / "marks" / f"{slug}-{suffix}").read_bytes()
    for kind, folder in (("banner", "banners"), ("social", "social")):
        files[repo / "assets" / f"{slug}-{kind}.png"] = (ASSETS / folder / f"{slug}-{kind}.png").read_bytes()
    for suffix in ("mark.svg", "mark-32.png", "mark-64.png", "mark-512.png"):
        files[repo / "assets" / f"{slug}-{suffix}"] = (ASSETS / "marks" / f"{slug}-{suffix}").read_bytes()
    config = (THEME / "config.toml").read_text(encoding="utf-8")
    config = config.replace('primaryColor = "#aa5d83"', f'primaryColor = "{FAMILIES[a["family"]]["600"]}"')
    if entry.get("max_upload_mb"):  # keep each app's own upload cap
        config = config.replace("headless = true\n", f"headless = true\nmaxUploadSize = {entry['max_upload_mb']}\n")
    files[repo / ".streamlit" / "config.toml"] = config.encode("utf-8")
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync signal-theme into the app clones.")
    parser.add_argument("slugs", nargs="*", help="apps.yaml slugs (default: all)")
    parser.add_argument("--check", action="store_true", help="report stale copies instead of writing")
    args = parser.parse_args()

    entries = yaml.safe_load((HUB / "apps.yaml").read_text(encoding="utf-8"))
    if args.slugs:
        entries = [e for e in entries if e["slug"] in set(args.slugs)]
    stale = 0
    for entry in entries:
        repo = CLONES / entry["repo"]
        if not repo.exists():
            print(f"skip {entry['slug']}: no clone at {repo}")
            continue
        for path, data in planned_files(entry).items():
            if path.exists() and path.read_bytes() == data:
                continue
            stale += 1
            if args.check:
                print(f"stale  {path.relative_to(CLONES)}")
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            print(f"wrote  {path.relative_to(CLONES)}")
    if args.check and stale:
        print(f"{stale} file(s) out of date; run scripts/sync_theme.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
