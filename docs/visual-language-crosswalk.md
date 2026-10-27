# Relationship to `visual-language`

**Reviewed:** 2026-10-27  
**Source:** [BrianMills2718/visual-language](https://github.com/BrianMills2718/visual-language) (`main`)  
**Status:** architecture comparison; no code imported or dependency added.

## Assessment

**Substantial conceptual overlap, complementary scope, premature for code-level integration.**

`lore-interlingua` translates claims made in different philosophical and esoteric traditions into a theory-scoped conceptual representation. `visual-language` investigates a general **temporal visual notation**: stable rules for turning semantic operations into geometric and time-varying marks. Both distinguish semantics from graphics; neither should substitute a pretty animation for an explicit meaning contract.

The two projects are best modeled as separate layers:

```text
lore-specific sources / vocabulary
      ↓
lore-interlingua: scoped, typed conceptual claims
      ↓
semantic projection: the claim and distinctions a viewer needs
      ↓
visual-language: candidate grammar rules and visual operators
      ↓
renderer: Canvas / SVG / video
```

This is a **candidate integration**, not an existing executable pipeline.

## Reusable elements

| Source | Value for lore-interlingua | Constraint |
|---|---|---|
| [Architecture and Scope](https://github.com/BrianMills2718/visual-language/blob/main/docs/ARCHITECTURE_AND_SCOPE.md) | Semantic model → viewpoint/projection → notation → renderer separation | Lore translation happens before projection; do not bury it in visual styling |
| [Visual Semantics](https://github.com/BrianMills2718/visual-language/blob/main/docs/VISUAL_SEMANTICS.md) | Identity, persistence, causality, scope, topology, and timescale invariants | Meaning-bearing marks must not silently imply claims absent from the source |
| [Primitive Catalog](https://github.com/BrianMills2718/visual-language/blob/main/catalog/primitives.yaml) | Candidate `node`, `marker`, `track`, `region`, `link`, `boundary`; time variables and composable operators | These are graphic elements, **not** interlingua semantic primitives |
| [Grammar Rules](https://github.com/BrianMills2718/visual-language/blob/main/catalog/grammar-rules.yaml) | Candidate rules for recurrence, delayed transfer, synchronization, and relation creation | All are experimental; do not mark as validated |
| [Notation Literacy Experiment](https://github.com/BrianMills2718/visual-language/blob/main/experiments/001-notation-literacy.md) | Learn → decode unseen combinations → transfer across domains → static-baseline comparison | Especially important for testing supposedly intuitive symbolism |
| [Notation renderer](https://github.com/BrianMills2718/visual-language/blob/main/notation.js) | Renderer-native notation key and sample Canvas implementations of G1–G4 | Code is presentation-specific and partly imperative; no general semantic input API |
| [Crusoe experiment](https://github.com/BrianMills2718/visual-language/blob/main/docs/CRUSOE_CONSTRUCTION.md) | Add one mechanism at a time, use negative controls, compare static alternatives | The prebiological ladder is a separate research agenda, not lore ontology |

## Key non-equivalences

1. **Animated explanation ≠ visual notation.** The previous Gurdjieff MP4 is an explanatory artifact. A compositional language must work with previously unseen subjects after the viewer learns a key.
2. **Transfer ≠ grounding.** Gurdjieff's asserted energetic nourishment may be depicted as a transfer; Plotinian ontological dependence cannot automatically use moving particles or a time-delayed arrow.
3. **Differentiation ≠ splitting a material object.** Bailey's seven rays may be qualitative expressions, not seven resources physically depleted from the source.
4. **Observation ≠ experience.** The Crusoe workbench's read-only observation register is not sufficient to express subjective experience or reflexive awareness.
5. **Choice ≠ libertarian free will ≠ moral responsibility.** A learned rule for selecting alternatives must not imply metaphysical freedom or moral status.
6. **Temporal presentation ≠ temporal occurrence.** Revealing an atemporal relation over several seconds does not license the claim that the represented process took time.

## Proposed minimal cross-project experiment

Use one `lore-interlingua` corpus and a small borrowed *candidate* notation key, but keep implementations independent.

| Corpus case | Meaning to preserve | First candidate visuals | Failure control |
|---|---|---|---|
| Gurdjieff: organic life nourishes Moon | Recipient-dependence and asserted transfer of a particular cosmic substance | Nodes, bound relation, traveling marker, optional receiving-state effect | Compare against a persistent, non-transferring relation |
| Bailey: one Life expresses seven rays | Differentiation of qualities without assumed source depletion | One identity with seven coordinated distinguishable expressions | Viewers must not read this as seven units of mass being shipped |
| Plotinus: Intellect grounded in the One | Existence-dependence without motion, depletion, or chronological production | Persistent relation, relative dependence with an atemporal key | Freeze test: remove time cues, ensure the relation remains intelligible |
| Gurdjieff: self-remembering | Experience, attending to an object, reflexive awareness | New grammar candidate; no existing G1–G6 encoding yet | Must distinguish attention from reflection without labeling every scene |

Success requires (1) correspondence with the interlingua claim, (2) compositional reuse, (3) readers trained on a compact key decoding **unseen** examples, and (4) a meaningful gain over static figures. Failure should trigger notation revision, **not** a post-hoc reinterpretation of the lore.

## Project-management recommendation

**Keep the repositories independent now.** Reuse experimental protocols and conceptual constraints immediately; avoid copying the whole `visual-language` codebase. When two or more cross-domain experiments establish stable, useful conventions, define a versioned intermediate visualization schema and then consider a shared renderer or library.

No evidence currently establishes that the candidate `visual-language` grammar is learned reliably by outside viewers; its written tests describe research plans rather than demonstrated results.
