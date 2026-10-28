#!/usr/bin/env python3
"""Package source-linked case records for the dependency-free encyclopedia.

This does not make an ontology assertion or generate a film from semantics.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'encyclopedia/cases.json'
TARGET = ROOT / 'encyclopedia/cases.js'


def build(raw):
    data = json.loads(raw)
    return ('// Generated from cases.json; do not edit by hand.\n'
            'window.LORE_CASES = '
            + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true', help='Fail when the browser copy is stale')
    args = p.parse_args()
    expected = build(SOURCE.read_text(encoding='utf8'))
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding='utf8') != expected:
            p.error('cases.js stale: run python scripts/build_encyclopedia_cases.py')
        print('PASS: cases.js matches cases.json')
    else:
        TARGET.write_text(expected, encoding='utf8')
        print(f'Wrote {TARGET.relative_to(ROOT)}')

if __name__ == '__main__':
    main()
