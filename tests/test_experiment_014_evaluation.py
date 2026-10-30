"""Regression checks for the *instrument*, not for human learning outcomes."""
import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "014-conceptual-representation"
STUDY = EXP / "evaluation"

spec = importlib.util.spec_from_file_location("li014_scorer", STUDY / "score_results.py")
scorer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorer)


class ControlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.radios = {}
        self.ids = set()
        self.forms = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "input" and attrs.get("type") == "radio":
            self.radios.setdefault(attrs.get("name"), set()).add(attrs.get("value"))
        if tag == "form":
            self.forms.append(attrs)
        if tag == "script":
            self.scripts.append(attrs.get("src"))


def synthetic_record():
    return {
        "schema": scorer.SCHEMA,
        "condition": "follow-influence",
        "exposure_self_reported_complete": True,
        "comprehension": {
            **scorer.KEYS["comprehension"],
            "C4": "Planetary influences are received by organic life, which mediates them to Earth."
        },
        "transfer": {
            **scorer.KEYS["transfer"],
            "T5": "The solid line was more distinct to me."
        },
        "note": "Synthetic fixture, NOT a participant response."
    }


class Experiment014EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (STUDY / "index.html").read_text(encoding="utf-8")
        cls.js = (STUDY / "study.js").read_text(encoding="utf-8")
        cls.parser = ControlParser()
        cls.parser.feed(cls.html)

    def test_ui_options_match_scoring_key(self):
        self.assertEqual(self.parser.radios, scorer.OPTIONS)
        for section in scorer.KEYS.values():
            for key, correct in section.items():
                self.assertIn(correct, scorer.OPTIONS[key])

    def test_local_only_and_staged_form(self):
        self.assertEqual(self.parser.scripts, ["study.js"])
        self.assertEqual(len(self.parser.forms), 2)
        for form in self.parser.forms:
            self.assertNotIn("action", form)
            self.assertNotIn("method", form)
        self.assertTrue({
            "stage-setup", "stage-comprehension", "stage-transfer", "stage-finish",
            "condition", "lesson-link", "begin-comprehension", "begin-transfer",
            "finish", "response-json", "download", "copy", "C4", "T5"
        } <= self.parser.ids)
        self.assertIn('id="stage-transfer" hidden', self.html)
        self.assertIn('id="stage-comprehension" hidden', self.html)
        self.assertIn('id="stage-finish" hidden', self.html)
        self.assertIn('href="../index.html?mode=follow-influence"', self.html)
        self.assertIn("state.comprehension = Object.assign", self.js)
        self.assertIn('setStage("transfer")', self.js)
        self.assertIn('setStage("finish")', self.js)
        self.assertIn("Blob(", self.js)  # local download
        for blocked in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage",
                        "sessionStorage", "document.cookie"]:
            self.assertNotIn(blocked, self.js)
        self.assertNotIn("https://", self.js)

    def test_transfer_is_a_reversed_unlabelled_sign_task(self):
        self.assertIn("A solid arrow points left from Ivo to Selen.", self.html)
        self.assertIn("A dashed arrow points left from Nara to Ivo.", self.html)
        self.assertIn('aria-labelledby="transfer-title transfer-description"', self.html)
        transfer_visual = self.html.split('<svg viewBox="0 0 840 282"', 1)[1].split("</svg>", 1)[0]
        for name in ("Selen", "Ivo", "Nara"):
            self.assertIn(name, transfer_visual)
        # Source/intermediary/recipient role labels must not be printed on the new diagram.
        for label in (">SOURCE<", ">INTERMEDIARY<", ">RECIPIENT<"):
            self.assertNotIn(label, transfer_visual)

    def test_all_correct_scoring_and_manual_coding_separation(self):
        report = scorer.score_record(synthetic_record())
        self.assertEqual(report["comprehension"]["correct"], 3)
        self.assertEqual(report["transfer"]["correct"], 4)
        self.assertEqual(report["comprehension"]["missing"], 0)
        self.assertEqual(report["transfer"]["missing"], 0)
        self.assertEqual(report["diagnostic_response_patterns"], [])
        self.assertTrue(report["open_reconstruction_requires_manual_coding"])
        self.assertTrue(report["open_misreading_requires_review"])
        self.assertNotIn("Planetary influences", json.dumps(report))
        stats = scorer.summarize([report])
        self.assertEqual(stats["follow-influence"]["n"], 1)
        self.assertEqual(stats["follow-influence"]["comprehension_items_possible"], 3)
        self.assertEqual(stats["follow-influence"]["transfer_items_possible"], 4)

    def test_missing_unsure_and_misreadings_are_distinct(self):
        record = synthetic_record()
        record["condition"] = "trace-from-earth"
        record["comprehension"].update(
            C1="planet_earth_life", C2="all_natural_forces_stop", C3=None, C4=""
        )
        record["transfer"].update(
            T1="solid_ivo_selen", T2="dashed_nara_ivo", T3="unsure", T4=None, T5=""
        )
        report = scorer.score_record(record)
        self.assertEqual(report["comprehension"]["correct"], 0)
        self.assertEqual(report["comprehension"]["missing"], 1)
        self.assertEqual(report["transfer"]["missing"], 1)
        self.assertEqual(report["transfer"]["unsure"], 1)
        self.assertEqual(
            set(report["diagnostic_response_patterns"]),
            {"direct-bypass", "universal-no-forces", "notation-sign-reversal"}
        )
        self.assertFalse(report["open_reconstruction_requires_manual_coding"])
        self.assertEqual(scorer.summarize([report])["trace-from-earth"]["n"], 1)

    def test_invalid_payloads_are_rejected(self):
        invalids = [
            {"schema": "wrong"},
            {"condition": "other"},
            {"exposure_self_reported_complete": False},
            {"comprehension": {"C1": "not-a-code"}},
            {"transfer": {"T2": "not-a-code"}},
            {"comprehension": {"C4": "x" * 901}},
        ]
        for update in invalids:
            with self.subTest(value=update):
                record = synthetic_record()
                for key, value in update.items():
                    if isinstance(value, dict) and key in ("comprehension", "transfer"):
                        record[key].update(value)
                    else:
                        record[key] = value
                with self.assertRaises(ValueError):
                    scorer.score_record(record)

    def test_assigned_workbench_mode_is_supported(self):
        source = (EXP / "study.js").read_text(encoding="utf-8")
        self.assertIn("requestedMode", source)
        self.assertIn("mode=(follow-influence|trace-from-earth)", source)
        self.assertIn("if (requestedMode) selectMode(requestedMode[1]);", source)

    def test_javascript_syntax_and_behavior(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node unavailable, local fake-DOM behavior not exercised.")
        for script in (STUDY / "study.js", EXP / "study.js"):
            result = subprocess.run(
                [node, "--check", str(script)],
                cwd=ROOT, capture_output=True, text=True, timeout=20
            )
            self.assertEqual(result.returncode, 0, result.stderr)
        script = ROOT / "tests" / "fixtures" / "experiment014-evaluation-smoke.cjs"
        result = subprocess.run([node, str(script)], cwd=ROOT,
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Experiment 014 evaluation flow passed", result.stdout)

    def test_pages_package_includes_participant_instrument(self):
        workflow = (ROOT / ".github/workflows/publish-encyclopedia.yml").read_text(encoding="utf-8")
        self.assertIn("014-conceptual-representation", workflow)
        self.assertIn("experiments/014-conceptual-representation/evaluation/index.html", workflow)
        self.assertTrue((STUDY / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
