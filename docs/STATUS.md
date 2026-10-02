# Status

Last updated 2026-10-02. Source of truth for modes and tags: [`apps.yaml`](../apps.yaml).

| Family | App | Repo | Mode | Hub pins | Notes |
|---|---|---|---|---|---|
| Brand | Track Signal | brand-tracking | embedded | v1.1.0 | reference implementation of the contract |
| Brand | Position Signal | brand-positioning | embedded | v1.2.0 | `positionsignal.plotting` moved to `positionsignal.ui.plotting` |
| Market | Prospect Signal | b2b-prospecting | coming_soon | – | private until v1; brand refresh done |
| Market | Listen Signal | media-listening | coming_soon | – | private until v1; brand refresh done |
| Market | Influence Signal | influencer-campaigns | coming_soon | – | private until v1; renamed from CreatorSignal 2026-10-01; brand refresh done |
| Market | Season Signal | marketing-calendar | coming_soon | – | private until v1; plotly widened to `<8`; brand refresh done |
| Market | Adopt Signal | adoption-forecasting | embedded | v1.2.0 | demos generated in code |
| Customer | Worth Signal | customer-value-analytics | embedded | v1.2.0 | consolidation with Freddo's signal-core not started (CLAUDE.md §7) |
| Customer | Segment Signal | customer-segmentation | embedded | v1.2.0 | demos generated in code |
| Customer | Trace Signal | journey-path-analysis | embedded | v1.1.0 | |
| Customer | Recommend Signal | recommender-evaluation | embedded | v1.1.0 | |
| Research | Choice Signal | conjoint-analysis | embedded | v1.3.0 | demo CSVs bundled as package data |
| Research | Driver Signal | survey-driver-analysis | embedded | v1.1.0 | demos generated in code |
| Research | Measure Signal | measurement-validation | embedded | v1.3.0 | demo preloads |
| Research | Text Signal | open-text-analysis | embedded | v1.2.0 | demo preloads |
| Research | Tag Signal | pricing-analysis | embedded | v1.2.0 | |
| Decide | Experiment Signal | experiment-analysis | embedded | v1.2.0 | |
| Decide | Gate Signal | launch-decision-gate | embedded | v1.2.0 | |
| Decide | Alloc Signal | marketing-mix-allocation | embedded | v1.2.0 | Dockerfile `USER` line fixed |

All tags above are pushed to GitHub; the Hub's pinned installs (`requirements-apps.txt`) resolve from them.

## Open follow-ups

- GitHub settings outside git: descriptions/topics (`docs/github/set_repo_metadata.ps1`, needs the GitHub CLI),
  social previews (by hand), profile README (`docs/github/profile-README.md`).
- Phase 4: deploy to the VPS (`deploy/README.md`, done through the VPS chat) and the tag-bump automation.
- WorthSignal consolidation with Freddo's signal-core (CLAUDE.md §7): needs a file list approved before touching
  signal-crm.

## Done 2026-10-02

- Every embedded app opens with its fictional demo preloaded (some still need one click to run the analysis).
- Figtree is embedded (`signal-theme/signal_font.py`); no app or Hub page requests Google Fonts.
- The colorway uses a per-family contrast order (Research charts no longer pair ochre with terracotta).
- Prospect and Season Signal README screenshots re-taken in the new theme.
