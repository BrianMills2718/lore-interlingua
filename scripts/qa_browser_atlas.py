"""Real-browser smoke test of the current offline encyclopedia and Experiment 014.

This is a functional UI regression check, *not* a human comprehension study.
Requirements:
    python -m pip install "playwright>=1.49,<2"
    python -m playwright install chromium

Run:
    python scripts/qa_browser_atlas.py --root . --out artifacts/browser-smoke
"""
import argparse
import json
import re
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def assert_no_document_overflow(page, label):
    state = page.evaluate("""() => ({
      windowWidth: document.documentElement.clientWidth,
      documentWidth: document.documentElement.scrollWidth
    })""")
    if state["documentWidth"] > state["windowWidth"] + 3:
        raise AssertionError(f"{label} has horizontal document overflow: {state}")


def assert_relations(page, reception, mediation):
    for key, expected in [("reception", reception), ("mediation", mediation)]:
        locator = page.locator("#relation-" + key)
        if expected:
            expect(locator).to_have_class(re.compile(r"\bis-visible\b"))
        else:
            expect(locator).not_to_have_class(re.compile(r"\bis-visible\b"))


def run(root: Path, out: Path):
    atlas = root / "encyclopedia" / "index.html"
    workbench = root / "experiments" / "014-conceptual-representation" / "index.html"
    assessment = root / "experiments" / "014-conceptual-representation" / "evaluation" / "index.html"
    for item in [atlas, workbench, assessment]:
        if not item.is_file():
            raise FileNotFoundError(f"Missing offline atlas asset: {item}")

    out.mkdir(parents=True, exist_ok=True)
    errors = []
    external_requests = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width": 1366, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: external_requests.append(request.url)
                if request.url.startswith(("https://", "http://")) else None)

        # 1. The actual library must render its navigation and local study link.
        page.goto(atlas.as_uri())
        expect(page.locator("#total-count")).to_have_text("13")
        expect(page.locator("a[href='../experiments/014-conceptual-representation/index.html']")).to_be_visible()
        page.screenshot(path=str(out / "01-encyclopedia-desktop.png"), full_page=True)
        assert_no_document_overflow(page, "encyclopedia desktop")

        # 2. One model, two distinct reveal orders, persistent participant identities.
        page.goto(workbench.as_uri() + "?mode=trace-from-earth")
        earth_first = page.locator("button[data-mode='trace-from-earth']")
        expect(earth_first).to_have_attribute("aria-pressed", "true")
        expect(page.locator("#beat-label")).to_have_text("Beat 1 / 3")
        assert_relations(page, False, False)
        expect(page.locator("#concept-earth")).to_have_class(re.compile(r"\bis-selected\b"))
        page.locator("#next-step").click()
        assert_relations(page, False, True)
        expect(page.locator("#beat-label")).to_have_text("Beat 2 / 3")
        page.locator("button[data-inspect='organic-life']").click()
        expect(page.locator("#focus-name")).to_have_text("Terrestrial organic life")
        expect(page.locator("#beat-label")).to_have_text("Beat 2 / 3")
        assert_relations(page, False, True)
        page.locator("#next-step").click()
        assert_relations(page, True, True)
        page.screenshot(path=str(out / "02-workbench-earth-first.png"), full_page=True)

        page.locator("button[data-mode='follow-influence']").click()
        expect(page.locator("#beat-label")).to_have_text("Beat 1 / 3")
        assert_relations(page, False, False)
        page.locator("#next-step").click()
        assert_relations(page, True, False)
        page.locator("#next-step").click()
        assert_relations(page, True, True)
        expect(page.locator("#storyboard-list .treatment")).to_have_count(2)
        expect(page.locator("#storyboard-list .shot-card")).to_have_count(6)
        expect(page.locator("#notation-list > div")).to_have_count(5)

        # 3. Responsive viewport retains navigation and contains the wide diagrams.
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator("button[data-mode='overview']").click()
        assert_relations(page, True, True)
        assert_no_document_overflow(page, "workbench mobile")
        page.screenshot(path=str(out / "03-workbench-mobile.png"), full_page=True)

        # 4. Test a synthetic (not human) full submission, answer locking and download.
        page.set_viewport_size({"width": 1366, "height": 900})
        page.goto(assessment.as_uri() + "?condition=trace-from-earth")
        expect(page.locator("#condition")).to_have_value("trace-from-earth")
        expect(page.locator("#lesson-link")).to_have_attribute("href", "../index.html?mode=trace-from-earth")
        expect(page.locator("#begin-comprehension")).to_be_disabled()
        page.screenshot(path=str(out / "04-assessment-introduction.png"), full_page=True)

        page.locator("#exposure-complete").check()
        page.locator("#begin-comprehension").click()
        expect(page.locator("#stage-comprehension")).to_be_visible()
        expect(page.locator("#stage-transfer")).to_be_hidden()

        page.locator('input[name="C1"][value="planet_life_earth"]').check()
        page.locator('input[name="C2"][value="mediated_relation_unavailable"]').check()
        page.locator('input[name="C3"][value="no_physical_mechanism"]').check()
        page.locator("#C4").fill("The planetary world is described as a source; living things receive and mediate the relation toward Earth.")
        page.locator("#begin-transfer").click()
        expect(page.locator("#stage-comprehension")).to_be_hidden()
        expect(page.locator("#stage-transfer")).to_be_visible()
        page.screenshot(path=str(out / "05-assessment-transfer.png"), full_page=True)

        page.locator('input[name="T1"][value="dashed_nara_ivo"]').check()
        page.locator('input[name="T2"][value="solid_ivo_selen"]').check()
        page.locator('input[name="T3"][value="ivo"]').check()
        page.locator('input[name="T4"][value="no_universal_mechanism"]').check()
        page.locator("#T5").fill("Synthetic QA response. No participant was involved.")
        page.locator("#finish").click()
        expect(page.locator("#stage-finish")).to_be_visible()
        expect(page.locator("#stage-transfer")).to_be_hidden()
        response = json.loads(page.locator("#response-json").input_value())
        assert response["schema"] == "lore-interlingua-experiment-014-formative-v1"
        assert response["condition"] == "trace-from-earth"
        assert response["comprehension"]["C1"] == "planet_life_earth"
        assert response["transfer"]["T2"] == "solid_ivo_selen"
        assert all(k not in response for k in ("name", "participant_id", "timestamp", "email"))
        page.screenshot(path=str(out / "06-assessment-finish.png"), full_page=True)

        with page.expect_download() as info:
            page.locator("#download").click()
        downloaded = info.value
        assert downloaded.suggested_filename == "experiment-014-anonymous-response.json"
        assert json.loads(downloaded.path().read_text(encoding="utf-8")) == response

        page.set_viewport_size({"width": 390, "height": 844})
        assert_no_document_overflow(page, "assessment mobile")
        page.screenshot(path=str(out / "07-assessment-mobile.png"), full_page=True)
        context.close()
        browser.close()

    if errors:
        raise AssertionError("Uncaught JavaScript errors: " + "; ".join(errors))
    if external_requests:
        raise AssertionError("The offline study made unexpected HTTP(S) requests: " + repr(external_requests))
    print("PASS: current encyclopedia, both Experiment 014 reveals, study stages, local download and mobile layout.")
    print("Synthetic QA only; no participant comprehension data were collected.")
    print(f"Browser screenshots: {out}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, default=Path("artifacts/browser-smoke"))
    args = parser.parse_args()
    run(args.root.resolve(), args.out.resolve())


if __name__ == "__main__":
    main()
