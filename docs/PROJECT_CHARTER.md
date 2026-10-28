# Project Charter — Lore Interlingua

**Authority:** This is the current normative project statement. Historical semantic specifications, film treatments, research notebooks, and issue discussions are evidence of how the project developed; they do not silently override this charter. See [Current State and Recovery Plan](PROJECT_STATUS.md).

## Mission

Develop a **visual and multimodal instrument for thinking about, exploring, and communicating coherent philosophical, esoteric, religious, and metaphysical systems**. A shared conceptual interlingua (an intermediate representation of concepts) and a compositional visual vocabulary are tools for this artistic and intellectual activity, not ends or restrictions in themselves.

Three intertwined functions:

1. **Represent:** externalize concepts and lore relationships through depiction, symbols, geometry, text, narration, and motion.
2. **Manipulate / reason:** vary a representation, its perspective, components or explicitly permitted transformations to explore consequences and dependencies.
3. **Reveal / discover:** recognize previously unnoticed similarities, distinctions, tensions, ambiguities or new questions; feed them back into source interpretation and design.

Formal entailment, analogy and imaginative discovery are **different**. A visually suggestive manipulation is not by itself a logical inference or evidence that any lore is empirically true.

## Operating principles

- **One coherent lore per audience-facing lore film, initially.** Scope a specific tradition, primary text or doctrinal strand; present its *positive internal claims*, not mainly contrasts against another system. Internal research and comparison artifacts may cover multiple renderings or traditions.
- **Source first; rendering free.** Define the essential subjects, relations, processes, and narrative scope before choosing central images. Preserve source provenance and significant interpretive uncertainty in research notes; an audience-facing work can have a concise initial attribution.
- **Artistic practice is irreducible.** Formal systems guide choices but do not mechanically generate all meaningful forms. Permit recognized iconography, invented metaphors, ornament, and experimental imagery.
- **Selective metaphor, not literalism.** Water may represent grace or transformation without claiming grace has volume or viscosity. Ask which correspondences matter and whether a metaphor's dominant reading contradicts the represented lore.
- **Text remains first class.** Label, narrate or explicitly state what visual forms cannot convey better. Avoid both text-only slide decks with decorative motion and a purist ban on verbal explanation.
- **First-contact access plus cumulative literacy.** Films should be accessible without prerequisite notation lessons; repeated visual conventions can reward experienced viewers, and optional videos may teach the grammar explicitly.
- **Atemporal and temporal structures are equally legitimate.** Domain time (in the represented world), presentation time, and manipulation time are distinct. Representing a timeless relationship is already ordinary; our problem is expressive richness, compositional fidelity and usefulness.
- **Example-driven iteration.** Create source-grounded examples and visual explorations; find gaps; revise the interlingua or visual vocabulary when justified. Do not expand ontology merely because new labels are imaginable.
- **Preserve alternatives without forcing equivalence.** Different traditions' words may conceal similar structures or different structures; correspondences must be investigated, not declared through lexical resemblance.
- **Critical project management.** Challenge weak choices, distinguish unverified hypotheses from settled claims, record corrections rather than overwriting history, and prioritize a credible development path over output volume.

## Separate products and evidence

| Work product | Purpose | Quality claim it may support |
| --- | --- | --- |
| Source-scoped lore model | Trace an internally coherent tradition's propositions and roles | Interpretive fidelity, pending source review |
| Conceptual interlingua | Make comparable relations and operations explicit across traditions | Structural expressibility, not philosophical truth |
| Visual-thinking study | Explore alternative imagery or manipulate a conceptual system | New questions, useful analogies and diagnosed gaps |
| Visual notation candidate | Offer reusable visual composition rules | Candidate learnability and semantic consistency, not universal meaning |
| Audience-facing film | Provide an artistic, understandable encounter with one lore | Narrative and communicative quality, not proof that the notation is general |
| Tests and benchmarks | Catch implementation mistakes or characterize a specific experience | Local properties only; not existential project viability |
| Inquiry Graph entry | Preserve how inquiry changed, with attribution | Research trajectory and decision history, not a truth store |

**A film is not proof of a compiler. A passing JSON Schema is not verification of a doctrine. A beautiful metaphor is not a logical theorem. A static diagram can be the best choice.**

## Architecture — conceptual, not an implemented pipeline

```text
selected source tradition / lore corpus
        |
        v
source-scoped interpretation and conceptual roles
        |                ^
        v                | revisions from visual inquiry
optional interlingua / explicit semantic structures
        |                ^
        v                |
art-directed visual and verbal compositions  <-->  manipulation
        |                |
        +--> audience-facing narrative and communication
        +--> discovered gaps, hypotheses and questions --> source research
```

There is **no working general pipeline** converting the v0.2 JSON corpus into finished videos. Current experiments are independently coded/art-directed. That is a documented limitation, not a production failure that a test suite hides.

## Repository responsibilities

- **[lore-interlingua](https://github.com/BrianMills2718/lore-interlingua)** owns tradition-specific source models, the candidate conceptual interlingua, lore-specific visual studies, artistic production notes and the project decision record.
- **[visual-language](https://github.com/BrianMills2718/visual-language)** separately investigates learned temporal notation, visual semantics, operations and audience decoding. Borrow concepts, tests and stable rules when justified. It is *not yet* a drop-in renderer for lore films. Its learned-notation orientation is narrower than the present project's iconic, metaphorical and first-contact communication aims.
- **[inquiry-graph](https://github.com/BrianMills2718/inquiry-graph)** owns source-anchored histories of questions, challenges, reframings and positions. It does not decide Catholic doctrine or own the visual grammar.

Do not duplicate a general renderer, generic ontology framework, or reasoning theory in this repository without first demonstrating a residual requirement unmet by existing work.

## What success can look like

A useful *partial* capability is sufficient: a vocabulary of reliable visual correspondences and expressive creative methods that helps us think better about some philosophical relations and make worthwhile films. Full automatic rendering, universal metaphysical translation, and the elimination of language are **not** success prerequisites.

Decisions about priority and value are architectural/strategic judgments informed by examples and opportunity costs, **not** benchmark thresholds. Individual poor animations justify criticism of their design, not an impossibility claim about visual representation.

## Current next action

Follow [Current State and Recovery Plan](PROJECT_STATUS.md) and the [Experiment Registry](EXPERIMENT_REGISTRY.md). First consolidate the corpus-to-scene relationship and choose one *actual lore mechanism* with identifiable visual operations; do not manufacture an additional feasibility question about whether timeless ideas can be depicted.
