# Status

Last updated 2026-10-02. Source of truth for modes and tags: [`apps.yaml`](../apps.yaml).

| Family | App | Repo | Mode | Hub pins | Notes |
|---|---|---|---|---|---|
| Brand | Track Signal | brand-tracking | embedded | v1.1.0 | reference implementation of the contract |
| Brand | Position Signal | brand-positioning | embedded | v1.2.0 | `positionsignal.plotting` moved to `positionsignal.ui.plotting` |
| Market | Prospect Signal | b2b-prospecting | embedded | v1.0.0 | Hub mode: offline demo, in-memory DuckDB, no Brreg calls |
| Market | Listen Signal | media-listening | embedded | v1.0.0 | Hub mode: demo corpus only, no feed collection, lexicon sentiment |
| Market | Influence Signal | influencer-campaigns | embedded | v1.0.0 | renamed from CreatorSignal; Hub mode: in-memory SQLite workspace |
| Market | Season Signal | marketing-calendar | embedded | v1.0.0 | Hub mode: campaigns in session memory |
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

- Optional: pin repos on the GitHub profile.
- Phase 4: deploy to the VPS (`deploy/README.md`, done through the VPS chat) and the tag-bump automation.
- WorthSignal consolidation with Freddo's signal-core (CLAUDE.md §7): needs a file list approved before touching
  signal-crm.

## Done 2026-10-02

- Every embedded app opens with its fictional demo preloaded (some still need one click to run the analysis).
- Figtree is embedded (`signal-theme/signal_font.py`); no app or Hub page requests Google Fonts.
- The colorway uses a per-family contrast order (Research charts no longer pair ochre with terracotta).
- Prospect and Season Signal README screenshots re-taken in the new theme.
- GitHub: repo renamed to `signal-hub` and made public; descriptions (spaced names), Signal Hub homepage and
  suite topics on all 20 repos; social previews on all 20 repos (the four Norwegian ones went public on 2026-10-02); profile README in
  `UlrikErlingsen/UlrikErlingsen`.
