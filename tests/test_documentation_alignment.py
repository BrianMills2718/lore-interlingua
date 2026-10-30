"""Guard a few high-value documentation facts against recurring drift.

These are documentation consistency checks, not source or comprehension tests.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class DocumentationAlignmentTests(unittest.TestCase):
    def test_registry_has_unique_completed_experiment_rows(self):
        registry = read("docs/EXPERIMENT_REGISTRY.md")
        rows = re.findall(r"^\|\s*(\d{3})(?:–\d{3})?\s*\|", registry, re.MULTILINE)
        self.assertEqual(len(rows), len(set(rows)))
        for item in ("000", "009", "010", "011", "012", "013"):
            self.assertIn(item, rows)
        self.assertNotIn(r"\n\n| 009 |", registry)

    def test_current_encyclopedia_files_and_offline_snapshot_exist(self):
        for name in (
            "encyclopedia/index.html",
            "encyclopedia/imagery.html",
            "encyclopedia/README.md",
            "downloads/Lore_Visual_Semantic_Encyclopedia_v0_4_Living_Intermediary.zip",
        ):
            with self.subTest(path=name):
                self.assertTrue((ROOT / name).is_file())

    def test_current_encyclopedia_ui_describes_completed_film_013(self):
        html = read("encyclopedia/index.html")
        self.assertIn("Films 011, 012 and 013", html)
        docs = read("encyclopedia/README.md")
        self.assertIn("Films 011, 012 and 013", docs)
        self.assertNotIn("proposed integrated Film 013 has already been produced", docs)

    def test_current_package_and_browser_qa_are_discoverable(self):
        workflow = read(".github/workflows/publish-encyclopedia.yml")
        self.assertIn("actions/upload-artifact@v4", workflow)
        self.assertIn("lore-interlingua-current-offline-atlas", workflow)
        self.assertIn("retention-days: 30", workflow)
        browser_workflow = read(".github/workflows/qa-atlas-browser.yml")
        self.assertIn("qa_browser_atlas.py", browser_workflow)
        self.assertIn("lore-interlingua-browser-qa", browser_workflow)
        self.assertIn("playwright", read("scripts/qa_browser_atlas.py"))
        docs = read("docs/ENCYCLOPEDIA_HOSTING.md")
        self.assertIn("lore-interlingua-current-offline-atlas", docs)

    def test_current_navigation_links_to_notation_and_snapshots(self):
        root = read("README.md")
        self.assertIn("docs/NOTATION_AND_COMPREHENSION.md", root)
        self.assertIn("offline ZIP", root)
        self.assertIn("Experiment 014", root)
        self.assertIn("is merged into `main`", root)
        self.assertIn("v0.4 package", read("downloads/README.md"))


if __name__ == "__main__":
    unittest.main()
