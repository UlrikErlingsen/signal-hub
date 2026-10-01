<!--
Signal README template. Replace every {{…}}. Keep the section order: readers learn it once and find
the same thing in every repo. Delete a section only if the app truly has nothing for it.
Move existing README text into the matching section; don't drop it.

{{Name}}        e.g. Measure Signal        (display name, with a space)
{{slug}}        e.g. measuresignal         (files, Docker tag)
{{ENV}}         e.g. MEASURESIGNAL         (launcher environment-variable prefix)
{{repo}}        e.g. measurement-validation
{{FAMILY}}      Brand | Market | Customer | Research | Decide
{{fam_hex}}     family 600 without "#": brand b2622d · market 728157 · customer aa5d83 · research a06f1f · decide 4f80a2
{{question}}    the one question the app answers, as a question
Repo topics:    signal-suite, signal-{{family}}, streamlit, local-first, + 2–3 method topics
Social preview: Settings → Social preview → upload assets/{{slug}}-social.png

Section map (old README → this template)
  badges + banner .................. header
  one-line promise + intro ......... header
  Read this first .................. Read this first
  Supported scope / does not ....... Scope
  Try it in three minutes .......... Try the demo
  Data layout ...................... Data contract
  Measurement/analysis contract .... Analysis contract (optional)
  Workflow / reliability / scoring . Methods
  Evidence-profile statuses ........ Decision statuses
  Evidence pack .................... Exports
  Run locally / Docker / env vars .. Run locally
  No install? AI file .............. No install
  Development checks ............... Development
  Relationship to the Signal suite . Where this fits
  Method references ................ References
  Originality and license .......... Originality and license
-->

<p align="center">
  <img src="assets/{{slug}}-banner.png" alt="{{Name}}: {{question}}" width="100%">
</p>

<p align="center">
  <a href="https://github.com/UlrikErlingsen/{{repo}}/actions"><img alt="Tests" src="https://github.com/UlrikErlingsen/{{repo}}/actions/workflows/tests.yml/badge.svg"></a>
  <a href="https://github.com/UlrikErlingsen/signal-hub"><img alt="Signal · {{FAMILY}}" src="https://img.shields.io/badge/Signal-{{FAMILY}}-{{fam_hex}}?labelColor=2e2b25"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-2e2b25?logo=python&logoColor=f9f4ed">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-app-{{fam_hex}}?logo=streamlit&logoColor=f9f4ed">
  <a href="LICENSE"><img alt="License: AGPL-3.0-or-later" src="https://img.shields.io/badge/License-AGPL--3.0--or--later-645c50"></a>
</p>

<p align="center"><strong>{{one-line promise, under 20 words}}</strong></p>

**{{Name}}** helps {{who}} {{do what}}. It combines {{the main parts, one sentence}}.

> {{question}}

Everything runs locally with open-source Python packages. There is no account, telemetry, external AI call, remote database, or built-in persistence.

## Read this first

{{What the result means and what it does not prove. 2–4 short paragraphs or bullets.}}

## Scope

**Version {{x.y}} supports:**

- {{supported input / method / check}}

**It does not:** {{comma-separated list of what is out of scope}}. Where a sibling app covers it, link it: use **[{{Sibling Signal}}](https://github.com/UlrikErlingsen/{{sibling-repo}})**.

## Try the demo in three minutes

1. Start the app and click **{{demo button label}}**.
2. {{step}}
3. {{step}}
4. Export the evidence pack as {{XLSX / CSV-ZIP / JSON}}.

The demo is deterministic synthetic data. It represents no real respondent, organisation, course case or empirical finding.

## Data contract

{{Shape (one row per …), formats (CSV, XLSX, JSON), limits, required and optional columns, what gets rejected and why.}}

| {{id_column}} | {{column}} | {{column}} |
|---|---|---|
| {{example}} | {{example}} | {{example}} |

See the [data guide](docs/data-guide.md).

## Analysis contract

{{Optional. The fields recorded before analysis, and why they keep the analysis honest. Note any starter templates.}}

## Methods

{{The workflow in order: audit → diagnostics → model → uncertainty → output. Name each method. Say when modeling is withheld.}}

See [methods](docs/methods.md).

## Decision statuses

{{Each status the app can return, in caps, with one line on what triggers it.}}

- **{{STATUS}}**: {{trigger}}

See the [decision guide](docs/decision-guide.md).

## Exports

Excel, CSV-ZIP and JSON exports include:

- source filename, sheet and SHA-256 fingerprint;
- the full contract and software version;
- {{app-specific tables}};
- the decision status, warnings and exact reproducibility settings.

{{What is excluded, e.g. respondent identifiers and row-level values.}} Exported text is neutralised against spreadsheet-formula interpretation.

## Run locally

You need Python 3.10 or newer and a local copy of this folder.

**macOS:** double-click `run_app.command`. **Windows:** double-click `run_app.bat`.

The first launch creates a private `.venv` and downloads open-source dependencies. Later launches reuse it. Or use a terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

{{Name}} prefers local port {{port}} and falls back to another free port on macOS. The launcher accepts `{{ENV}}_PORT`, `{{ENV}}_MAX_UPLOAD_MB`, `{{ENV}}_NO_BROWSER` and `{{ENV}}_DEBUG`.

### Docker

```bash
docker build -t {{slug}} .
docker run --rm -p {{port}}:{{port}} {{slug}}
```

Then open http://127.0.0.1:{{port}}. The container runs as a non-root user.

## Privacy

{{Two sentences: where data is processed; who is responsible on a hosted deployment.}} See [PRIVACY.md](PRIVACY.md).

## No install? Give this file to an AI

[AI_ANALYST.md](AI_ANALYST.md) is a standalone analysis protocol for a capable AI assistant, with the same scope limits, calculations and honesty rules. The local app is the more private option: a cloud AI sees whatever you upload or paste.

## Development

```bash
python -m pip install -e ".[test]"
python -m pytest
python -m ruff check .
python -m build
```

{{What the test suite checks, one sentence.}}

## Where this fits in Signal

{{One or two sentences: which app comes before or after this one, and why.}}

| App | Asks |
|---|---|
| [Track Signal](https://github.com/UlrikErlingsen/brand-tracking) | Is the brand moving, or is the tracker just noisy? |
| [Position Signal](https://github.com/UlrikErlingsen/brand-positioning) | Where do brands sit relative to competitors? |
| [Prospect Signal](https://github.com/UlrikErlingsen/b2b-prospecting) | Which Norwegian companies fit the ideal customer? |
| [Listen Signal](https://github.com/UlrikErlingsen/media-listening) | What are Norwegian media and social channels saying? |
| [Creator Signal](https://github.com/UlrikErlingsen/influencer-campaigns) | Which creators delivered, and was every post labelled? |
| [Season Signal](https://github.com/UlrikErlingsen/marketing-calendar) | What does the Norwegian marketing year look like, worked backwards? |
| [Adopt Signal](https://github.com/UlrikErlingsen/adoption-forecasting) | When will a new product be adopted? |
| [Worth Signal](https://github.com/UlrikErlingsen/customer-value-analytics) | What are customers and relationships worth? |
| [Segment Signal](https://github.com/UlrikErlingsen/customer-segmentation) | Do customers form stable, useful groups? |
| [Trace Signal](https://github.com/UlrikErlingsen/journey-path-analysis) | How do logged customer journeys actually unfold? |
| [Recommend Signal](https://github.com/UlrikErlingsen/recommender-evaluation) | Which recommendation policy should be tested live? |
| [Choice Signal](https://github.com/UlrikErlingsen/conjoint-analysis) | How do product attributes drive choice? |
| [Driver Signal](https://github.com/UlrikErlingsen/survey-driver-analysis) | Which measured experiences move with satisfaction? |
| [Measure Signal](https://github.com/UlrikErlingsen/measurement-validation) | Does a multi-item score have a defensible structure? |
| [Text Signal](https://github.com/UlrikErlingsen/open-text-analysis) | What recurring patterns appear in open-ended responses? |
| [Tag Signal](https://github.com/UlrikErlingsen/pricing-analysis) | What price range is supported, and how does profit move? |
| [Experiment Signal](https://github.com/UlrikErlingsen/experiment-analysis) | Did the treatment cause a practically meaningful change? |
| [Gate Signal](https://github.com/UlrikErlingsen/launch-decision-gate) | Does a concept deserve the next investment? |
| [Alloc Signal](https://github.com/UlrikErlingsen/marketing-mix-allocation) | Where should the next marketing budget go? |

The maintained public suite is listed at [ulrikerlingsen.com](https://ulrikerlingsen.com) and in [Signal Hub](https://github.com/UlrikErlingsen/signal-hub).

## References

- {{Author, A. (Year). Title. Journal, vol, pages. https://doi.org/…}}

## Originality and license

{{Name}} is an independent implementation based on public statistical literature and original synthetic examples. It does not reproduce lecture slides, institution-specific cases, teaching diagrams, exercises, exam questions, screenshots, tables or other institution-specific teaching material. See [sources and originality](docs/sources.md).

The software and documentation are free under AGPL-3.0-or-later. The license covers this project's expression, not ownership of published statistical methods.

This application was developed with AI coding assistance and checked through source review, analytical fixtures, deterministic synthetic tests, automated app tests and visual inspection. Verify material decisions independently; no warranty is provided.

---

<p>
  <img src="assets/{{slug}}-mark-64.png" width="20" height="20" alt="" align="absmiddle">
  <strong>{{Name}}</strong> is part of <a href="https://github.com/UlrikErlingsen/signal-hub"><strong>Signal</strong></a>, open marketing-evidence tools by <a href="https://ulrikerlingsen.com">Ulrik Erlingsen</a>.
</p>
