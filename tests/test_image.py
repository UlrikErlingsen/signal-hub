"""The Docker image holds only what the Dockerfile copies. Rebuild that file set and import the Hub from it."""

from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def _copied(tmp: Path) -> Path:
    """Recreate /app from the Dockerfile's COPY lines (sources relative to the repo)."""
    app = tmp / "app"
    app.mkdir()
    for line in (ROOT / "Dockerfile").read_text(encoding="utf-8").splitlines():
        if not line.startswith("COPY "):
            continue
        *sources, dest = line.split()[1:]
        for source in sources:
            src = ROOT / source
            target = app / dest
            if dest.endswith("/") or len(sources) > 1:
                target = target / src.name
            target.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, target, dirs_exist_ok=True)
            else:
                shutil.copy2(src, target)
    return app


def test_the_image_file_set_imports_and_renders_the_hub_chrome(tmp_path: Path) -> None:
    app = _copied(tmp_path)
    code = "; ".join([
        "import pathlib, sys",
        "sys.path.insert(0, '.')",
        "import hub.theme, hub.home, hub.pages, hub.sidebar, hub.registry",
        "assert hub.theme.ROOT.resolve() == pathlib.Path('.').resolve(), hub.theme.ROOT",
        "apps = hub.registry.load()",
        "assert hub.theme.css() and hub.sidebar.css(apps) and hub.theme.mark('signalhub')",
        "hub.theme.sig.app('track')",
    ])
    result = subprocess.run([sys.executable, "-I", "-c", code], cwd=app, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr


def test_visitors_never_see_tracebacks() -> None:
    config = (ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8")
    assert re.search(r'^showErrorDetails = "none"$', config, re.M)
    assert "--client.showErrorDetails=none" in (ROOT / "Dockerfile").read_text(encoding="utf-8")
