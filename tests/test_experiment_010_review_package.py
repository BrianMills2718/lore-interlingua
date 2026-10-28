"""Verify the exact offline review artifacts committed for Experiment 010.

Checks archive integrity and fixed snapshot identity, not doctrinal accuracy,
visual comprehension or validity of metaphysical mechanisms.
"""
import hashlib
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "downloads/Lore_Visual_Semantic_Encyclopedia_v0_4_Living_Intermediary.zip"
COMPARISON = ROOT / "experiments/010-living-intermediary/review-comparison.jpg"


class Experiment010ReviewArtifactTests(unittest.TestCase):
    def test_exact_review_files(self):
        expected = {
            ARCHIVE: "2784123ce4c38eb9edbd6c7643856e855a151627e36053069c46d8db68a9c491",
            COMPARISON: "deaf48bf13bee1fcc2a7f140373f125b5bc801592bfa2a5689ed0c0fdf4cd4ab",
        }
        for file, digest in expected.items():
            self.assertTrue(file.is_file(), str(file))
            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), digest)

    def test_archive_integrity_and_offline_entrypoints(self):
        with zipfile.ZipFile(ARCHIVE) as z:
            self.assertIsNone(z.testzip())
            names = set(z.namelist())
            for path in (
                "index.html",
                "encyclopedia/index.html",
                "encyclopedia/catalog.json",
                "encyclopedia/catalog.js",
                "encyclopedia/cases.json",
                "experiments/010-living-intermediary/index.html",
                "experiments/010-living-intermediary/scene-contract.json",
                "study010-comparison.jpg",
            ):
                self.assertIn(path, names)
            self.assertIn("encyclopedia/index.html", z.read("index.html").decode("utf-8"))
            self.assertEqual(z.read("study010-comparison.jpg"), COMPARISON.read_bytes())


if __name__ == "__main__":
    unittest.main()
