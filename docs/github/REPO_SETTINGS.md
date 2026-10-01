# GitHub repository settings

The design (Claude Design "Signal GitHub") asks for the same metadata on every Signal repo. None of it lives in git,
so it is applied once per repo. `set_repo_metadata.ps1` does descriptions, homepages and topics with the GitHub CLI.

## Social preview (by hand, once per repo)

GitHub has no API for this. For each repo: **Settings → General → Social preview → Edit → Upload an image** and pick
`assets/<slug>-social.png` from that repo (1280×640). For this repo use `signal-theme/assets/social/signalhub-social.png`.

## Profile

Copy [profile-README.md](profile-README.md) into the `UlrikErlingsen/UlrikErlingsen` repository's README. Pin, in order:
signal-hub, customer-value-analytics, brand-tracking, experiment-analysis, then signal-crm (Freddo) as the separate product.
Prospect Signal joins the pins when b2b-prospecting goes public at v1.

## Repo name

The repository was created as `Signal-Hub`. Every link in the suite uses `signal-hub`; GitHub treats them the same,
but renaming it to lowercase in **Settings → General** keeps the URL identical everywhere. GitHub Desktop follows the rename.

## Descriptions and topics

| Repo | Description | Topics |
|---|---|---|
| signal-hub | Signal Hub: every Signal marketing-evidence tool behind one link. Open-source, local-first. | signal-suite, streamlit, local-first, marketing-analytics, portfolio |
| brand-tracking | Track Signal: is the brand moving, or is the tracker just noisy? Open-source, local-first Streamlit app. | signal-suite, signal-brand, streamlit, local-first, brand-tracking, survey-analysis |
| brand-positioning | Position Signal: where do brands sit relative to competitors? Open-source, local-first Streamlit app. | signal-suite, signal-brand, streamlit, local-first, perceptual-mapping, pca |
| b2b-prospecting | Prospect Signal: which Norwegian companies fit your ideal customer, and which first? Open-source, local-first Streamlit app. | signal-suite, signal-market, streamlit, local-first, b2b, brreg |
| media-listening | Listen Signal: who is talking about the brand in Norwegian media, and in what tone? Open-source, local-first Streamlit app. | signal-suite, signal-market, streamlit, local-first, media-monitoring, sentiment-analysis |
| influencer-campaigns | Influence Signal: which creators delivered, and was every post labelled properly? Open-source, local-first Streamlit app. | signal-suite, signal-market, streamlit, local-first, influencer-marketing, norway |
| marketing-calendar | Season Signal: what does the Norwegian marketing year look like, worked backwards? Open-source, local-first Streamlit app. | signal-suite, signal-market, streamlit, local-first, marketing-calendar, norway |
| adoption-forecasting | Adopt Signal: when will a new product be adopted? Open-source, local-first Streamlit app. | signal-suite, signal-market, streamlit, local-first, bass-diffusion, forecasting |
| customer-value-analytics | Worth Signal: what are customers and relationships worth? Open-source, local-first Streamlit app. | signal-suite, signal-customer, streamlit, local-first, clv, rfm |
| customer-segmentation | Segment Signal: do customers form stable, useful groups? Open-source, local-first Streamlit app. | signal-suite, signal-customer, streamlit, local-first, segmentation, clustering |
| journey-path-analysis | Trace Signal: how do logged customer journeys actually unfold? Open-source, local-first Streamlit app. | signal-suite, signal-customer, streamlit, local-first, customer-journey, markov-chain |
| recommender-evaluation | Recommend Signal: which recommendation policy should be tested live? Open-source, local-first Streamlit app. | signal-suite, signal-customer, streamlit, local-first, recommender-systems, offline-evaluation |
| conjoint-analysis | Choice Signal: how do product attributes drive choice? Open-source, local-first Streamlit app. | signal-suite, signal-research, streamlit, local-first, conjoint-analysis, market-research |
| survey-driver-analysis | Driver Signal: which measured experiences move with satisfaction? Open-source, local-first Streamlit app. | signal-suite, signal-research, streamlit, local-first, driver-analysis, survey-analysis |
| measurement-validation | Measure Signal: does a multi-item score have a defensible structure? Open-source, local-first Streamlit app. | signal-suite, signal-research, streamlit, local-first, psychometrics, factor-analysis |
| open-text-analysis | Text Signal: what recurring patterns appear in open-ended responses? Open-source, local-first Streamlit app. | signal-suite, signal-research, streamlit, local-first, text-analysis, nmf |
| pricing-analysis | Tag Signal: what price range is supported, and how does profit move? Open-source, local-first Streamlit app. | signal-suite, signal-research, streamlit, local-first, pricing, price-elasticity |
| experiment-analysis | Experiment Signal: did the treatment cause a practically meaningful change? Open-source, local-first Streamlit app. | signal-suite, signal-decide, streamlit, local-first, ab-testing, experimentation |
| launch-decision-gate | Gate Signal: does a concept deserve the next investment? Open-source, local-first Streamlit app. | signal-suite, signal-decide, streamlit, local-first, new-product-development, stage-gate |
| marketing-mix-allocation | Alloc Signal: where should the next marketing budget go? Open-source, local-first Streamlit app. | signal-suite, signal-decide, streamlit, local-first, marketing-mix, budget-optimization |
