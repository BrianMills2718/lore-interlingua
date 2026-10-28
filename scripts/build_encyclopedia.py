#!/usr/bin/env python3
"""Rebuild/check the encyclopedia's offline catalog from canonical JSON.

This is a data packaging utility, NOT ontology inference or scene generation.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / 'encyclopedia/catalog.json'
OUT = ROOT / 'encyclopedia/catalog.js'


def build(raw):
    data = json.loads(raw)
    return ('// Generated from catalog.json; do not edit directly.\n'
            'window.LORE_ENCYCLOPEDIA = '
            + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Exit nonzero if generated data is stale')
    args = parser.parse_args()
    expected = build(IN.read_text(encoding='utf-8'))
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding='utf-8') != expected:
            parser.error('catalog.js is stale; run python scripts/build_encyclopedia.py')
        print('PASS: offline catalog.js matches catalog.json')
    else:
        OUT.write_text(expected, encoding='utf-8')
        print(f'Wrote {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()