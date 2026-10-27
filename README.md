# Cosmology Interlingua

A research and prototyping project for translating metaphysical, esoteric, and philosophical systems into a **common conceptual interlingua**, and eventually into a **compositional visual language** for animation.

**Status:** semantic prototype v0.2. No production renderer yet.

## The problem

Distinct traditions may use the same words for different concepts, or different words for structurally similar ideas. We want to separate **source terminology**, **conceptual meaning**, and **visual expression** rather than assign arbitrary icons directly to terms.

```text
Primary sources → contextual interpretation → worldview-scoped proposition
                → conceptual interlingua → compositional visual grammar
                → diagrams and animation → comprehension testing
```

The aim is to model what a tradition *claims*, not to endorse its metaphysics. Presentation may use a single opening attribution/disclaimer rather than per-scene epistemic qualifiers; detailed research evidence remains in the model.

## Current materials

| Path | Purpose |
| --- | --- |
| [`docs/v0.2.md`](docs/v0.2.md) | Current semantic specification, decisions and limitations |
| [`data/v0.2.json`](data/v0.2.json) | 29 translated propositions: Gurdjieff, Bailey, Plotinus, Dennett, and constructed tests |
| [`schemas/v0.2.schema.json`](schemas/v0.2.schema.json) | JSON Schema for expression structure |
| [`reports/v0.2.validation.json`](reports/v0.2.validation.json) | Original structural validation results |
| [`docs/v0.1.md`](docs/v0.1.md) and [`data/v0.1.json`](data/v0.1.json) | Earlier ontology and 12-proposition corpus |
| [`scripts/build_v02.py`](scripts/build_v02.py) | Reconstruct the v0.2 corpus and schema from v0.1 |
| [`scripts/validate.py`](scripts/validate.py) | Revalidate corpus structure, roles and type constraints |
| [`tests/test_interlingua.py`](tests/test_interlingua.py) | Regression checks against malformed claims |
| [`examples/gurdjieff_cosmic_myth.mp4`](examples/gurdjieff_cosmic_myth.mp4) | Prior programmatic animation, a stylistic reference rather than a renderer output |

## Local usage

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

To regenerate the current data files from v0.1:

```bash
python scripts/build_v02.py
python scripts/validate.py
```

## Key design requirements

- **Theory-relative semantics:** assertions belong to a named tradition or model; incompatibilities between traditions do not become contradictions in the interlingua.
- **Composable meaning:** complex visual expressions should be derived from reusable spatial and temporal operations where possible.
- **Visual pluralism:** iconic depictions and learned conventional signs are permitted alongside compositional geometry.
- **No forced conflations:** subjective experience, awareness, deliberation, choice, free will, and moral responsibility must be separately expressible.
- **No false mechanics:** material transfer, existential dependence, logical implication, and moral obligation must not all render as the same causal flow.
- **Research provenance:** keep source locations and interpretation notes in the corpus, without requiring intrusive on-screen disclaimers.

## Visual experiments

- **[Experiment 001 — The Earth as Transmitter](experiments/001-lunar-nourishment/README.md)**: art-directed, source-grounded 28-second animation of Gurdjieff's lunar nourishment with semantic scene manifest, reusable renderer, storyboard, assessment and tests. The video is [in the repository](experiments/001-lunar-nourishment/visual-experiment-001.mp4).

## Proposed next milestone

Build three small animations from the same semantics-to-visuals pipeline. Test (1) experience versus awareness, (2) choosing versus having the ability to do otherwise, and (3) cosmic nourishment versus existential grounding. Evaluate intelligibility with people unfamiliar with the ontology before expanding its primitive vocabulary.

## Limitations

Schema/type validation does **not** prove philosophical correctness of a translation. The current 39 predicates are a provisional lexicon, **not** 39 visual primitives. There is no claim of mathematical minimality or demonstrated viewer comprehension.

## License

No license has been selected yet. Do not presume permission to redistribute third-party source texts or imagery. The initial animation is an internally generated reference asset.
