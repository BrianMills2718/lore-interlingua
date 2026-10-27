"""Regression tests for the semantic corpus validator."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import validate  # noqa: E402


class CorpusValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "data/v0.2.json").read_text())
        cls.schema = json.loads((ROOT / "schemas/v0.2.schema.json").read_text())

    def test_current_corpus(self):
        self.assertEqual(validate(self.data, self.schema), [])

    def test_invalid_modal(self):
        data = copy.deepcopy(self.data)
        # Put illegal deontic necessity into a well-formed expression.
        claim = data["claims"][0]
        claim["expression"] = {
            "op": "modal", "domain": "deontic", "mode": "necessary",
            "item": {"op": "exists", "entity": next(k for k, t in claim["symbols"].items() if t == "entity")}
        }
        self.assertTrue(any("modal combination" in e for e in validate(data, self.schema)))

    def test_undeclared_symbol(self):
        data = copy.deepcopy(self.data)
        data["claims"][0]["expression"] = {
            "op": "exists", "entity": "never_declared"
        }
        self.assertTrue(any("requires a declared entity" in e for e in validate(data, self.schema)))

    def test_duplicate_id(self):
        data = copy.deepcopy(self.data)
        data["claims"][1]["id"] = data["claims"][0]["id"]
        self.assertTrue(any("duplicate claim id" in e for e in validate(data, self.schema)))

    def test_missing_source(self):
        data = copy.deepcopy(self.data)
        data["claims"][0]["evidence"]["sources"].append("nonexistent-source")
        self.assertTrue(any("unresolved source" in e for e in validate(data, self.schema)))


if __name__ == "__main__":
    unittest.main()
