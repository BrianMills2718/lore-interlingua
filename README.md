# Lore Interlingua

**An artistic and conceptual research project for thinking with, exploring, and communicating philosophical, esoteric, and metaphysical lore through a developing multimodal visual language.**

We use source-grounded conceptual models, reusable visual relations, symbolic imagery, motion, text, and artistic interpretation. The goal is **not** to eliminate words or automatically render every doctrine. Visual representation can also support manipulation and discovery: seeing a relation differently may expose new questions and distinctions.

**Current status (October 2026):** exploratory research. The corpus validator works, and there are several hand-directed animations and interactive studies, but **no demonstrated generic pipeline from the conceptual interlingua to finished films**. The previous animated-slideshow workflow is not the recommended next step. The basic ability to represent atemporal ideas is not in dispute. See the [project audit and recovery plan](docs/PROJECT_STATUS.md).

## Start here

| Document | Role |
| --- | --- |
| **[Project Charter](docs/PROJECT_CHARTER.md)** | Current mission, artistic commitments, semantic boundaries, and project scope |
| **[Visual–Semantic Encyclopedia](encyclopedia/README.md)** · [Open interactive atlas](encyclopedia/index.html) | Thirteen interconnected concepts, four visual hypotheses to manipulate, and the first complete source-linked Gurdjieff case |
| **[Current State / Recovery Plan](docs/PROJECT_STATUS.md)** | Findings, gaps, priorities, and next architectural work |
| **[Experiment Registry](docs/EXPERIMENT_REGISTRY.md)** | Status of Experiments 000–009; what was actually produced and learned |
| [Decision Record](docs/DECISIONS.md) | Retained, revised and superseded project choices |
| [Communication-First Artistic Design](docs/communication-first-design.md) | Metaphor, text, accessibility, one-lore films and artistic freedom |
| [Visual Reasoning Instrument](docs/visual-reasoning-instrument.md) | Representation ↔ manipulation ↔ discovery |
| [Relationship to Visual Language](docs/visual-language-crosswalk.md) | Reuse-first boundary with the separate temporal-notation project |

**Current instructions:** Charter → Status → Registry. The original [v0.1](docs/v0.1.md) and [v0.2](docs/v0.2.md) semantic specifications document earlier versions; their historic "next gate" sections are not the current project plan.

## The Ray of Creation — Experiment 012

**[Experiment 012 — The Ray of Creation](experiments/012-ray-of-creation/README.md)** is a 124-second continuous cosmological film extending the art direction of Experiment 011. It travels through the Absolute, All Worlds, All Suns, Sun, planetary world, Earth and Moon, and presents the source-scoped 1/3/6/12/24/48/96 orders of laws. Increasingly constrained motion is a selective **visual metaphor**, not a literal model of those laws. Its [original visual scene](experiments/012-ray-of-creation/film.html), [source contract](experiments/012-ray-of-creation/scene-contract.json), [caption file](experiments/012-ray-of-creation/captions.srt), reproducible score and MP4 renderer, and [encyclopedia study](encyclopedia/studies/012-ray-of-creation.md) are tracked here. Video remains the primary deliverable; a [directly playable, compressed 480p preview](experiments/012-ray-of-creation/Ray_of_Creation_review_480p.mp4) is archived alongside the sources.

## Earlier audience-facing Gurdjieff film

**[Experiment 011 — The Sensitive Earth](experiments/011-sensitive-earth/README.md)** is an 86-second continuously animated, source-scoped Gurdjieff lore film, with recognizable vegetation, animal and human figures, directional reception, mediation toward Earth, and differentiated radiation to Sun/planets/Moon. The repository includes [the standalone offline picture viewer](experiments/011-sensitive-earth/film.html), [English subtitles](experiments/011-sensitive-earth/captions.srt), [semantic contract](experiments/011-sensitive-earth/scene-contract.json), a [review storyboard](experiments/011-sensitive-earth/review_storyboard.jpg), and a reproducible 1280×720 H.264/AAC rendering workflow. A directly playable [480p film preview](experiments/011-sensitive-earth/The_Sensitive_Earth_review_480p.mp4) is archived here; the full-resolution 1280×720 MP4 was delivered separately in chat and can be reproduced from the renderer. The current film is an artistic interpretation, not an established generic semantic-to-film pipeline.

## Offline review package

The complete **Encyclopedia v0.4 / Experiment 010** review snapshot is [stored on GitHub](downloads/README.md), including a [downloadable ZIP](downloads/Lore_Visual_Semantic_Encyclopedia_v0_4_Living_Intermediary.zip) and a [three-condition comparison image](experiments/010-living-intermediary/review-comparison.jpg). Source files remain editable in their existing directories. No separate chat attachment is required to obtain the review package.

## What exists

- **Visual-semantic encyclopedia:** [Browse 13 concept entries](encyclopedia/index.html), search an ontology-style navigation graph, inspect existing source-scoped claims and experiment with four proposed visual correspondences. It now includes [Gurdjieff Study 009 as a fully annotated applied case](encyclopedia/index.html#case-study), distinguishing depicted claims G02/G03 from contextual claim G04. Data and visual mappings remain provisional, not a new universal ontology.
- **Interlingua research:** [v0.2 corpus](data/v0.2.json) (29 propositions, 15 declared sorts, 39 typed predicates); [JSON Schema](schemas/v0.2.schema.json), [validator](scripts/validate.py) and [unit tests](tests/test_interlingua.py). The earlier [v0.1](data/v0.1.json) includes 12 examples.
- **Tradition-specific model:** [Catholic source-scoped world model](research/catholic-world-model/README.md) and [typed JSON](research/catholic-world-model/v0.1.json), with its own structure, independent of the v0.2 interlingua.
- **Visual work:** [experiment index](docs/EXPERIMENT_REGISTRY.md) links Gurdjieff, Bailey, Manichaeism/Catholicism comparisons, a Catholic visual-thinking workbench, a botanical film, a Trinity–Incarnation animatic, and a mathematical interactive demonstration.
- **Research history:** [Inquiry Graph](https://github.com/BrianMills2718/inquiry-graph/tree/main/examples/conversations/2026-10-25-lore-visual-interlingua) contains selected source-anchored conversation excerpts, **not** a complete export or a truth database.

## Architecture — still under investigation

```text
specific primary-source lore
        ↓
interpretation and roles
        ↕
optional conceptual interlingua
        ↕
art-directed visual / verbal / interactive exploration
        ↔ manipulation and discovered questions
        ↓
film, study, diagram, or other artifact
```

The **interlingua is an optional structuring instrument**, not a doctrinal adjudicator or a requirement that every image be formally derived. Metaphorical correspondences are selective; for example, grace may be depicted as water without claiming it has physical mass. A film can express **one coherent lore** without explaining every interpretive uncertainty on-screen.

## Reproduce the research checks

Python 3.11+, install the small schema dependency:

```bash
python -m pip install -r requirements.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

These validate **structural contracts**, selected invariants and source-reference presence. They do **not** establish doctrinal truth, source-paraphrase correctness, cross-domain visual semantics, or audience comprehension. Animation renderers have separate dependencies; follow their experiment README files.

The corpus can be regenerated from v0.1 with `python scripts/build_v02.py`, but that is a *version-specific build*, not an end-to-end visualization tool.

## Repo boundaries

- [visual-language](https://github.com/BrianMills2718/visual-language) — research into learned, domain-transferable temporal notation; reuse ideas, do not assume its grammar is already an expressive lore renderer.
- [inquiry-graph](https://github.com/BrianMills2718/inquiry-graph) — capture of reasoning trajectory and source-anchored positions.
- This repository — source-scoped lore models, conceptual translation, artistic experiments, and decisions about their relationship.

## What comes next

Per the [recovery plan](docs/PROJECT_STATUS.md): choose one actual metaphysical relation with nontrivial structure; specify source meaning, a visual correspondence, and a potentially illuminating manipulation; produce a *small research study*, not another polished slideshow. Consolidate reusable conventions only after discovering repeated need.

## License and publication

No license is currently selected. Do not presume reuse rights over third-party source texts or media. The repository is public and some project histories include selected user-conversation excerpts; review their publication scope before importing further transcripts or private project material.

## Experiment 009 — Visual encoding audit

The encyclopedia now includes a [source-anchored interactive audit](encyclopedia/studies/009-encoding-audit.html) of whether outgoing colors/shapes encode distinct cosmic mechanisms or chiefly distinguish types of radiation and their destinations. Use **Current marks**, **Uniform marks**, **Swap symbols**, and **Equalize mark speeds** to inspect which graphic choices are conventional. The [findings](encyclopedia/studies/009-encoding-audit.md) separate G03's source-asserted differences in kind from unsourced differences in speed or physical mechanism. This is a design investigation, **not** a viewer test or general ontology expansion.

## Experiment 010 — The Living Intermediary

The [interactive study](experiments/010-living-intermediary/index.html) explores organic life's mediating role in Gurdjieff's cosmology through bare-ground, grassland and human-gathering conditions. The visual-semantic encyclopedia now includes [Mediation](encyclopedia/index.html) as its thirteenth concept and a second applied case. These are source-scoped artistic experiments, not physical simulations or established universal notation.
