"""Experiment 014 workbench: provenance, offline build and storyboard trace tests."""
import json
import shutil
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "014-conceptual-representation"
sys.path.insert(0, str(ROOT / "scripts"))
from build_experiment_014_study import compiled_source  # noqa: E402


def load(name):
    return json.loads((EXP / name).read_text(encoding="utf-8"))


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class Experiment014WorkbenchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load("concept-model.json")
        cls.notation = load("notation.json")
        cls.presentations = load("presentations.json")
        cls.storyboards = load("storyboard-treatments.json")

    def test_generated_offline_bundle_is_current(self):
        bundle = (EXP / "study-data.js").read_text(encoding="utf-8")
        self.assertEqual(bundle, compiled_source())
        prefix = "window.LI_EXPERIMENT_014 = "
        self.assertIn(prefix, bundle)
        payload = json.loads(bundle.split(prefix, 1)[1].removesuffix(";\n"))
        self.assertEqual(payload["model"], self.model)
        self.assertEqual(payload["notation"], self.notation)
        self.assertEqual(payload["presentations"], self.presentations)
        self.assertEqual(payload["storyboards"], self.storyboards)

    def test_storyboards_are_linearizations_not_new_claims(self):
        self.assertEqual(self.storyboards["model_ref"], "concept-model.json")
        self.assertEqual(self.storyboards["presentations_ref"], "presentations.json")
        expected = {v["id"]: v for v in self.presentations["variants"]}
        self.assertEqual({v["id"] for v in self.storyboards["treatments"]}, set(expected))
        all_relations = {r["id"] for r in self.model["relationships"]}
        all_concepts = {c["id"] for c in self.model["concepts"]}
        shot_ids = []
        for treatment in self.storyboards["treatments"]:
            with self.subTest(variant=treatment["id"]):
                steps = expected[treatment["id"]]["steps"]
                self.assertEqual(len(treatment["shots"]), len(steps))
                for shot, step in zip(treatment["shots"], steps):
                    shot_ids.append(shot["id"])
                    self.assertEqual(shot["beat"], step["order"])
                    self.assertEqual(shot["focus"], step["focus"])
                    self.assertIn(shot["focus"], all_concepts)
                    self.assertEqual(shot["relation_ids_visible"], step["visible_relationships"])
                    self.assertTrue(set(shot["relation_ids_visible"]) <= all_relations)
                    self.assertGreater(shot["suggested_seconds"], 0)
                    for key in ("framing", "caption", "narration", "nonclaim"):
                        self.assertTrue(shot[key].strip())
                    self.assertFalse({"claims", "concepts", "relationships", "domain_time"} & set(shot),
                                     "Storyboard beats must not redefine the model.")
        self.assertEqual(len(shot_ids), len(set(shot_ids)))
        self.assertEqual({c["id"] for c in self.model["claims"]}, {"G02"})

    def test_accessible_offline_controls_and_visual_semantics_exist(self):
        html = (EXP / "index.html").read_text(encoding="utf-8")
        parser = Tags()
        parser.feed(html)
        elements = parser.elements
        ids = {attrs["id"] for _, attrs in elements if "id" in attrs}
        modes = {attrs["data-mode"] for tag, attrs in elements if tag == "button" and "data-mode" in attrs}
        focus = {attrs["data-inspect"] for tag, attrs in elements if tag == "button" and "data-inspect" in attrs}
        self.assertEqual(modes, {"overview", "follow-influence", "trace-from-earth"})
        self.assertEqual(focus, {c["id"] for c in self.model["concepts"]})
        self.assertTrue({
            "concept-diagram", "visual-description", "relation-reception", "relation-mediation",
            "focus-name", "focus-facets", "storyboard-list", "notation-list",
            "next-step", "previous-step", "interpretive-limits", "relation-summary",
        } <= ids)
        self.assertIn(("html", {"lang": "en"}), elements)
        scripts = [attrs["src"] for tag, attrs in elements if tag == "script" and "src" in attrs]
        self.assertEqual(scripts, ["study-data.js", "study.js"])
        self.assertIn("aria-live=\"polite\"", html)
        self.assertIn('role="img"', html)
        self.assertIn("Dashed and solid relations", html)
        self.assertIn("not an astronomical mechanism", html.lower())

    def test_pages_assembly_includes_workbench(self):
        workflow = (ROOT / ".github/workflows/publish-encyclopedia.yml").read_text(encoding="utf-8")
        self.assertIn("014-conceptual-representation", workflow)
        self.assertIn("experiments/014-conceptual-representation/index.html", workflow)

    def test_javascript_syntax_and_interactions_without_browser_dependencies(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node unavailable; browser behavior must be tested separately.")
        for name in ("study.js", "study-data.js"):
            result = subprocess.run([node, "--check", str(EXP / name)],
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
        test = ROOT / "tests" / "fixtures" / "experiment014-dom-smoke.cjs"
        result = subprocess.run([node, str(test)], cwd=ROOT,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + "\n" + result.stderr)
        self.assertIn("Experiment 014 mode interactions passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
