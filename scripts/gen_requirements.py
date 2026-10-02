"""Generate the app requirement files from apps.yaml.

    requirements-apps.txt   embedded apps pinned to their release tags (used by Docker, CI and run_app)
    local-apps.txt          the same apps as editable installs from sibling clones (development). Deliberately not
                            named requirements*.txt: Dependabot scans those and cannot see the sibling folders.

Usage: python scripts/gen_requirements.py [--check]
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

HUB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HUB))

from hub.registry import load

HEADER = "# Generated from apps.yaml by scripts/gen_requirements.py. Do not edit by hand.\n"


def render() -> dict[Path, str]:
    apps = [a for a in load() if a.mode == "embedded"]
    pinned = HEADER + "".join(f"{a.requirement}\n" for a in apps)
    local = HEADER + "# Editable installs from sibling clones, for working on apps and the Hub together.\n"
    local += "".join(f"-e ../{a.repo}[ui]\n" for a in apps)
    return {HUB / "requirements-apps.txt": pinned, HUB / "local-apps.txt": local}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate requirement files from apps.yaml.")
    parser.add_argument("--check", action="store_true", help="exit 1 if a file is out of date")
    args = parser.parse_args()
    stale = []
    for path, text in render().items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current == text:
            continue
        stale.append(path.name)
        if not args.check:
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.name}")
    if args.check and stale:
        print(f"out of date: {', '.join(stale)}; run scripts/gen_requirements.py")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
