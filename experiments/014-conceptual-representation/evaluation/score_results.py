"""Score Experiment 014's *anonymous, formative* responses offline.

Usage:
    python experiments/014-conceptual-representation/evaluation/score_results.py response.json [response2.json ...]

Scoring is limited to the predeclared multiple-choice items; open responses need
manual coding. Do not commit identifiable participant responses into this public repo.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

SCHEMA = "lore-interlingua-experiment-014-formative-v1"
CONDITIONS = {"follow-influence", "trace-from-earth"}
KEYS = {
    "comprehension": {
        "C1": "planet_life_earth",
        "C2": "mediated_relation_unavailable",
        "C3": "no_physical_mechanism",
    },
    "transfer": {
        "T1": "dashed_nara_ivo",
        "T2": "solid_ivo_selen",
        "T3": "ivo",
        "T4": "no_universal_mechanism",
    },
}
OPTIONS = {
    "C1": {"planet_life_earth", "planet_earth_life", "life_creates_planets", "unsure"},
    "C2": {
        "all_natural_forces_stop", "direct_route_preserved",
        "mediated_relation_unavailable", "historical_earth", "unsure"
    },
    "C3": {"exact_particles", "measured_rates", "no_physical_mechanism", "unsure"},
    "T1": {"dashed_nara_ivo", "solid_ivo_selen", "both", "unsure"},
    "T2": {"dashed_nara_ivo", "solid_ivo_selen", "both", "unsure"},
    "T3": {"nara", "ivo", "selen", "unsure"},
    "T4": {"exact_translation", "physical_conservation", "no_universal_mechanism", "unsure"},
}

def score_record(record):
    """Validate a response shape and return diagnostics without its written answers."""
    if not isinstance(record, dict) or record.get("schema") != SCHEMA:
        raise ValueError("unexpected response schema")
    if record.get("condition") not in CONDITIONS:
        raise ValueError("unknown or missing presentation condition")
    if record.get("exposure_self_reported_complete") is not True:
        raise ValueError("study exposure not confirmed (self-report)")
    for section in KEYS:
        if not isinstance(record.get(section), dict):
            raise ValueError("missing response section: " + section)
    for section, field in [("comprehension", "C4"), ("transfer", "T5")]:
        if not isinstance(record[section].get(field), str):
            raise ValueError("invalid open response field: " + field)
        if len(record[section][field]) > 900:
            raise ValueError("open response exceeds 900 characters: " + field)

    scores = {}
    for section, key in KEYS.items():
        answers = record[section]
        correct, missing, unsure = 0, 0, 0
        per_item = {}
        for item, expected in key.items():
            actual = answers.get(item)
            if actual is not None and actual not in OPTIONS[item]:
                raise ValueError("unrecognized answer code " + item)
            if actual is None:
                missing += 1
                per_item[item] = "missing"
            elif actual == "unsure":
                unsure += 1
                per_item[item] = "unsure"
            else:
                is_correct = actual == expected
                correct += int(is_correct)
                per_item[item] = "correct" if is_correct else "incorrect"
        scores[section] = {
            "correct": correct,
            "maximum": len(key),
            "answered": len(key) - missing,
            "missing": missing,
            "unsure": unsure,
            "items": per_item,
        }

    c = record["comprehension"]
    t = record["transfer"]
    flags = [
        code for code, triggered in {
            "direct-bypass": c.get("C1") == "planet_earth_life" or c.get("C2") == "direct_route_preserved",
            "source-reversal": c.get("C1") == "life_creates_planets",
            "literal-particles": c.get("C3") == "exact_particles",
            "quantified-physics": c.get("C3") == "measured_rates",
            "universal-no-forces": c.get("C2") == "all_natural_forces_stop",
            "notation-sign-reversal": t.get("T1") == "solid_ivo_selen" or t.get("T2") == "dashed_nara_ivo",
        }.items() if triggered
    ]
    return {
        "condition": record["condition"],
        "comprehension": scores["comprehension"],
        "transfer": scores["transfer"],
        "diagnostic_response_patterns": flags,
        "open_reconstruction_requires_manual_coding": bool(c["C4"].strip()),
        "open_misreading_requires_review": bool(t["T5"].strip()),
    }

def summarize(results):
    """Descriptive counts only: no inferential claims from a small formative sample."""
    groups = {}
    for item in results:
        groups.setdefault(item["condition"], []).append(item)
    output = {}
    for condition, rows in sorted(groups.items()):
        output[condition] = {
            "n": len(rows),
            "comprehension_correct_total": sum(r["comprehension"]["correct"] for r in rows),
            "comprehension_items_possible": len(rows) * len(KEYS["comprehension"]),
            "transfer_correct_total": sum(r["transfer"]["correct"] for r in rows),
            "transfer_items_possible": len(rows) * len(KEYS["transfer"]),
            "missed_item_count": sum(
                r[section]["missing"] for r in rows for section in KEYS
            ),
            "diagnostic_response_pattern_counts": dict(Counter(
                code for r in rows for code in r["diagnostic_response_patterns"]
            )),
        }
    return output

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path, nargs="+",
                        help="Anonymous response JSON files from the browser form")
    args = parser.parse_args()
    results = []
    for file in args.responses:
        record = json.loads(file.read_text(encoding="utf-8"))
        results.append(score_record(record))
    print(json.dumps({
        "instrument": SCHEMA,
        "n": len(results),
        "individual_scored_results_without_raw_text": results,
        "descriptive_group_counts": summarize(results),
        "caution": (
            "Synthetic/demo files are not human data. Closed-item results do not score "
            "open responses. No inference of teaching efficacy, source truth, or "
            "validated universal notation is warranted."
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
