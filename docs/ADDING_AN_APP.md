# Adding an app to Signal

`apps.yaml` is the only place an app is listed. Everything else (the Hub's sidebar and cards, requirement pins,
the theme's app list, the README tables in this repo and in every app repo, topics, repo descriptions, the suite
size in prose) is read from it or written from it by `scripts/sync_suite.py`.

All commands run from the `signal-hub` folder. App repos are cloned next to it (`../<repo>`).

## 1. The app repo

The app is its own repo and Python package with a Streamlit UI. To run inside the Hub it follows the
[app contract](APP_CONTRACT.md):

- `src/<package>/ui/__init__.py` exposes `render()` and `APP_INFO = {"product", "version", "repo", "slug"}`.
- `render()` never calls `st.set_page_config` or `st.navigation`; pages sit behind a sidebar radio keyed
  `"<slug>:page"`.
- Every widget and session-state key goes through `k()` (`"<slug>:name"`).
- No Streamlit import outside `src/<package>/ui/`. `streamlit` and `plotly` go in the `ui` extra.
- Hub mode (`SIGNAL_HUB=1`): the fictional demo is preloaded, state lives in session memory, nothing is written to
  disk and nothing goes over the network.
- Demo data and anything else the UI reads ship as package data. No reads from the repo root.

## 2. The registry entry

Add the app to `apps.yaml`, in the family it belongs to (file order is menu order):

```yaml
- slug: shift                 # short id and session-state namespace
  key: shift                  # same as slug for new apps
  product: Shift Signal
  repo: cannibalization-analysis
  dist: shiftsignal           # pyproject [project].name
  package: shiftsignal        # import name
  tag: v1.0.0                 # the release the Hub pins
  family: Decide
  mode: embedded
  public: true
  max_upload_mb: 20
  question: Does a launch grow the portfolio, or move existing demand around?
  one_liner: Plan where a new item's volume will come from, then ...
  methods: [Source of volume, Difference-in-differences, Location bootstrap]
  tagline: "New demand, or demand moved around?"
  topics: [cannibalization, difference-in-differences]
```

## 3. Standard repo files

```bash
python scripts/scaffold_app.py shift
```

This adds whatever the repo is missing from `signal-theme/app-template/` and `signal-theme/README.template.md`,
filled in from the entry:

- the README skeleton;
- CHANGELOG, CITATION, CONTRIBUTING, PRIVACY, SECURITY, CODE_OF_CONDUCT;
- the Dockerfile and both launchers, on the next free port;
- the GitHub tests workflow, Dependabot, and issue and pull-request templates;
- `tests/test_hub_contract.py`.

It never overwrites a file. Then write the README sections that still hold `{{…}}`, and make the contract test pass.

## 4. Mark and brand images

Draw the mark as `signal-theme/assets/marks/<key>signal-mark.svg` in the suite style:
- `viewBox="0 0 96 96"`;
- a full circle in the family's 600 colour;
- a glyph in `#f9f4ed`, stroke 7;
- one accent dot in the family's 300 colour.

Copy an existing mark from the same family as a starting point, and add the SVG to `marks.json`. Then:

```bash
python scripts/sync_suite.py                                   # registers the app in signal_theme.APPS
python signal-theme/tools/render_brand_images.py shift         # mark PNGs, README banner, social preview
```

The image tool needs Edge or Chrome. The banner chips default to the entry's `methods`.

## 5. Sync every list

```bash
python scripts/sync_suite.py
```

This writes:
- the theme's app list and the requirement pins;
- this README's tables and suite size;
- the profile README;
- `topics.txt` and `docs/github/set_repo_metadata.ps1`;
- the "Where this fits in Signal" table in every app README;
- the theme copy, marks, banner, social preview and `.streamlit/config.toml` in every app clone.

`--check` lists what is stale. CI runs `--check --hub-only`.

## 6. Test, release, publish

1. In the app repo: `pytest`, `ruff check .`, `python -m build`; set version 1.0.0, write the CHANGELOG, commit and
   `git tag -a v1.0.0`.
2. Here: `pip install -e ../<repo>[ui]`, then `pytest` (the `apps` smoke tests render the new app inside the Hub).
3. Push the app with its tag first, then this repo and the other app repos the sync touched. The Hub's CI
   installs the app from the tag archive, so the tag must be on GitHub before the Hub push.
4. On GitHub:
   - make the app repo public;
   - run its line from `docs/github/set_repo_metadata.ps1` to set the description and topics;
   - upload `assets/<key>signal-social.png` as the social preview (Settings → Social preview).
5. Add a row to [STATUS.md](STATUS.md). Redeploy the Hub image.
