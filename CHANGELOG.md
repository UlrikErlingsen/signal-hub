# Changelog

All notable changes to Signal Hub are documented here.

## [0.1.0] - 2026-10-01

### Added

- One Streamlit app for the Signal suite: front page (Claude Design "Signal Hub Page"), sidebar menu by family, and
  every embedded tool rendered through its `<package>.ui.render()` entry point inside an error-isolating wrapper.
- `apps.yaml` registry with validation; generated `requirements-apps.txt` (release-tag archive pins) and
  `requirements-local.txt` (editable sibling clones).
- `signal-theme/`: master copy of the Organic Signal design kit (theme module, marks, banners, social previews,
  README template, topics) and `scripts/sync_theme.py` to copy it into each app. Influence Signal artwork
  regenerated for the 2026-10-01 rename with `signal-theme/tools/render_brand_images.py`.
- App contract (`docs/APP_CONTRACT.md`), brand rollout recipe (`docs/BRAND_ROLLOUT.md`), status page, GitHub profile
  and repository settings kit (`docs/github/`).
- Tests (registry, front page, per-app smoke tests), CI with an all-apps dependency-resolution job, Dockerfile and a
  GHCR image workflow, launchers for Windows and macOS.
