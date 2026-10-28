"""Structural consistency checks for the visual-semantic research atlas.

These tests are not proofs of visual comprehension, metaphysical truth,
source-translation fidelity, or the effectiveness of proposed iconography.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_encyclopedia import build

CATALOG = ROOT / 'encyclopedia/catalog.json'


class VisualSemanticEncyclopediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CATALOG.read_text(encoding='utf-8'))
        cls.concepts = cls.data['concepts']
        cls.by_id = {c['id']: c for c in cls.concepts}
        cls.claims = {c['id']: c for c in json.loads(
            (ROOT / 'data/v0.2.json').read_text(encoding='utf-8'))['claims']}
        cls.catholic_entities = {c['id'] for c in json.loads(
            (ROOT / 'research/catholic-world-model/v0.1.json').read_text(encoding='utf-8'))['entities']}

    def test_seed_size_unique_identifiers_and_real_source_links(self):
        self.assertEqual(len(self.concepts), 13)
        self.assertEqual(len(self.concepts), len(self.by_id))
        self.assertEqual(set(self.by_id), {'existence','identity','unity','plurality',
            'part-whole','dependence','causation','process','transformation',
            'time','agency','participation','mediation'})
        self.assertEqual(len({c['id'] for c in self.data['facets']}), len(self.data['facets']))
        facets={f['id'] for f in self.data['facets']}
        for c in self.concepts:
            self.assertTrue(c['label'] and c['definition'])
            self.assertTrue(c['facets'] and set(c['facets']) <= facets)
            self.assertTrue(c['examples'] and c['distinctions'] and c['questions'])
            self.assertTrue(c['visual_candidates'])
            self.assertIn(c['demo_id'], {'dependence','identity','composition','time'})
            self.assertEqual(set(c['position']), {'x','y'})

    def test_navigation_relations_are_typed_and_resolve(self):
        allowed=set(self.data['relation_types'])
        pairs=set()
        for c in self.concepts:
            for edge in c['relations']:
                self.assertIn(edge['type'], allowed)
                self.assertIn(edge['target'], self.by_id)
                self.assertNotEqual(edge['target'], c['id'])
                self.assertTrue(edge['why'])
                key=(c['id'], edge['type'], edge['target'])
                self.assertNotIn(key,pairs)
                pairs.add(key)
        # Every concept should be reachable via editorial links; no isolated glossary islands.
        visited=set(); frontier=['dependence']
        while frontier:
            current=frontier.pop()
            if current in visited: continue
            visited.add(current)
            neighbors={e['target'] for e in self.by_id[current]['relations']}
            neighbors.update(c['id'] for c in self.concepts for e in c['relations'] if e['target']==current)
            frontier.extend(neighbors-visited)
        self.assertEqual(visited,set(self.by_id))

    def test_every_example_is_an_existing_scoped_reference(self):
        for c in self.concepts:
            for ex in c['examples']:
                self.assertIn(ex['source'],self.data['sources'])
                self.assertTrue(ex['relevance'] and ex['statement'] and ex['scope'])
                if ex['source']=='interlingua-v0.2':
                    original=self.claims[ex['ref']]
                    self.assertEqual(ex['statement'],original['statement'])
                    self.assertEqual(ex['scope'],original['scope'])
                elif ex['source']=='catholic-world-model-v0.1':
                    self.assertIn(ex['ref'],self.catholic_entities)
                    self.assertEqual(ex['scope'],'catholicism')

    def test_visual_hypotheses_have_explicit_nonclaims(self):
        candidate_ids=set()
        for c in self.concepts:
            for candidate in c['visual_candidates']:
                self.assertNotIn(candidate['id'],candidate_ids)
                candidate_ids.add(candidate['id'])
                self.assertEqual(candidate['status'],'hypothesis')
                self.assertTrue(candidate['mapping'] and candidate['does_not_assert'])
                self.assertTrue(candidate['primitives'])
        self.assertGreater(len(candidate_ids),12)

    def test_offline_generated_catalog_matches_canonical_json(self):
        expected=build(CATALOG.read_text(encoding='utf-8'))
        actual=(ROOT/'encyclopedia/catalog.js').read_text(encoding='utf-8')
        self.assertEqual(actual,expected,
            'Generated catalog.js out of sync: run python scripts/build_encyclopedia.py')

    def test_offline_page_uses_local_code_only(self):
        page=(ROOT/'encyclopedia/index.html').read_text(encoding='utf-8')
        for src in ['styles.css','catalog.js','app.js','cases.js','cases-ui.js']:
            self.assertIn(src,page)
        self.assertNotIn('https://cdn.',page)
        self.assertIn('id="demo"',page)
        self.assertIn('id="graph"',page)


if __name__ == '__main__':
    unittest.main()
