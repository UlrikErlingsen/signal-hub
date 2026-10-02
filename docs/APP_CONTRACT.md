# App ↔ Hub contract

Signal Hub runs every embedded app inside one Streamlit process. An app joins the Hub by exposing an importable UI
entry point. The app also keeps working on its own, exactly as before.

## 1. Package layout

```
src/<package>/
    __init__.py            core: __version__, no Streamlit import
    ...                    core modules: analysis, io, examples, ...  (no Streamlit import)
    ui/
        __init__.py        APP_INFO + render()
        app.py             the former app.py body, wrapped in functions (optional split)
        signal_theme.py    synced from signal-hub/signal-theme (do not edit in the app repo)
        assets/marks/      synced: <slug>-mark.svg, -32.png, -64.png
app.py                     thin standalone entry point
```

Architecture rule: **no Streamlit import anywhere under `src/<package>/` except `src/<package>/ui/`.** The core stays
importable without a UI library (Freddo installs cores with `--no-deps`). The guard test in each repo skips `ui/`.

## 2. `src/<package>/ui/__init__.py`

```python
from <package> import __version__

APP_INFO = {"product": "Track Signal", "version": __version__, "repo": "brand-tracking", "slug": "track"}


def render() -> None:
    """Draw the whole app on the current page. Never calls st.set_page_config."""
```

- `render()` draws everything: theme (`sig.apply`), sidebar lockup and controls, masthead, the selected page and the
  footer. Everything that must run on every rerun lives inside `render()` (or functions it calls). Module-level code
  runs once per process when imported, not once per rerun.
- `render()` must not call `st.set_page_config`. Only the standalone `app.py` or the Hub may call it.
- `render()` must not call `st.navigation`/`st.Page` (the Hub owns navigation). Pick pages with a sidebar
  `st.radio`, as the analytics apps already do.
- Errors inside a page are caught and shown with the app's friendly error. The Hub also wraps `render()`, so an
  uncaught error shows an error card instead of taking the Hub down.

## 3. Standalone `app.py`

```python
"""Track Signal standalone entry point."""
import os
os.environ.setdefault("ARROW_DEFAULT_MEMORY_POOL", "system")

from pathlib import Path
import sys

import streamlit as st

SRC = Path(__file__).resolve().parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tracksignal.ui import render, signal_theme as sig  # noqa: E402

st.set_page_config(**sig.page_config("track"))
render()
```

## 4. Session state and widget keys

Every `st.session_state` key and every explicit widget `key=` is namespaced with the slug: `"track:raw_data"`,
`"track:wave_select"`. Use one helper so it cannot drift:

```python
NS = "track"
def k(name: str) -> str:
    return f"{NS}:{name}"
```

Widgets without an explicit `key` get an automatic key from their label and parameters. If two apps have an
identical widget (same label and arguments) and both render in one session, Streamlit raises
`DuplicateWidgetID` only within the same run; across pages it is safe. Still, give every stateful widget an
explicit namespaced key, and always key the page-selector radio (`key=k("page")`).

## 5. Dependencies

- `streamlit` (and plotting-only dependencies, if the core never imports them) move to an optional extra:
  `[project.optional-dependencies] ui = ["streamlit>=1.38,<2", ...]`. The `test` extra includes them.
- `requirements.txt` keeps listing everything, so `run_app.bat`/Docker work unchanged.
- The theme module and marks ship as package data:
  `[tool.setuptools.package-data] "<package>.ui" = ["assets/marks/*"]`.
- Ranges must stay compatible with the other apps (the Hub installs all of them in one environment). Today the
  shared environment resolves to streamlit 1.64, plotly 7.1, pandas 2.3, numpy 2.5.

## 6. Tests every app keeps

- Existing AppTest of `app.py` still passes.
- `from <package>.ui import render, APP_INFO` works; `APP_INFO["version"] == __version__`.
- AppTest of a tiny script that calls `render()` without `set_page_config` renders the demo with no exception.
- Guard: no `streamlit` import under `src/<package>/` outside `ui/`.

## 7. Releasing

Bump the version (minor for this rollout), add a CHANGELOG entry, update `CITATION.cff`, commit, and create an
annotated tag `vX.Y.Z`. Then change the app's `tag:` in signal-hub `apps.yaml` and set `mode: embedded`.

## 8. Hub mode (`SIGNAL_HUB=1`)

The Hub sets the environment variable `SIGNAL_HUB=1` before importing apps. When it is set, an app must:

- keep all state in the Streamlit session (in-memory SQLite/DuckDB, `st.session_state`), never write files or
  databases on the server, and never read a user's earlier workspace;
- make no outbound network requests (registry APIs, RSS, web pages); use its bundled fictional demo or uploads;
- say so in the UI where a feature is disabled ("Live collection is off in Signal Hub; run the app locally").

Standalone behaviour is unchanged. Test both modes (monkeypatch the variable).

Apps with their own multipage navigation (`st.navigation` + `pages/`) keep it for the standalone `app.py`; `render()`
draws the same page functions behind a namespaced sidebar radio instead, because the Hub owns `st.navigation`.
