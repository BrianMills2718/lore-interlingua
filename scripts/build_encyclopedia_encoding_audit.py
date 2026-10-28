#!/usr/bin/env python3
"""Rebuild/check the offline data mirror for the Experiment 009 encoding audit.

Data packaging only. Does not infer ontology or validate metaphysical truth.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'encyclopedia/studies/009-encoding-audit.json'
TARGET = ROOT / 'encyclopedia/studies/009-encoding-audit-data.js'


def build(raw):
    data = json.loads(raw)
    return ('// Generated from 009-encoding-audit.json; do not edit manually.\n'
            'window.LORE_ENCODING_AUDIT = '
            + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    expected=build(SOURCE.read_text(encoding='utf8'))
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding='utf8')!=expected:
            parser.error('audit data mirror stale; run python scripts/build_encyclopedia_encoding_audit.py')
        print('PASS: encoding audit data mirror matches canonical JSON')
    else:
        TARGET.write_text(expected,encoding='utf8')
        print('Wrote',TARGET.relative_to(ROOT))

if __name__ == '__main__':main()
