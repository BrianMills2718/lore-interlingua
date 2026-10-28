from pathlib import Path
import json,re,unittest
ROOT=Path(__file__).resolve().parent
class Film013(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ROOT/'scene-contract.json').read_text());self.h=(ROOT/'film.html').read_text();self.cues=json.loads((ROOT/'cues.json').read_text())
 def test_scope_and_count(self):
  self.assertEqual(self.c['production']['duration_seconds'],176)
  self.assertEqual(self.c['production']['fps'],24)
  self.assertEqual([x['ref'] for x in self.c['claims']],['G01','G02','G03','G04'])
  self.assertEqual([x['role'] for x in self.c['claims']],['depicted']*3+['context-only'])
  self.assertTrue(all(x['semantic'] and x['not_asserted'] for x in self.c['relation_operations']))
 def test_cumulative(self):
  ops={x['id'] for x in self.c['relation_operations']}
  self.assertGreaterEqual(len(ops),9)
  self.assertTrue({'three-forces','octave-interval','organic-life','incoming-influence','inward-mediation','outward-radiation','selected-hierarchy'}.issubset(ops))
  self.assertEqual(self.h.count('window.renderDuration=T;'),1)
  self.assertIn('function livingSurface(',self.h)
  self.assertIn('function outgoingRadiations(',self.h)
  self.assertIn('function sourceGeometry(',self.h)
  self.assertIn('function mediatedResponse(',self.h)
 def test_cues(self):
  self.assertEqual(self.cues[0]['at'],0);self.assertEqual(self.cues[-1]['to'],176.1)
  for a,b in zip(self.cues,self.cues[1:]):self.assertEqual(a['to'],b['at'])
  text=' '.join(x['title']+' '+x['line'] for x in self.cues).lower()
  for concept in ['three','seven','interval','planetary influences','plants','animals','people','sun','moon','radiates','physical nature']:
   self.assertIn(concept,text)
  self.assertEqual(len(re.findall(r'\n\d+\n\d\d:\d\d:\d\d,\d\d\d -->', '\n'+(ROOT/'captions.srt').read_text())),len(self.cues))
if __name__=='__main__':unittest.main()
