"""Structural tests only: they do not validate viewer comprehension or doctrine."""
from pathlib import Path
import json,re, unittest
HERE=Path(__file__).parent
class Ray012(unittest.TestCase):
    def test_contract_has_source_law_sequence(self):
        d=json.loads((HERE/'scene-contract.json').read_text())
        self.assertEqual([w['orders_of_laws'] for w in d['worlds']],[1,3,6,12,24,48,96])
        self.assertEqual(len({w['id'] for w in d['worlds']}),7)
        self.assertTrue(d['source']['text_url'].startswith('https://'))
        self.assertTrue(all(op['why'] and op['does_not_assert'] for op in d['semantic_operations']))
    def test_offline_video_source_present(self):
        s=(HERE/'film.html').read_text()
        self.assertIn('window.renderAt=renderAt',s)
        self.assertIn('window.renderDuration=T',s)
        self.assertIn('T=124',s)
        self.assertIn('data:image/jpeg;base64,',s)
        self.assertNotIn('https://cdn.',s)
        self.assertIn('orders of laws',s.lower())
    def test_exported_captions_cover_film(self):
        s=(HERE/'captions.srt').read_text()
        self.assertIn('00:00:00,000 -->',s)
        self.assertIn('00:02:04,000',s)
    def test_source_statement_is_scoped(self):
        s=(HERE/'README.md').read_text()
        self.assertIn('Ouspensky',s)
        self.assertIn('not modern astrophysics',s)
        self.assertIn('visual-language hypotheses',s)
if __name__=='__main__':unittest.main()
