# Notation and comprehension — research method, not a standardized grammar

**Status (2026-10-29):** A **provisional design and evaluation guide** for Lore Interlingua. This is not a new source of metaphysical claims, an approved symbol dictionary, an implemented compiler, or evidence of audience learning. The [Project Charter](PROJECT_CHARTER.md) governs goals and artistic freedom; [current status](PROJECT_STATUS.md) and [decision record](DECISIONS.md) govern what work is actually complete.

## Objective and evidence

Two priorities, which require different evidence:

1. **Comprehension:** after encountering an explanation, can a viewer reconstruct the *source-scoped* roles, distinctions and conditions without importing major unsupported causal claims?
2. **Reusable notation:** after learning a convention with one example, can a viewer decode that convention in a materially changed example rather than recognizing only the original artwork?

A visually attractive result, source-aligned captions, an executable schema, and repeated graphics **do not** establish either outcome on their own. The work can remain artistically valuable without claiming a formal universal language.

## The upstream/downstream boundary

```text
selected source passage and interpretive limits
                 ↓
source-scoped conceptual model (whole concepts, facets, relationships, constraints)
                 ↓
selected explanatory view / level of conceptual detail
                 ├── candidate visual, verbal and motion conventions
                 └── explanatory traversal (what to disclose and in what order)
                                  ↓
              storyboard, interactive view, film, or other composition
                                  ↓
          viewer interpretation / manipulation / critique
                                  ↺ source and design revision
```

**Upstream means the model exists independently of the order of shots.** A traversal *linearizes* an explanation; it may begin at a recipient and later reveal its source without asserting that the recipient historically precedes or causes the source. Keep **domain time**, **presentation time**, and **manipulation time** distinct.

The model can preserve **one concept with inspectable facets** (e.g., organic life with grassland and human-gathering examples), rather than creating a disconnected node for every property. A designer can retain an object of attention while inspecting relations and detail; whether that improves learning must still be tested.

## Moody's Physics of Notations as a design audit

**Reference:** Daniel L. Moody, “[The ‘Physics’ of Notations: Toward a Scientific Basis for Constructing Visual Notations in Software Engineering](https://doi.org/10.1109/TSE.2009.67),” *IEEE Transactions on Software Engineering* **35**(6), 756–779 (2009).

The paper proposes **nine principles of cognitive effectiveness** for external *diagrammatic notation*. It is directly relevant to designing a **learnable, discriminable visual vocabulary**, but does **not** validate philosophical source interpretations, mental phenomenology, film editing, or audience comprehension of a specific artifact. Using the principles for motion, voice, cinematography or interactive reveal is an **adaptation** of the original scope, not a result established by the 2009 paper.

| Principle | Question to audit in Lore Interlingua |
| --- | --- |
| **Semiotic clarity** | Do different intended constructs have distinguishable signs? Is one sign overloaded or an important relation left unencoded? |
| **Perceptual discriminability** | Can viewers tell the marks apart using shape, behavior, location and labeling—not color alone? |
| **Semantic transparency** | Do familiar icons convey a helpful first interpretation, or does a metaphor suggest the wrong mechanism? |
| **Complexity management** | Can a concept remain a coherent whole while the presentation reveals selected facets or nested detail? |
| **Cognitive integration** | Can a viewer preserve participant identity and context across views, scene transitions and camera movement? |
| **Visual expressiveness** | Do multiple visual variables carry meaningful, nonredundant distinctions without inventing source-specific physical measurements? |
| **Dual coding** | Do words/captions/narration and visual behavior support the same meaning, including where the graphic cannot be self-explanatory? |
| **Graphic economy** | Is the learned vocabulary small enough to retain without forcing genuinely different relations into one ambiguous sign? |
| **Cognitive fit** | Does the form suit this task and audience? An initial public film and an expert diagnostic atlas may use different levels of symbolic compression. |

**Trade-offs are expected.** Increasing distinctions can inflate the symbol inventory; reducing the inventory can blur different meanings. Artistic ornaments need not each be formal semantic tokens, but a visually dominant misleading correspondence needs review.

## Worked case: G02 organic-life mediation

**Reported claim:** Within Gurdjieff's cosmological account as described by P. D. Ouspensky, planetary influences are received by terrestrial organic life, which mediates them to Earth. See [corpus G02](../data/v0.2.json), [Experiment 010](../experiments/010-living-intermediary/README.md) and the [Film 013 audit](../experiments/013-living-interval/CONTINUITY_AND_EXPLANATION.md).

| Element of model | Proposed meaning-bearing difference | Misreading to investigate |
| --- | --- | --- |
| **Reception** (planetary world → organic life) | Incoming symbolic indication **ends at living subjects**; context stays visible | Physical particles with asserted speed, quantity or biochemical absorption |
| **Mediation** (organic life → Earth) | A distinct, locally originated **relationship to Earth** is revealed, not simply more of the identical incoming dots | An asserted one-to-one physical transduction or conservation equation |
| **Intermediary requirement** | The G02 **represented mediated relation** depends on organic life's presence | Bare ground receives no other forces whatsoever |
| **Grassland / human gathering** | Inspectable alternatives *within* the organic-life concept, with source-reported differences in received influences | Exactly two named particle species or empirically known living filter frequencies |

The **concept identity** and its **relationship role** are different things. Organic life is an intermediary in G02 and a source of differentiated outward radiation in G03. A reusable notation should bind marks to *roles within a specified relation*, not permanently decree that a particular physical object is always a recipient or intermediary.

Candidate colors, glyphs, motion rates and imagery are **art direction** until their selected meanings and nonclaims are documented. Neither a generic arrow nor a moving particle is automatically an adequate sign for every dependency.

## How to evaluate candidates

Use a lightweight record for each candidate convention: **source claim → relationship and constraints → visible/verbal features → intended reading → plausible false reading → comparison treatment → observed viewer interpretations**.

**First-contact comprehension:** Show unfamiliar viewers an explanation with appropriate labels/narration, then ask them to identify the source, intermediary and recipient; describe *why* the intermediary matters; and explain the difference between reception and mediation. Invite their own diagrams or verbal reconstructions and separately record unsupported inferences (e.g., actual particles, transfer rates, or direct Earth reception).

**Learned reuse:** Explicitly teach a sign, then test it in a different source-scoped example in which the entities change but the *structural relationship* is legitimately comparable. Avoid implying doctrinal equivalence merely because a symbol recurs. Consider an alternative notation or a well-written text/static baseline, with order counterbalanced where feasible.

**Comprehension and notation transfer are separate outcomes.** A small formative study (for example 8–12 people) is for detecting confusion, not estimating general effectiveness. Tests of structural consistency or JSON references do not replace these audience tasks.

## Thoughtfeel: inspiration, not a validity shortcut

Discussions in [r/MentalAtlas](https://www.reddit.com/r/MentalAtlas/) and the [thoughtfeel explanation](https://thoughtfeel.net/what-is-thoughtfeel/) describe a reported personal experience of attending to concepts beyond inner speech or mental imagery. The useful **design hypothesis** is to preserve coherent conceptual wholes with inspectable properties and relationships. Introspective reports are **not** evidence that this project's particular external notation improves learning. Use independently observable comprehension and transfer tasks.

## Existing and proposed work

- The [encyclopedia](../encyclopedia/README.md) is an existing **provisional research atlas**; the offline v0.4 review package and current Film 013 imagery should not be conflated.
- [Experiment 014 PR #37](https://github.com/BrianMills2718/lore-interlingua/pull/37) is **proposed, not yet merged into `main` as of this document update**. Its concept model, five candidate correspondences and two traversals specify semantic intent, but **not** a finished graphical syntax, storyboard, viewer trial or transferable grammar.
- **Next after merge:** create concrete, alternative graphical realizations and an inspectable view; linearize the same G02 model into two storyboard treatments; audit fidelity and likely sign confusion; then evaluate comprehension and learned reuse.
- The neighboring [visual-language project](https://github.com/BrianMills2718/visual-language) remains the experimental home of general learned temporal-notation research. Reuse genuinely useful conventions rather than duplicating its speculative grammar in this repository.
