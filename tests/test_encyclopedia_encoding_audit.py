"""Integrity checks for the Experiment 009 semantic-encoding research exercise.

These checks compare sources/implementation/links. Not viewer comprehension or
proof that radiations have the illustrated physical properties.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_encyclopedia_encoding_audit import build

FILE=ROOT/'encyclopedia/studies/009-encoding-audit.json'

class EncodingAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(FILE.read_text(encoding='utf8'))
        cls.cases=json.loads((ROOT/'encyclopedia/cases.json').read_text(encoding='utf8'))
        cls.corpus=json.loads((ROOT/'data/v0.2.json').read_text(encoding='utf8'))

    def test_case_and_existing_claim_references(self):
        ids={x['id'] for x in self.cases['cases']}
        self.assertIn(self.data['case_id'],ids)
        claims={x['id']:x['statement'] for x in self.corpus['claims']}
        self.assertEqual([x['id'] for x in self.data['claims']],['G02','G03','G04'])
        for x in self.data['claims']:
            self.assertEqual(x['statement'],claims[x['id']])
        self.assertIn('not depicted',self.data['claims'][2]['status'])

    def test_three_encodings_are_declared_and_original_scene_agrees(self):
        channels=self.data['encoding']['outgoing']['channels']
        self.assertEqual([c['id'] for c in channels],['moon','sun','planets'])
        self.assertEqual([c['shape'] for c in channels],['dot','square','ring'])
        self.assertEqual(len(set(x['color'] for x in channels)),3)
        self.assertEqual(len(set(x['rate'] for x in channels)),3)
        scene=(ROOT/'experiments/009-cosmic-membrane/index.html').read_text(encoding='utf8')
        for channel in channels:
            self.assertIn(channel['color'],scene)
            self.assertIn('rate:'+str(channel['rate']).lstrip('0'),scene)

    def test_mode_interventions_do_not_mutate_lore_claims(self):
        self.assertEqual({x['id'] for x in self.data['operations']},{'original','uniform','permuted'})
        for x in self.data['operations']:
            self.assertIn('G03',x['preserves'])
            self.assertTrue(x['changes'] and x['question'])
        self.assertTrue(any('G04' in x['conclusion'] for x in self.data['findings']))
        for x in self.data['findings']:
            self.assertTrue(x['basis'] and x['limit'] and x['conclusion'])

    def test_offline_page_and_enyclopedia_link(self):
        case=next(x for x in self.cases['cases'] if x['id']==self.data['case_id'])
        self.assertEqual(case['artifact']['encoding_audit'],'studies/009-encoding-audit.html')
        for fn in ['009-encoding-audit.html','009-encoding-audit-data.js','009-encoding-lab.js']:
            self.assertTrue((ROOT/'encyclopedia/studies'/fn).is_file())
        page=(ROOT/'encyclopedia/studies/009-encoding-audit.html').read_text(encoding='utf8')
        for key in ['mode-original','mode-uniform','mode-permuted','same-rates','show-g02','comparison']:
            self.assertIn(f'id="{key}"',page)
        ui=(ROOT/'encyclopedia/cases-ui.js').read_text(encoding='utf8')
        self.assertIn('c.artifact.encoding_audit',ui)
        self.assertNotIn('innerHTML', (ROOT/'encyclopedia/studies/009-encoding-lab.js').read_text(encoding='utf8'))

    def test_offline_generated_mirror(self):
        self.assertEqual(build(FILE.read_text(encoding='utf8')),
                         (ROOT/'encyclopedia/studies/009-encoding-audit-data.js').read_text(encoding='utf8'))

if __name__=='__main__':unittest.main()
