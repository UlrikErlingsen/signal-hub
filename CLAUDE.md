# CLAUDE.md — Signal Hub

Build brief for coding agents. Read all of it before writing code. Amendments since the original brief are marked
**(2026-10-01)**.

## 1. What Signal Hub is

Ulrik Erlingsen builds **Signal**, a suite of open-source, local-first marketing tools. Each tool is its own GitHub
repo under `UlrikErlingsen`: a Python package with a Streamlit app, in one house style (`brand-tracking`, Track
Signal, is the reference repo).

Signal Hub is one Streamlit app that puts all the tools behind a single link: one front page, a sidebar menu grouped
by family, and every released tool running inside it.

- Audience: recruiters and hiring managers for marketing roles (one link, a coherent product, any tool tried in
  under a minute). Second audience: developers reading the code on GitHub.
- Not: a rewrite of the apps, a monorepo, a data platform, or a product with user accounts. It assembles apps that
  already exist. **Business logic never moves into the Hub.**

## 2. The apps

Source of truth: each repo's `pyproject.toml` and README; local clones sit next to this folder. The Hub's list is
[`apps.yaml`](apps.yaml) (never list apps anywhere else). **(2026-10-03)** `scripts/sync_suite.py` writes every
derived list from it (theme APPS block, pins, README tables here and in every app, topics, repo metadata, the suite
size in prose); `scripts/scaffold_app.py` gives a new app repo the standard files. Recipe:
[docs/ADDING_AN_APP.md](docs/ADDING_AN_APP.md).

**(2026-10-01)** The sidebar uses the five design families from Claude Design "Unified Signal apps design":
Brand (Track, Position) · Market (Prospect, Listen, Influence, Season, Adopt, Rival, Reach) · Customer (Worth, Segment,
Trace, Blueprint, Recommend) · Research (Choice, Driver, Measure, Text, Tag, Learn) · Decide (Experiment, Gate, Shift,
Alloc).

- All 24 apps are embedded. **(2026-10-03)** Rival (`competitor-analysis`), Reach (`location-catchment-analysis`),
  Learn (`research-prioritization`) and Blueprint (`service-blueprinting`) joined at v1.0.0. Shift Signal (`cannibalization-analysis`, menu and product
  cannibalization) joined at v1.0.0. The four Norwegian-market apps (`b2b-prospecting` Prospect Signal,
  `media-listening` Listen Signal, `influencer-campaigns` **Influence Signal** (renamed from CreatorSignal on
  2026-10-01), `marketing-calendar` Season Signal) went public and joined at v1.0.0 on 2026-10-02. In the Hub they
  run in Hub mode (APP_CONTRACT section 8): no registry/RSS calls, no disk writes, demo data in session memory.
- Freddo CRM (`signal-crm`, Frappe-based, demo https://freddo.ulrikerlingsen.com) is a separate product, not in the
  Hub. The front page links to it.

## 3. Architecture

### 3.1 Repo and stack

Python 3.10+, Streamlit multipage via `st.navigation` + `st.Page`, AGPL-3.0-or-later, author "Ulrik Erlingsen". Same
files as the app repos (README with banner and badges, CHANGELOG, SECURITY, PRIVACY, CONTRIBUTING, Dockerfile,
run_app.bat/.command, pyproject, ruff, pytest).

Apps install as packages pinned to release tags. **(2026-10-01)** Pins use GitHub tag archives so no git client is
needed: `tracksignal[ui] @ https://github.com/UlrikErlingsen/brand-tracking/archive/refs/tags/v1.1.0.zip`.
`scripts/gen_requirements.py` writes `requirements-apps.txt` (pins) and `local-apps.txt` (editable sibling
clones) from `apps.yaml`.

### 3.2 The app ↔ Hub contract

See [docs/APP_CONTRACT.md](docs/APP_CONTRACT.md): `src/<pkg>/ui/__init__.py` exposes `render()` (never calls
`st.set_page_config` or `st.navigation`) and `APP_INFO`; thin standalone `app.py`; slug-namespaced session-state and
widget keys (`"worth:horizon"`); `streamlit` in a `[ui]` extra. Rule in every app: **no Streamlit import anywhere
under `src/<pkg>/` except `src/<pkg>/ui/`**; the guard test ignores `ui/`. Apps not on the contract run as `link`
or `coming_soon`.

### 3.3 What the Hub contains

- `hub/app.py`: `st.set_page_config`, theme, `st.navigation` from `apps.yaml` (hidden; see `hub/sidebar.py`).
- `hub/home.py`: the front page (section 4). **(2026-10-02)** Design "Signal Hub Home v2" replaces "Signal Hub Page".
- `hub/sidebar.py`: the menu: lockup, tool search, one collapsible group per family with app marks (`st.page_link`).
- `hub/registry.py`: loads and validates `apps.yaml`, fails loudly on a bad entry.
- `hub/pages.py`: one wrapper per app: slim header (product, version, source, standalone demo), then
  `<pkg>.ui.render()` inside try/except. A crashing app shows an error card and never takes the Hub down.
- `hub/theme.py` + `signal-theme/`: **(2026-10-01)** the Organic Signal design kit replaces the old brand-tracking
  colours (cream `#f5ead8`, warm dark sidebar `#2e2b25`, Figtree, one accent per family; the Hub chrome uses the
  Brand accent `#b2622d`). `signal-theme/` is the master copy; `scripts/sync_theme.py` copies it into each app.
- No business logic, no data processing, no shared database.

### 3.4 Dependencies

All apps share one environment. The CI `apps` job installs every pinned app plus the Hub and fails on resolver
conflicts. When two apps conflict, fix the range in the app repo (new patch release); never vendor or patch inside
the Hub. Heavy optional dependencies (torch for Listen Signal) stay optional; the Hub uses the light fallback.

### 3.5 Demo data

Every app preloads a deterministic fictional demo. Where cheap, align new demos on the fictional brand "Fjellbrus"
(Norwegian sports drink). Every page states the data is fictional.

## 4. Front page

1. Promise of the suite plus a short paragraph: open-source, local-first tools that show uncertainty.
2. **(2026-10-02)** Every tool as a card from `apps.yaml`, grouped by family, with a search box and family filter;
   then the four steps every app shares.
3. "Customers in practice": Prospect Signal finds the market → CSV export → Freddo CRM manages the customers.
4. "How it's built": each tool its own repo and package, released versions pinned, no telemetry, no accounts;
   built with AI-assisted development (Ulrik specifies, reviews and ships); no real-user or traction claims.
5. Footer: GitHub profile, ulrikerlingsen.com, licence.

## 5. Privacy and safety

No telemetry, analytics scripts or accounts. Uploads stay in session memory, never on the server's disk.
**(2026-10-03)** Upload caps: `max_upload_mb` in apps.yaml (1000 MB for data-heavy tools, 50 MB for small structured
inputs) when run locally; every launcher takes `<APP>_MAX_UPLOAD_MB`, Docker images `STREAMLIT_SERVER_MAX_UPLOAD_SIZE`.
The Hub runs locally at 1000 MB and its Docker image defaults to 50 MB for the public demo. No external AI calls from the Hub. Each app's own rules still apply (Prospect Signal never stores
people; Influence Signal compliance is "checklist support, not legal advice").

## 6. Versioning and updates

An app releases by bumping its version, updating its CHANGELOG and tagging `vX.Y.Z`. The Hub updates an app by
changing one `tag:` line in `apps.yaml`, regenerating requirements, testing and redeploying. Later (phase 4): an
Action in each app repo sends `repository_dispatch` on a new tag and a Hub workflow opens a "bump <app> to vX.Y.Z"
PR. Freddo pins the same app tags as the Hub (e.g. Worth Signal); keep both in step.

## 7. WorthSignal consolidation (Hub phase, not started)

`customer-value-analytics` (`cva`) becomes Worth Signal's single home. Move the general calculators and retention
models from `signal-crm/packages/signal-core/src/signal_core/worth/` into `src/cva/` (not `ui/`, no Streamlit), with
their pinned lecture/exam tests. signal-core keeps the Freddo-specific layer and pins the new cva tag. Coordinate with
the Freddo agent; **never edit `signal-crm` without listing every file you would touch first.**

## 8. Deployment

`python:3.12-slim`, pins from `requirements-apps.txt`, non-root user, port 8501, `/_stcore/health` health check.
Target: a subdomain such as `signal.ulrikerlingsen.com`. Hosting, DNS, reverse proxy, TLS and firewall are handled
outside this repo. Images build on GitHub Actions to GHCR (`.github/workflows/image.yml`). Hand-off:
[deploy/README.md](deploy/README.md).

## 9. Tests

`tests/test_registry.py` (registry validation, theme consistency, generated files), `tests/test_home.py` (front page
via AppTest), `tests/test_apps.py` (marker `apps`: every embedded app honours the contract and renders its demo in
the wrapper). ruff (line length 120) + pytest.

## 10. Phases

- P0 contract + P1 skeleton + P2 rollout: done on 2026-10-02 for all 15 analytics apps (see STATUS).
- P3: the four Norwegian apps joined at v1.0.0 on 2026-10-02 (public, embedded, Hub mode).
- P4: Docker/GHCR (workflow ready), hosting hand-off, tag-bump PR automation.
- Parallel: the WorthSignal consolidation (section 7).

## 11. Working rules

- Ulrik commits and pushes from GitHub Desktop. Commit locally in small, logical steps and say what to push.
- Changes in an app repo happen in that repo, as a release. Never copy app code into the Hub.
- Ask before touching `signal-crm` (Freddo). Hosting and infrastructure are handled outside this repo.
- Keep [docs/STATUS.md](docs/STATUS.md) current.
- When unsure about a fact (an API, a product name, a version), check the repo. Never guess.
