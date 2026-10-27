"""Static checks of the experiment manifest and integration with corpus v0.2."""
from pathlib import Path
import json
import unittest

BASE = Path(__file__).resolve().parent
PROJECT = BASE.parents[1]

class SceneContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scene = json.loads((BASE/'scene.json').read_text())
        cls.corpus = json.loads((PROJECT/'data'/'v0.2.json').read_text())

    def test_corpus_claim_links(self):
        ids = {claim['id'] for claim in self.corpus['claims']}
        for ref in self.scene['semantic_references']:
            self.assertIn(ref, ids)

    def test_actions_reference_current_claims(self):
        valid = set(self.scene['semantic_references'])
        for e in self.scene['events']:
            self.assertLess(e['from'], e['to'])
            self.assertLessEqual(e['to'], self.scene['duration_seconds']+1)
            self.assertTrue(set(e['claim'].split('/')).issubset(valid))
            self.assertTrue(e['render_conventions'])
            self.assertTrue(e['guard'])

    def test_explicit_art_direction_and_attribution(self):
        self.assertFalse(self.scene['art_direction']['colors_are_semantic'])
        self.assertIn('interpretation', self.scene['attribution'].lower())

if __name__ == '__main__':
    unittest.main()
