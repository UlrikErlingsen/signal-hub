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

All tags above exist locally and are **not pushed yet**. The Hub's pinned installs (`requirements-apps.txt`) only work
once each app's `main` and tag are pushed to GitHub.

## Open follow-ups

- Push every app repo with its tag, then this repo (see the hand-off in the session summary).
- GitHub settings that are not in git: descriptions/topics (`docs/github/set_repo_metadata.ps1`), social previews
  (by hand), profile README (`docs/github/profile-README.md`), optional rename of `Signal-Hub` to `signal-hub`.
- Some apps open on a welcome page with demo buttons instead of a preloaded demo (Adopt, Choice, Segment, Worth,
  Driver, Experiment, Alloc, Position, Tag). Decide whether the Hub should preload them.
- README screenshots in Prospect and Season Signal still show the old look; Influence and Listen were re-shot.
- Research colorway: the first two hues (Research 600, Brand 600) are close; a family-specific order in
  `colorway()` would help, but apps index into it today, so change it together with those charts.
- Figtree loads from Google Fonts in every app; self-hosting the font would remove the only third-party request.
- Phase 4: deploy to the VPS (`deploy/README.md`) and the tag-bump automation.
