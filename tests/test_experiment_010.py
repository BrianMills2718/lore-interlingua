"""Traceability and interface checks for mediation study 010 (not physics proof)."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class MediationVisualCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=json.loads((ROOT/'experiments/010-living-intermediary/scene-contract.json').read_text())
        cls.atlas=json.loads((ROOT/'encyclopedia/catalog.json').read_text())
        cls.cases=json.loads((ROOT/'encyclopedia/cases.json').read_text())
        cls.corpus=json.loads((ROOT/'data/v0.2.json').read_text())

    def test_cases_and_concept_are_connected_without_duplicate_ontology(self):
        self.assertEqual(len(self.atlas['concepts']),13)
        mediation=next(x for x in self.atlas['concepts'] if x['id']=='mediation')
        self.assertEqual(mediation['examples'][0]['ref'],'G02')
        self.assertTrue(mediation['visual_candidates'][0]['does_not_assert'])
        case=next(x for x in self.cases['cases'] if x['id']=='gurdjieff-010-living-intermediary')
        self.assertTrue(any(x['id']=='mediation' for x in case['related_concepts']))
        self.assertEqual({x['id'] for x in case['claims']},{'G02'})
        self.assertEqual(case['claims'][0]['statement'],next(x['statement'] for x in self.corpus['claims'] if x['id']=='G02'))
        self.assertEqual(case['source_observation']['status'],'additional passage-specific distinction (not an extra v0.2 predicate)')

    def test_source_and_counterfactual_are_not_conflated(self):
        self.assertEqual(self.contract['source']['corpus_claim_id'],'G02')
        self.assertEqual({x['id'] for x in self.contract['exploratory_conditions']},{'bare','grass','people'})
        bare=next(x for x in self.contract['exploratory_conditions'] if x['id']=='bare')
        self.assertIn('counterfactual',bare['semantic_role'])
        self.assertIn('not a historical timeline',self.contract['temporal_categories']['manipulation'])
        for m in self.contract['visual_correspondences']:
            self.assertTrue(m['meaning'] and m['not_asserted'])

    def test_ui_modes_and_semantic_constraints(self):
        page=(ROOT/'experiments/010-living-intermediary/index.html').read_text()
        for s in ['data-mode="bare"','data-mode="grass"','data-mode="people"',
                  'id="show-other"','id="diagnostics"','id="time"','window.__study010',
                  'illustrative', 'counterfactual', 'state.mode']:
            self.assertIn(s,page)
        self.assertNotIn('espeak',page.lower())
        ui=(ROOT/'encyclopedia/cases-ui.js').read_text()
        self.assertIn('case-picker',ui)
        self.assertIn('c.source_observation',ui)
        self.assertNotIn('innerHTML',ui)

if __name__=='__main__':unittest.main()
