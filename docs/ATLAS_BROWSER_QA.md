# Atlas browser QA and review screenshots

**Status:** This is a **real-browser functional regression check**, not an audience comprehension study, source-text audit, proof of cross-tradition notation or accessibility certification.

## What it checks

The [Playwright smoke script](../scripts/qa_browser_atlas.py) opens the repository's **actual offline HTML** in Chromium. It verifies:

1. The encyclopedia loads its 13-concept directory and links to the current Experiment 014 workbench.
2. Earth-first mode starts with **no disclosed relation** and reveals mediation before reception, preserving the model and its relationship directions.
3. Source-first mode discloses **reception** before mediation. All three participants stay visible. Inspecting one does **not** change the explanatory beat.
4. The workbench has two manual storyboard treatments (six beats) and five provisional notation mappings.
5. The assessment opens its assigned presentation condition, requires an exposure self-report, and keeps the transfer task hidden until comprehension answers are captured.
6. A **synthetic QA response** completes the staged questionnaire and explicitly downloads a local JSON file. Browser errors and unexpected HTTP(S) requests fail the test.
7. Desktop and mobile views avoid document-wide horizontal overflow (wide diagrams may scroll inside their intended panels).

Successful execution saves screenshots for review and uploads them as the **lore-interlingua-browser-qa** Actions artifact for 30 days.

## How to inspect the results

Open [Browser QA workflow runs](https://github.com/BrianMills2718/lore-interlingua/actions/workflows/qa-atlas-browser.yml). Choose a successful run for the commit you want. Download the **lore-interlingua-browser-qa** artifact under **Artifacts**, then inspect the numbered screenshots. **These images are software screenshots, not human responses.**

For a complete, **currently built offline encyclopedia**, use the separate [Publish Visual–Semantic Encyclopedia workflow](https://github.com/BrianMills2718/lore-interlingua/actions/workflows/publish-encyclopedia.yml) and download the **lore-interlingua-current-offline-atlas** artifact. Extract it and open the top-level index.html. This does not depend on successful GitHub Pages activation.

## Reproduce locally

Requires Python 3.11+ and the Playwright Chromium browser:

    python -m pip install "playwright>=1.49,<2"
    python -m playwright install chromium
    python scripts/qa_browser_atlas.py --root . --out artifacts/browser-smoke

The script deliberately uses file:// URLs so missing local scripts or broken relative links are detectable. The workbench itself needs no remote services.

## Evidence boundaries

A passing browser check does **not** demonstrate that people understand the relations, that the notation improves learning, or that every accessibility requirement is met. The synthetic export used for smoke testing must **not** be presented as a human participant response. Site hosting remains separately verified; a successful package or browser QA job cannot prove that GitHub Pages is live.

For real research, use the [Experiment 014 formative protocol](../experiments/014-conceptual-representation/evaluation/README.md), collect only voluntary responses, and assess comprehension and notation transfer separately. Do not commit participant data or identifiers to this public repository.
