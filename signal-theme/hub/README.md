<p align="center"><img src="assets/signalhub-banner.png" alt="Signal Hub — open, local-first marketing evidence tools" width="100%"></p>

<p align="center"><strong>Nineteen small apps. Each answers one marketing question, shows its method, and runs on your own machine.</strong></p>

## <img src="https://img.shields.io/badge/-%20-b2622d?style=flat-square" height="14" alt=""> Brand

| | App | Question | Repo |
|---|---|---|---|
| <img src="assets/marks/tracksignal-mark-64.png" width="28" alt=""> | **Track Signal** | Is the brand moving, or is the tracker just noisy? | [brand-tracking](https://github.com/UlrikErlingsen/brand-tracking) |
| <img src="assets/marks/positionsignal-mark-64.png" width="28" alt=""> | **Position Signal** | See where brands stand | [brand-positioning](https://github.com/UlrikErlingsen/brand-positioning) |

## <img src="https://img.shields.io/badge/-%20-728157?style=flat-square" height="14" alt=""> Market

| | App | Question | Repo |
|---|---|---|---|
| <img src="assets/marks/prospectsignal-mark-64.png" width="28" alt=""> | **Prospect Signal** | Norwegian B2B prospecting from open Brønnøysund data | [b2b-prospecting](https://github.com/UlrikErlingsen/b2b-prospecting) |
| <img src="assets/marks/listensignal-mark-64.png" width="28" alt=""> | **Listen Signal** | Norwegian media and social listening | [media-listening](https://github.com/UlrikErlingsen/media-listening) |
| <img src="assets/marks/influencesignal-mark-64.png" width="28" alt=""> | **Influence Signal** | Which creators delivered, and was every post labelled properly? | [influencer-campaigns](https://github.com/UlrikErlingsen/influencer-campaigns) |
| <img src="assets/marks/seasonsignal-mark-64.png" width="28" alt=""> | **Season Signal** | The Norwegian marketing year, worked backwards | [marketing-calendar](https://github.com/UlrikErlingsen/marketing-calendar) |
| <img src="assets/marks/adoptsignal-mark-64.png" width="28" alt=""> | **Adopt Signal** | Know when the market will follow | [adoption-forecasting](https://github.com/UlrikErlingsen/adoption-forecasting) |

## <img src="https://img.shields.io/badge/-%20-aa5d83?style=flat-square" height="14" alt=""> Customer

| | App | Question | Repo |
|---|---|---|---|
| <img src="assets/marks/worthsignal-mark-64.png" width="28" alt=""> | **Worth Signal** | Find the customers, value, and moves that matter | [customer-value-analytics](https://github.com/UlrikErlingsen/customer-value-analytics) |
| <img src="assets/marks/segmentsignal-mark-64.png" width="28" alt=""> | **Segment Signal** | Find the groups worth understanding | [customer-segmentation](https://github.com/UlrikErlingsen/customer-segmentation) |
| <img src="assets/marks/tracesignal-mark-64.png" width="28" alt=""> | **Trace Signal** | Where do journeys flow, stall, and end? | [journey-path-analysis](https://github.com/UlrikErlingsen/journey-path-analysis) |
| <img src="assets/marks/recommendsignal-mark-64.png" width="28" alt=""> | **Recommend Signal** | Compare recommendation policies before the live test | [recommender-evaluation](https://github.com/UlrikErlingsen/recommender-evaluation) |

## <img src="https://img.shields.io/badge/-%20-a06f1f?style=flat-square" height="14" alt=""> Research

| | App | Question | Repo |
|---|---|---|---|
| <img src="assets/marks/choicesignal-mark-64.png" width="28" alt=""> | **Choice Signal** | Know what customers actually value | [conjoint-analysis](https://github.com/UlrikErlingsen/conjoint-analysis) |
| <img src="assets/marks/driversignal-mark-64.png" width="28" alt=""> | **Driver Signal** | See what moves with satisfaction and what to test next | [survey-driver-analysis](https://github.com/UlrikErlingsen/survey-driver-analysis) |
| <img src="assets/marks/measuresignal-mark-64.png" width="28" alt=""> | **Measure Signal** | Is this score measuring what you think it is? | [measurement-validation](https://github.com/UlrikErlingsen/measurement-validation) |
| <img src="assets/marks/textsignal-mark-64.png" width="28" alt=""> | **Text Signal** | What are people actually saying, and does the pattern hold? | [open-text-analysis](https://github.com/UlrikErlingsen/open-text-analysis) |
| <img src="assets/marks/tagsignal-mark-64.png" width="28" alt=""> | **Tag Signal** | What price range is supported, and how does profit move? | [pricing-analysis](https://github.com/UlrikErlingsen/pricing-analysis) |

## <img src="https://img.shields.io/badge/-%20-4f80a2?style=flat-square" height="14" alt=""> Decide

| | App | Question | Repo |
|---|---|---|---|
| <img src="assets/marks/experimentsignal-mark-64.png" width="28" alt=""> | **Experiment Signal** | Did the treatment cause a change worth acting on? | [experiment-analysis](https://github.com/UlrikErlingsen/experiment-analysis) |
| <img src="assets/marks/gatesignal-mark-64.png" width="28" alt=""> | **Gate Signal** | Know when the evidence deserves the next investment | [launch-decision-gate](https://github.com/UlrikErlingsen/launch-decision-gate) |
| <img src="assets/marks/allocsignal-mark-64.png" width="28" alt=""> | **Alloc Signal** | Put the next budget where it works hardest | [marketing-mix-allocation](https://github.com/UlrikErlingsen/marketing-mix-allocation) |

## How the apps fit together

Apps hand off rather than overlap: a tracking contrast in Track Signal is not a causal effect, so it points to Experiment Signal; construct scores need Measure Signal evidence first. Each README names its siblings under **Read this first**.

## Shared design

Every app imports `signal_theme.py` for its look, marks and chart palette. One accent per family.

---

All repos carry the `signal-suite` topic: [browse them](https://github.com/topics/signal-suite). Freddo CRM is a separate product.
By [Ulrik Erlingsen](https://ulrikerlingsen.com) · AGPL-3.0-or-later
