"""Source-linked visual case and semantic-parsimony integrity checks.

These are checks of editorial traceability, not of the truth of Gurdjieff's
account, its physical interpretation or viewer understanding.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_encyclopedia_cases import build

DATA=ROOT/'encyclopedia/cases.json'

class AppliedCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DATA.read_text(encoding='utf8'))
        cls.atlas=json.loads((ROOT/'encyclopedia/catalog.json').read_text(encoding='utf8'))
        cls.by_id={c['id']:c for c in cls.atlas['concepts']}

    def test_unique_cases_and_real_source_claims(self):
        cases=self.data['cases']
        self.assertGreaterEqual(len(cases),1)
        self.assertEqual(len(cases),len({x['id'] for x in cases}))
        for c in cases:
            self.assertTrue(c['scope'] and c['tradition'])
            self.assertTrue(c['source_documents'])
            self.assertTrue(all(x['url'].startswith('https://') for x in c['source_documents']))
            self.assertEqual(len(c['claims']),len({x['id'] for x in c['claims']}))
            for claim in c['claims']:
                self.assertIn(claim['id'],{'G02','G03','G04'})
                self.assertTrue(claim['reading'] and claim['not_shown'])
                self.assertIn(claim['status'],{'depicted','context only — not depicted'})
        self.assertIn('not depicted',next(x for x in cases[0]['claims'] if x['id']=='G04')['status'])

    def test_claim_statements_are_exact_corpus_paraphrases(self):
        corpus_path=ROOT/'data/v0.2.json'
        if not corpus_path.exists():
            self.skipTest('Local isolated viewer checkout has no v0.2 corpus; full repository CI performs this check')
        claims={x['id']:x for x in json.loads(corpus_path.read_text(encoding='utf8'))['claims']}
        for case in self.data['cases']:
            for claim in case['claims']:
                self.assertIn(claim['id'],claims)
                self.assertEqual(claim['statement'],claims[claim['id']]['statement'])
                self.assertEqual(claims[claim['id']]['scope'],case['tradition'])

    def test_concept_links_resolve_without_duplicate_ontology(self):
        for case in self.data['cases']:
            for rel in case['related_concepts']:
                self.assertIn(rel['id'],self.by_id)
                self.assertIn(rel['claim_id'],{x['id'] for x in case['claims']})
                self.assertTrue(rel['role'] and rel['why'])
        self.assertEqual(len(self.atlas['concepts']),13)
        self.assertNotIn('concepts',self.data)

    def test_each_major_mark_has_a_role_and_nonclaim(self):
        for c in self.data['cases']:
            known={x['id'] for x in c['claims']}
            self.assertEqual(len(c['marks']),len({x['id'] for x in c['marks']}))
            for mark in c['marks']:
                for k in ['label','symbol','color','kind','referent','mapping','why','does_not_assert','visibility']:
                    self.assertTrue(mark[k],(mark['id'],k))
                self.assertTrue(set(mark['claim_ids'])<=known)
                if not mark['claim_ids']:
                    self.assertEqual(mark['kind'],'ornament')
                    self.assertEqual(mark['referent'].split()[0],'none')
                # The illustrated lunar stream is NOT proof of the stronger maintenance claim.
                self.assertNotIn('G04',mark['claim_ids'])
            expected={'G02','G03'} if c['id'].startswith('gurdjieff-009') else {'G02'}
            self.assertEqual({x['id'] for x in c['claims'] if x['status']=='depicted'},expected)

    def test_interactive_scene_and_local_links(self):
        for c in self.data['cases']:
            target=(ROOT/'encyclopedia'/c['artifact']['html']).resolve()
            self.assertTrue(str(target).startswith(str(ROOT)),target)
            self.assertTrue(target.exists(),target)
            # Documentation stays canonical in the main repository; the offline
            # study bundle does not duplicate narrative/source review files.
            for key in ['primary_treatment','scene_contract','narration_audit','parsimony_audit']:
                experiment='009-cosmic-membrane' if '009' in c['id'] else '010-living-intermediary'
                self.assertTrue(c['artifact'][key].startswith(
                    'https://github.com/BrianMills2718/lore-interlingua/blob/main/experiments/'+experiment+'/'))
        page=(ROOT/'encyclopedia/index.html').read_text(encoding='utf8')
        for target in ['cases.js','cases-ui.js','id="case-study"','id="case-scene"','id="case-marks"']:
            self.assertIn(target,page)
        ui=(ROOT/'encyclopedia/cases-ui.js').read_text(encoding='utf8')
        self.assertIn('No marks in this scene independently depict this stronger claim.',ui)
        self.assertIn('case-picker',ui)
        self.assertNotIn('innerHTML',ui)

    def test_generated_offline_mirror(self):
        self.assertEqual((ROOT/'encyclopedia/cases.js').read_text(encoding='utf8'),
                         build(DATA.read_text(encoding='utf8')))

if __name__=='__main__':
    unittest.main()
