"""Give an app clone the standard Signal repo files, filled in from its apps.yaml entry.

Writes only files that do not exist yet, so it is safe to re-run on a finished repo:

    README.md (from signal-theme/README.template.md), CHANGELOG.md, CITATION.cff, CONTRIBUTING.md, PRIVACY.md,
    SECURITY.md, CODE_OF_CONDUCT.md, Dockerfile, .dockerignore, .gitignore, run_app.bat, run_app.command,
    .github/ (tests workflow, Dependabot, issue and pull-request templates), tests/test_hub_contract.py

Usage (from the signal-hub folder; the app clone sits next to it):

    python scripts/scaffold_app.py shift              # create the missing files
    python scripts/scaffold_app.py shift --dry-run    # list what would be created
    python scripts/scaffold_app.py shift --port 8598  # launcher/Docker port (default: next free 85xx port)

Full checklist for a new app: docs/ADDING_AN_APP.md.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys

HUB = Path(__file__).resolve().parents[1]
CLONES = HUB.parent
TEMPLATE = HUB / "signal-theme" / "app-template"
README_TEMPLATE = HUB / "signal-theme" / "README.template.md"
sys.path.insert(0, str(HUB))

from hub.registry import App, load  # noqa: E402

FAMILY_HEX = {"Brand": "b2622d", "Market": "728157", "Customer": "aa5d83", "Research": "a06f1f", "Decide": "4f80a2"}
HUB_PORT = 8610
BOUNDARIES = ("uncertainty visible beside every estimate, named methods with their limits, no causal claims the design "
              "cannot support, and fictional demo data only.")


def used_ports() -> set[int]:
    ports = {HUB_PORT}
    for dockerfile in CLONES.glob("*/Dockerfile"):
        ports.update(int(p) for p in re.findall(r"^EXPOSE (\d+)", dockerfile.read_text(encoding="utf-8"), re.M))
    return ports


def next_port(repo: Path) -> int:
    own = repo / "Dockerfile"
    if own.exists() and (found := re.search(r"^EXPOSE (\d+)", own.read_text(encoding="utf-8"), re.M)):
        return int(found.group(1))
    taken = used_ports()
    return next(p for p in range(8585, 8700) if p not in taken)


def _version(repo: Path, app: App) -> str:
    init = repo / "src" / app.package / "__init__.py"
    found = re.search(r'__version__\s*=\s*"([^"]+)"', init.read_text(encoding="utf-8")) if init.exists() else None
    return found.group(1) if found else "1.0.0"


def fields(app: App, repo: Path, port: int) -> dict[str, str]:
    slug = f"{app.key}signal"
    return {
        "Name": app.product, "slug": slug, "ENV": slug.upper(), "repo": app.repo, "package": app.package,
        "key": app.key, "port": str(port), "max_upload_mb": str(app.max_upload_mb or 50), "FAMILY": app.family,
        "family": app.family.lower(), "fam_hex": FAMILY_HEX[app.family], "question": app.question,
        "tagline": app.slogan, "one_liner": app.one_liner, "version": _version(repo, app),
        "date": date.today().isoformat(), "boundaries": BOUNDARIES,
    }


def fill(text: str, values: dict[str, str]) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values.get(m.group(1), m.group(0)), text)


def planned(app: App, repo: Path, port: int) -> dict[Path, str]:
    values = fields(app, repo, port)
    files = {repo / path.relative_to(TEMPLATE): fill(path.read_text(encoding="utf-8"), values)
             for path in sorted(TEMPLATE.rglob("*")) if path.is_file()}
    files[repo / "README.md"] = fill(README_TEMPLATE.read_text(encoding="utf-8"), values)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Add the standard Signal repo files to an app clone.")
    parser.add_argument("slug", help="the app's apps.yaml slug")
    parser.add_argument("--port", type=int, help="local port for the launchers and Docker")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    apps = {a.slug: a for a in load()}
    if args.slug not in apps:
        print(f"{args.slug!r} is not in apps.yaml. Add its entry first (docs/ADDING_AN_APP.md, step 2).")
        return 1
    app = apps[args.slug]
    repo = CLONES / app.repo
    if not repo.exists():
        print(f"No clone at {repo}. Clone {app.repo} next to signal-hub first.")
        return 1
    port = args.port or next_port(repo)
    for path, text in planned(app, repo, port).items():
        rel = path.relative_to(CLONES)
        if path.exists():
            print(f"kept    {rel}")
            continue
        print(f"{'would create' if args.dry_run else 'created'} {rel}")
        if not args.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    if not args.dry_run:
        print(f"\nPort {port}. Next: fill the remaining {{{{…}}}} in README.md, then follow docs/ADDING_AN_APP.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
