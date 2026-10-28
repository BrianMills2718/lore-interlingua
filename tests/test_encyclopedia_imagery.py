"""Check cumulative film imagery records for consistency, not viewer comprehension."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_encyclopedia_imagery import build

class CumulativeImageryTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.d=json.loads((ROOT/'encyclopedia/imagery.json').read_text(encoding='utf-8'))
    cls.concepts={c['id'] for c in json.loads((ROOT/'encyclopedia/catalog.json').read_text(encoding='utf-8'))['concepts']}
    cls.claims={c['id'] for c in json.loads((ROOT/'data/v0.2.json').read_text(encoding='utf-8'))['claims']}
  def test_work_and_source_links(self):
    self.assertEqual({w['id'] for w in self.d['works']},{'011','012'})
    for w in self.d['works']:
      self.assertTrue((ROOT/'encyclopedia'/w['source']).is_file(),w['source'])
      self.assertTrue((ROOT/'encyclopedia'/w['storyboard']).is_file(),w['storyboard'])
  def test_terms_explain_what_is_not_explained(self):
    for t in self.d['terms']:
      self.assertTrue(t['question'] and t['source_meaning'] and t['explained_now'] and t['missing'])
      self.assertIn(t['source'],self.d['source_documents'])
    self.assertIn('seven',{t['id'] for t in self.d['terms']})
  def test_film_status_nonclaims_and_provenance(self):
    ids=set()
    for m in self.d['motifs']:
      self.assertNotIn(m['id'],ids);ids.add(m['id'])
      self.assertTrue(set(m['source_ref'])<=self.claims)
      self.assertTrue(set(m['ontology'])<=self.concepts)
      self.assertIn(m['film011'],{'present','partial','absent'})
      self.assertIn(m['film012'],{'present','partial','absent'})
      self.assertTrue(m['next'] and m['non_claim'] and m['what_lost'])
    self.assertTrue(any(m['film011']=='present' and m['film012']=='absent' for m in self.d['motifs']))
  def test_generated_js_and_html(self):
    self.assertEqual(build((ROOT/'encyclopedia/imagery.json').read_text(encoding='utf-8')),(ROOT/'encyclopedia/imagery-data.js').read_text(encoding='utf-8'))
    h=(ROOT/'encyclopedia/imagery.html').read_text(encoding='utf-8')
    self.assertIn('imagery-data.js',h);self.assertIn('imagery.js',h)
    self.assertIn('id="film-comparison"',h)
    self.assertNotIn('https://cdn.',h)

if __name__=='__main__':unittest.main()
