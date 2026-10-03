# Changelog

All notable changes to Signal Hub are documented here.

## [Unreleased]

### Added

- Rival Signal (`competitor-analysis`, Market), Reach Signal (`location-catchment-analysis`, Market), Learn Signal
  (`research-prioritization`, Research) and Blueprint Signal (`service-blueprinting`, Customer) at v1.0.0:
  twenty-four apps.
- Data limits, local vs public (APP_CONTRACT section 9):
  - Run on your own computer, the tools have no built-in data limits; memory is the limit.
  - Uploads default to 10 GB (`max_upload_mb: 10000`, `SIGNALHUB_MAX_UPLOAD_MB`).
  - The Hub's Docker image is the public demo: 50 MB uploads and `SIGNAL_PUBLIC=1`, which turns on every tool's demo
    caps.
  - The app template's launchers and Dockerfile follow the same pattern.
- Shift Signal (`cannibalization-analysis`, Decide family) at v1.0.0: twenty apps.
- `scripts/sync_suite.py`: one command that writes every list derived from `apps.yaml`:
  - the `signal_theme.APPS` block and the requirement pins;
  - the README app tables and the suite size in prose;
  - topics and repo metadata;
  - every app README's suite table and theme copy.

  `--check` for CI.
- `scripts/scaffold_app.py` and `signal-theme/app-template/`: the standard repo files for a new app, filled in
  from its registry entry.
- `docs/ADDING_AN_APP.md`.
- `apps.yaml` gains `tagline` and `topics`.
- `render_brand_images.py` also renders the mark PNGs and takes banner chips from `methods`.

### Fixed

- The Docker image lacked `signal-theme/signal_font.py`, so the Hub failed to start (`ModuleNotFoundError`). `tests/test_image.py` now rebuilds the image's file set from the Dockerfile and imports the Hub from it.
- Visitors no longer see Streamlit tracebacks (`showErrorDetails = "none"`); the Hub's own error cards stay.
- `render_brand_images.py` failed to start (an f-string syntax error).

### Removed

- `signal-theme/hub/README.md` and `signal-theme/profile/README.md`, stale copies from the design-kit import. The live
  versions are `README.md` and `docs/github/profile-README.md`.

### Changed

- Front page and sidebar follow Claude Design "Signal Hub Home v2": every tool as a card grouped by family, with a
  search box and family filter; the four shared steps as one band; "Customers in practice" and "How it's built"
  side by side. The featured trio, question picker and separate suite list are gone (the cards cover them).
- The sidebar is the Hub's own (`hub/sidebar.py`; `st.navigation` runs hidden): Signal Hub lockup, tool search, one
  collapsible group per family with each app's mark, and GitHub and Freddo CRM links after the open app's controls.
- App pages open with a "← All tools" link in the header. The sidebar starts collapsed on phones.

## [0.1.0] - 2026-10-02

### Added

- One Streamlit app for the Signal suite: front page (Claude Design "Signal Hub Page"), sidebar menu by family, and
  every embedded tool rendered through its `<package>.ui.render()` entry point inside an error-isolating wrapper.
- `apps.yaml` registry with validation; generated `requirements-apps.txt` (release-tag archive pins) and
  `local-apps.txt` (editable sibling clones).
- `signal-theme/`: master copy of the Organic Signal design kit (theme module, marks, banners, social previews,
  README template, topics) and `scripts/sync_theme.py` to copy it into each app. Influence Signal artwork
  regenerated for the 2026-10-01 rename with `signal-theme/tools/render_brand_images.py`.
- App contract (`docs/APP_CONTRACT.md`), brand rollout recipe (`docs/BRAND_ROLLOUT.md`), status page, GitHub profile
  and repository settings kit (`docs/github/`).
- Figtree embedded as `signal-theme/signal_font.py` (OFL), so no page requests Google Fonts; per-family
  contrast-ordered chart colorway; per-app upload caps (`max_upload_mb`) kept by the theme sync.
- Tests (registry, front page, per-app smoke tests), CI with an all-apps dependency-resolution job, Dockerfile and a
  GHCR image workflow, launchers for Windows and macOS.
