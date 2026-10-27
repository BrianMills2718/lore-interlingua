"""Contracts for Bailey's seven-ray scene (no visual comprehension claim)."""
import json
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

class BaileySceneContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scene=json.loads((HERE/'scene.json').read_text())
        cls.claims={v['id'] for v in json.loads((ROOT/'data/v0.2.json').read_text())['claims']}

    def test_claims_link_to_existing_bailey_corpus(self):
        self.assertEqual(set(self.scene['semantic_references']), {'B01','B02','B03'})
        self.assertTrue(set(self.scene['semantic_references']).issubset(self.claims))

    def test_seven_rays_three_and_four(self):
        rays=self.scene['rays']
        self.assertEqual([r['number'] for r in rays], list(range(1,8)))
        self.assertEqual([r['group'] for r in rays], ['aspect']*3+['attribute']*4)
        self.assertEqual(len({r['texture'] for r in rays}),7)

    def test_guarded_scene_events(self):
        refs=set(self.scene['semantic_references'])
        for e in self.scene['events']:
            self.assertIn(e['claim'],refs)
            self.assertLess(e['from'],e['to'])
            self.assertLessEqual(e['to'],self.scene['duration_seconds'])
            self.assertTrue(e['guard'])
            self.assertTrue(e['render_conventions'])

    def test_no_material_equivalence_assumed(self):
        self.assertIn('No travelling particles',self.scene['comparison_to_001']['modified'])
        self.assertFalse(self.scene['art_direction']['colors_are_semantic'])
        self.assertFalse(self.scene['art_direction']['motion_is_literal_cosmological_time'])

if __name__=='__main__':unittest.main()
