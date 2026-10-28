"""Structural and semantic guardrails for the Catholic world-model research fixture.

These tests check transcription/representation integrity. They are NOT theological
proofs, empirical validations of the doctrine, or viewer comprehension studies.
"""
import json
import unittest
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[1] / "research/catholic-world-model/v0.1.json"


class CatholicWorldModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
        cls.entities = {e["id"]: e for e in cls.model["entities"]}
        cls.sources = cls.model["sources"]

    def test_unique_identity_and_valid_source_references(self):
        for section in ("entities", "relations", "processes", "states"):
            entries = self.model[section]
            self.assertEqual(len([e["id"] for e in entries]), len(set(e["id"] for e in entries)))
            for e in entries:
                self.assertTrue(e["source_ids"], (section, e["id"]))
                for sid in e["source_ids"]:
                    self.assertIn(sid, self.sources, (section, e["id"], sid))
        for sid, src in self.sources.items():
            self.assertTrue(src["url"].startswith("https://www.vatican.va/"), sid)

    def test_relations_and_processes_resolve(self):
        for r in self.model["relations"]:
            self.assertIn(r["subject"], self.entities)
            self.assertIn(r["object"], self.entities)
            self.assertIn(r["temporality"], {"eternal", "atemporal", "origin", "ongoing",
                "structural", "historical", "historical_ongoing", "historical_saving",
                "saving_history", "ecclesial", "liturgical", "teleological", "identity",
                "ecclesial_eschatological"})
        for p in self.model["processes"]:
            self.assertTrue(p["guardrail"])
            for eid in p["participant_ids"]:
                self.assertIn(eid, self.entities)

    def test_trinity_person_and_nature_not_conflated(self):
        persons = {e["id"] for e in self.model["entities"] if e["kind"] == "divine_person"}
        self.assertEqual(persons, {"father", "son", "spirit"})
        has_divine_nature = {r["subject"] for r in self.model["relations"]
            if r["predicate"] == "has_nature" and r["object"] == "divine_nature"}
        self.assertEqual(has_divine_nature, persons)
        self.assertEqual(self.entities["mary"]["kind"], "created_person")
        self.assertEqual(self.entities["jesus"]["kind"], "identity_alias")
        self.assertIn(("jesus", "son"), {(r["subject"], r["object"]) for r in self.model["relations"]
            if r["predicate"] == "same_person_as"})

    def test_creation_not_material_transfer_or_coeternal_dualism(self):
        self.assertEqual(self.entities["god"]["kind"], "divine_being")
        self.assertEqual(self.entities["fallen_angels"]["kind"], "created_kind")
        self.assertTrue(any(r["predicate"] == "freely_creates" and
            r["subject"] == "god" and r["object"] == "created_order" for r in self.model["relations"]))
        self.assertTrue(any(r["predicate"] == "sustains_in_being" and
            r["subject"] == "god" and r["object"] == "created_order" for r in self.model["relations"]))
        self.assertTrue(any("not a transfer of divine substance" in r["meaning"] for r in self.model["relations"]))

    def test_materiality_and_eschatology_distinctions(self):
        states = {s["id"] for s in self.model["states"]}
        self.assertTrue({"purgatory", "heaven", "hell", "bodily_resurrection"} <= states)
        self.assertTrue(any(r["predicate"] == "directed_toward" and
            r["object"] == "new_creation" for r in self.model["relations"]))


if __name__ == "__main__":
    unittest.main()
