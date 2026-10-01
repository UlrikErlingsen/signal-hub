# Signal brand rollout: per-repo recipe

How each app repo moves to the Organic Signal brand (Claude Design "Unified Signal apps design", Oct 2026) and,
for the analytics apps, to the Hub contract in [APP_CONTRACT.md](APP_CONTRACT.md). One repo = one pass through this
list. The worked example is `brand-tracking` (Track Signal).

Source of the design: `signal-theme/` in this repo (theme module, marks, banners, social previews, README template,
topics). `scripts/sync_theme.py` has already copied the synced files into every app clone (see its docstring). Never
edit the synced copies in an app repo; change `signal-theme/` here and re-sync.

## Naming

- Display name has a space: **Track Signal**, **Worth Signal**, **Influence Signal** (not "TrackSignal").
  Use it in every user-facing place: UI text, page title, sidebar, masthead, footer, README, docs, issue templates,
  export metadata labels shown to people.
- Do not rename technical identifiers: package/import names, dist names, env-var prefixes (`TRACKSIGNAL_PORT`),
  Docker image tags, Unix user names, file slugs (`tracksignal-banner.png`), JSON keys that are part of a data
  contract, or anything a test fixture or stored file depends on.
- `influencer-campaigns` is **Influence Signal** (renamed from CreatorSignal on 2026-10-01). Never write "Creator Signal".
- Name-screen notes and `docs/name-screen.md` keep their substance. Do not claim any new legal clearance.

## A. Every repo (all 19)

1. **Theme.** Replace the pasted `<style>` block and the hand-written lockup, masthead, hero, cards, header, notes and
   footer with `signal_theme` (imported as `sig` from `<package>.ui`):
   `sig.apply(key)`, `sig.sidebar_brand(key, tagline)`, `sig.masthead(key, promises, kicker)`,
   `sig.hero(...)`, `sig.cards(...)`, `sig.header(...)`, `sig.note("info"|"warn"|"boundary", text)`,
   `sig.footer(key, __version__, line)`. Keep the app's own words (eyebrow, hero title, kicker, promises, footer line).
   Old CSS classes such as `.boundary`, `.warning-box`, `.small-note` become `sig.note(...)` or `st.caption(...)`.
2. **Charts.** `sig.apply()` registers the Plotly templates (Figtree, family colorway). Pass the per-app template to
   every figure and show it with `sig.chart(key, fig, key=k("..."))` (sets the template and `theme=None`, so
   Streamlit's chart theme does not replace Figtree). If you call `st.plotly_chart` directly, pass `theme=None` and
   `template=sig.template(key)` (the process-wide default is shared across Hub sessions). Use `sig.roles(key)` for semantic
   colours, not the global `sig.ROLES`. `sig.note("muted", ...)` replaces small-print notes; notes support **bold**, `code`, [links](https://...) and blank-line paragraphs. Remove hard-coded old
   palette colours (`#173C3A`, `#D95B40`, `#83D2B4`, `#F2C66D`, the old per-app greens/teals, etc.). Map them to:
   categorical series → `sig.colorway(key)`; sequential → `sig.sequential(key)`; diverging → `sig.DIVERGING`;
   estimate → `sig.CORE["text"]`; interval/band → `sig.CORE["soft"]`; practical threshold →
   `sig.FAMILIES["brand"]["600"]`; highlighted/own series → `sig.app(key)["fam"]["600"]`; zero line →
   `sig.CORE["muted"]`. Keep chart meaning identical.
3. **Page config.** `st.set_page_config(**sig.page_config(key))` in the standalone `app.py` (favicon = the mark).
4. **Assets.** The synced files are in `assets/` (`<slug>-banner.png`, `-social.png`, `-mark.svg`,
   `-mark-32/64/512.png`). Update every reference (README, app, tests, Dockerfile, docs, pyproject) to them, then
   delete superseded brand files in `assets/` (old `*-banner.svg`, old lockups, old marks with other names). Keep
   anything that is not branding (screenshots, examples).
5. **`.streamlit/config.toml`** is synced (family `primaryColor`, cream background). Keep it.
6. **README** follows `signal-theme/README.template.md`: banner PNG, the five badges with the family colour, promise,
   intro, question callout, then the sections in template order, the "Where this fits in Signal" table, References,
   Originality and license, and the suite footer with the 64 px mark. Move existing text into the matching section;
   do not drop content, honesty statements, scope limits or references. Keep sentences tests rely on for substance
   (e.g. "does **not** manufacture a universal ...") unless you update the test with an equivalent statement.
7. **Issue templates.** Add `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml` and `config.yml` modelled
   on `customer-value-analytics/.github/ISSUE_TEMPLATE/` (product name and repo URL substituted, data-safety wording
   kept). Keep the existing PR template.
8. **Tests.** Update tests that assert the old palette, old names, old README headings or old asset paths so they
   assert the new brand instead (theme import, family colour in config, banner PNG in README, new section headings,
   display name). Do not weaken analytical, privacy, boundary or originality tests.
9. **pyproject.** Add `[tool.setuptools.package-data] "<package>.ui" = ["assets/marks/*"]` (merge with any existing
   package-data). Keep version ranges compatible with the shared environment (streamlit 1.64, plotly 7.1,
   pandas 2.3, numpy 2.5).

## B. Analytics apps (15): Hub contract + release

10. Refactor to [APP_CONTRACT.md](APP_CONTRACT.md): `src/<package>/ui/__init__.py` with `APP_INFO` and `render()`,
    the app body inside functions, thin `app.py`, slug-namespaced session-state and widget keys, `streamlit` in a
    `ui` extra (plus `test` extra), guard test that allows only `ui/` to import Streamlit, and a test that renders
    `render()` from a script without `set_page_config`.
11. Release: bump the **minor** version (x.Y.0) in pyproject, `__init__.__version__` and `CITATION.cff`; add a CHANGELOG
    entry ("Signal brand refresh and Signal Hub entry point"); commit; create an annotated tag
    `git tag -a vX.Y.0 -m "<Name> vX.Y.0"`. Do not push.

## C. Norwegian apps (4, pre-v1, private): brand only

`b2b-prospecting`, `media-listening`, `influencer-campaigns`, `marketing-calendar`. Do section A only. They use
`st.navigation` with `pages/`; keep that. Swap their own theme helpers (`pages/ui.py` `apply_theme`, `st.logo` with
old lockups) for `signal_theme`. Their repo rules (CLAUDE.md / AGENTS.md) still apply; amend "no Streamlit under
src/" to "except `src/<package>/ui/`" in the rule text and the guard test. No version bump or tag: add the changes
under `## [Unreleased]` in the CHANGELOG. `marketing-calendar`: widen `plotly` to `>=5.18,<8` so it installs next
to the other apps.

## Verify and commit

- Run, from the repo folder, with the shared environment (do not install packages into it):
  `"C:/Users/callo/OneDrive/All/Dokumenter/GitHub/Signal Hub/.venv/Scripts/python.exe" -m pytest -q` and
  `... -m ruff check .` Both must pass.
- Commit locally on `main` in small logical commits (theme, README/assets, contract, release). End each commit
  message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Never push.
