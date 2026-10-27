#!/usr/bin/env python3
"""Check schema, declared symbol types, predicate arity, and modal constraints.

This validates internal consistency, NOT the philosophical truth of the claims.
"""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/v0.2.json"
SCHEMA = ROOT / "schemas/v0.2.schema.json"
MODES = {
    "alethic": {"possible", "necessary"},
    "deontic": {"obligatory", "permitted"},
    "epistemic": {"known", "believed"},
    "agential": {"can"},
}


def validate(corpus, schema):
    errors = []
    validator = Draft202012Validator(schema)
    errors.extend(f"schema: {e.message}" for e in validator.iter_errors(corpus))
    if errors:
        return errors

    seen = set()
    signatures = corpus["predicates"]
    sources = corpus["sources"]

    def check(expr, symbols, location):
        op = expr["op"]
        if op == "atom":
            predicate = expr["predicate"]
            signature = signatures.get(predicate)
            if signature is None:
                errors.append(f"{location}: unknown predicate {predicate}")
                return
            roles = expr["roles"]
            if set(roles) != set(signature):
                errors.append(f"{location}: wrong argument roles for {predicate}")
            for role, expected in signature.items():
                if role not in roles:
                    continue
                actual = roles[role]
                if expected.startswith("list:"):
                    required_type = expected[5:]
                    if not isinstance(actual, list):
                        errors.append(f"{location}: {role} must be a list")
                        continue
                    symbols_to_check = actual
                else:
                    required_type = expected
                    symbols_to_check = [actual]
                for symbol in symbols_to_check:
                    if not isinstance(symbol, str) or symbol not in symbols:
                        errors.append(f"{location}: undeclared symbol {symbol!r}")
                    elif required_type != "any" and symbols[symbol] != required_type:
                        errors.append(f"{location}: type mismatch for {symbol!r} as {role}")
        elif op in {"and", "or"}:
            for child in expr["items"]:
                check(child, symbols, location)
        elif op == "not":
            check(expr["item"], symbols, location)
        elif op == "implies":
            check(expr["antecedent"], symbols, location)
            check(expr["consequent"], symbols, location)
        elif op == "exists":
            if symbols.get(expr["entity"]) != "entity":
                errors.append(f"{location}: exists() requires a declared entity")
        elif op == "modal":
            domain = expr["domain"]
            mode = expr["mode"]
            if mode not in MODES[domain]:
                errors.append(f"{location}: invalid {domain}/{mode} modal combination")
            if domain == "agential":
                if symbols.get(expr.get("agent")) != "entity":
                    errors.append(f"{location}: agential modality requires an entity agent")
            elif expr.get("agent"):
                errors.append(f"{location}: agent given for non-agential modality")
            check(expr["item"], symbols, location)

    for claim in corpus["claims"]:
        name = claim["id"]
        if name in seen:
            errors.append(f"duplicate claim id {name}")
        seen.add(name)
        check(claim["expression"], claim["symbols"], name)
        for sid in claim["evidence"]["sources"]:
            if sid not in sources:
                errors.append(f"{name}: unresolved source {sid}")
        if claim["evidence"]["kind"] == "source_paraphrase" and not claim["evidence"]["sources"]:
            errors.append(f"{name}: unattributed source paraphrase")
    return errors


def main():
    corpus = json.loads(CORPUS.read_text())
    schema = json.loads(SCHEMA.read_text())
    errors = validate(corpus, schema)
    if errors:
        print("FAILED:\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(corpus['claims'])} propositions, {len(corpus['predicates'])} predicates; schema, types, sources and modalities checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
