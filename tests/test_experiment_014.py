"""Experiment 014: structure and explanatory-order invariants, not viewer comprehension."""
import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "014-conceptual-representation"


def load(name):
    return json.loads((EXP / name).read_text(encoding="utf-8"))


def contract_errors(model, notation, presentations):
    errors = []
    ids = [c["id"] for c in model["concepts"]]
    role_by_id = {c["id"]: c["role"] for c in model["concepts"]}
    claims = {c["id"] for c in model["claims"]}
    sources = {s["id"] for s in model["sources"]}
    relations = {r["id"]: r for r in model["relationships"]}
    if len(ids) != len(set(ids)) or len(relations) != len(model["relationships"]):
        errors.append("duplicate concept or relationship ID")
    if not all(set(c["source_ids"]) <= sources for c in model["claims"]):
        errors.append("unresolved claim source")
    for relation in model["relationships"]:
        if relation["source"] not in ids or relation["target"] not in ids:
            errors.append("unresolved relationship endpoint")
        if not set(relation["claim_ids"]) <= claims:
            errors.append("unresolved relationship claim")
        if not set(relation.get("requires_present", [])) <= set(ids):
            errors.append("unresolved requirement")
    expected_roles = {"planetary-world": "source", "organic-life": "intermediary", "earth": "recipient"}
    if role_by_id != expected_roles:
        errors.append("unexpected participant roles")
    expected_relations = {
        "reception": ("receives", "planetary-world", "organic-life"),
        "mediation": ("mediates-to", "organic-life", "earth"),
    }
    if set(relations) != set(expected_relations):
        errors.append("missing or unexpected relationship")
    for rid, expected in expected_relations.items():
        r = relations.get(rid)
        if r is not None and (r["type"], r["source"], r["target"]) != expected:
            errors.append("relation changed: " + rid)
    if "organic-life" not in relations.get("mediation", {}).get("requires_present", []):
        errors.append("mediation lost its intermediary requirement")

    mappings = notation["mappings"]
    keys = [(m["binds"], m["value"]) for m in mappings]
    expected_keys = {
        ("concept_role", role) for role in expected_roles.values()
    } | {("relationship_type", typ) for typ, _, _ in expected_relations.values()}
    if set(keys) != expected_keys or len(keys) != len(set(keys)):
        errors.append("notation does not cover distinct roles and relationships once each")
    if any(not m["intended_meaning"] or not m["not_asserted"] for m in mappings):
        errors.append("notation meaning or limitations missing")
    if notation["model_ref"] != "concept-model.json":
        errors.append("notation references another model")

    variants = presentations["variants"]
    if presentations["model_ref"] != "concept-model.json" or presentations["notation_ref"] != "notation.json":
        errors.append("presentation references another model/notation")
    if len(variants) != 2 or len({v["id"] for v in variants}) != 2:
        errors.append("expected two distinct traversals")
    orders = []
    revealed_orders = []
    for variant in variants:
        steps = variant["steps"]
        if [s["order"] for s in steps] != list(range(1, len(steps) + 1)):
            errors.append("nonlinear or duplicate beat order")
        if not steps:
            errors.append("empty traversal")
            continue
        for step in steps:
            if step["focus"] not in ids:
                errors.append("unresolved focus")
            if set(step["visible_concepts"]) != set(ids):
                errors.append("unstable or missing concept identity")
            if not set(step["visible_relationships"]) <= set(relations):
                errors.append("unresolved visible relationship")
            if any(k in step for k in ("claims", "relationships", "domain_time")):
                errors.append("traversal overrides underlying meaning")
        if set(steps[-1]["visible_relationships"]) != set(relations):
            errors.append("traversal did not reveal complete relation structure")
        if any(not set(prev["visible_relationships"]) <= set(nxt["visible_relationships"])
               for prev, nxt in zip(steps, steps[1:])):
            errors.append("relationship reveal is not cumulative")
        orders.append(tuple(s["focus"] for s in steps))
        revealed_orders.append(tuple(
            tuple(s["visible_relationships"]) for s in steps
        ))
    if len(orders) == 2 and (orders[0] == orders[1] or revealed_orders[0] == revealed_orders[1]):
        errors.append("explanatory orders did not differ")
    return errors


class Experiment014ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load("concept-model.json")
        cls.notation = load("notation.json")
        cls.presentations = load("presentations.json")

    def test_contract(self):
        self.assertEqual(contract_errors(self.model, self.notation, self.presentations), [])

    def test_corrupted_relationship_fails(self):
        changed = copy.deepcopy(self.model)
        changed["relationships"][1]["source"] = "planetary-world"
        self.assertTrue(any("relation changed" in e
                            for e in contract_errors(changed, self.notation, self.presentations)))

    def test_undeclared_reveal_fails(self):
        changed = copy.deepcopy(self.presentations)
        changed["variants"][0]["steps"][0]["visible_relationships"] = ["invented-force"]
        self.assertTrue(any("unresolved visible relationship" in e
                            for e in contract_errors(self.model, self.notation, changed)))

    def test_incomplete_second_traversal_fails(self):
        changed = copy.deepcopy(self.presentations)
        changed["variants"][1]["steps"][-1]["visible_relationships"] = ["mediation"]
        self.assertTrue(any("did not reveal complete" in e
                            for e in contract_errors(self.model, self.notation, changed)))


if __name__ == "__main__":
    unittest.main()
