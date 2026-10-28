# Current State and Recovery Plan

**Review date:** 2026-10-27. **Scope:** lore-interlingua's current main branch, significant historical conversation decisions, the related visual-language and inquiry-graph projects. This is a **documentation/architecture audit**, not a revalidation of every theology passage, source link or binary frame.

**Decision:** Keep the project. **Retire the slideshow-style production workflow as the default research method.** Do not frame the basic ability to depict timeless relations as an open feasibility question. Do not add another ontology or full renderer before identifying a concrete missing capability.

## 1. Current inventory and quality of evidence

- **Research corpus:** v0.1 (12 examples) and v0.2 (29 propositions, 15 sorts and 39 typed predicates). The JSON Schema, structural validator, and corpus tests are real. They check shapes, types, references and declared modalities; they do **not** prove that philosophical translations are accurate.
- **Research models:** A Catholic world model has a separate typed JSON structure, concept roles and selected Catechism references. It is not ingested by the shared v0.2 interlingua or a generic renderer.
- **Film/visual assets:** Eight numbered experiments (with 003–004 grouped in one folder) plus an earlier 48-second example, of different types; see [Experiment Registry](EXPERIMENT_REGISTRY.md). Some have video/source checked in, some only semantic descriptions or an interactive HTML.
- **Artistic/semantic practice:** [Communication-first design](communication-first-design.md), [Visual reasoning instrument](visual-reasoning-instrument.md), and [Project Charter](PROJECT_CHARTER.md) articulate the current philosophy, but their historical amendment sequence needs one canonical summary.
- **Related projects:** `visual-language` has notation primitives, temporal rules, and experimental protocols; it is not a production-ready lore compositor. `inquiry-graph` holds a curated, incomplete source-anchored conversation trajectory (not a full native ChatGPT export).
- **CI:** v0.2 validation, Python unit tests and scene tests for Experiments 001–002. The broader test directory also contains tests for the Catholic world model and Experiment 008. Passing CI does not establish audience understanding, metaphysical truth, semantic generality or visual elegance.

## 2. Audit findings / dispositions

| ID | Priority | Finding and evidence | Disposition |
| --- | --- | --- | --- |
| A01 | **P0** | Root README says "semantic prototype v0.2; no production renderer" and points to a superseded three-animation milestone. | **Fix now**: accurate charter, inventory, status and navigation; retain versioned semantics as historical milestones. |
| A02 | **P0** | `docs/v0.2.md`, experiment notes and Catholic casting memo contain "next gate" instructions that were superseded later. | **Fix now**: visible archival notices, links to this status; preserve historical findings rather than rewriting the record. |
| A03 | **P0** | The no-go benchmark and atemporal "feasibility" questions were superseded; `experiments/008-atemporal-invariant/README.md` still invokes the original gate. | **Fix now**: mark the illustration as narrow and diagnostic, not the project's decision criterion. |
| A04 | **P0** | No central index identifies which experiment videos/renderers/HTML are actually in the repository. Some linked chat packages are not checked in. | **Fix now**: classify artifacts and unresolved reproducibility in [Experiment Registry](EXPERIMENT_REGISTRY.md). |
| A05 | **P1** | `data/v0.2.json` and scene contracts are different manually authored formats; none of 001–008 is a proof of a generalized corpus-to-animation pipeline. | **Investigate next**: design a *minimal semantic-to-scene trace* for one small lore claim, rather than a new universal schema. |
| A06 | **P1** | The v0.2 corpus and Catholic model cite primary and secondary sources, but source-to-claim interpretive accuracy has not undergone independent textual audit. | **Queue a targeted source review** for whichever doctrine becomes the next case; do not imply schema checks verify content. |
| A07 | **P1** | `visual-language` and this repo both discuss notation, operations and comprehension. Ownership is not yet embodied in a shared contract. | **Reuse-first integration**: let lore-interlingua own source-scoped models and artistic studies; borrow candidate notation from visual-language; define an interchange example only after a real use. |
| A08 | **P1** | Repeated graphics (circle, gold contour, arrows) were used without clear semantic identities; captions often carry all substantive claims. | **Change production workflow**: semantic casting and visual operation analysis before rendering, with artistic liberty explicitly preserved. |
| A09 | **P2** | Status metadata and file naming vary across experiments; 003–004 renderers and media were shared as conversation downloads, not checked into GitHub. | **Inventory first**, then decide whether to import missing source/binaries or mark as irreproducible historic artifacts. Avoid pretending all outputs are reproducible. |
| A10 | **P2** | Research decision provenance lives in chat, issues and isolated docs; not all corrections reached experiment READMEs. | **Use one decision log** with superseded status and canonical links; keep Inquiry Graph for question history, not truth/authorization. |
| A11 | **P2** | Licensing is unspecified; user excerpts and metadata are present in publicly accessible repositories; some primary-source permissions differ. | **Governance review** before publishing larger conversation dumps or third-party media; do not silently assume free redistribution. |
| A12 | **P2** | Automated checks are narrow and do not cover link integrity, source availability or scene contract semantics end-to-end. | **Keep claims calibrated.** Add lightweight checks when repeated failures justify them; do not turn test counts into a proxy for conceptual progress. |

## 3. Proposed authoritative document structure

- **[PROJECT_CHARTER](PROJECT_CHARTER.md)** — current goal, what success means, allowed artistic methods, repo boundaries; edit only through explicit decision.
- **[PROJECT_STATUS](PROJECT_STATUS.md)** — current research state, audit, prioritized next work; update as work changes.
- **[EXPERIMENT_REGISTRY](EXPERIMENT_REGISTRY.md)** — what artifacts actually exist and what each taught us; do not conflate "rendered" with "validated."
- **[DECISIONS](DECISIONS.md)** — accepted and superseded project decisions with traceable references.
- **[Communication-first design](communication-first-design.md)** and **[Visual reasoning instrument](visual-reasoning-instrument.md)** — detailed supporting methods.
- **[v0.2 semantics](v0.2.md)** and v0.1 — versioned historical specifications, not current roadmaps.
- **[Catholic world model](../research/catholic-world-model/README.md)** — one tradition-specific source reconstruction; not the whole project.
- **[Atemporal reasoning appraisal](../research/atemporal-visual-reasoning-gate.md)** — conceptual argument, not a program-level kill gate.

Do not restructure directories or rename historic assets until downstream links and imports are understood. **Consolidation by indexing and status is safer than destructive deletion.**

## New design reference: encyclopedia v0.1 (2026-10-28)

A browsable [Visual–Semantic Encyclopedia](../encyclopedia/README.md) now brings together twelve connected concepts, source-corpus examples, provisional visual mappings and four small interactive reasoning studies. **It does not create a new upper ontology, verify symbolism, or automate video production.** It is the central index for proposing and criticizing visual choices, not a replacement for the tradition-specific models or the experiment archive. Next, embed a fully scoped *real lore case* (for instance Study 009) with mark-to-meaning links so the atlas does not become detached from artistic work.

## 4. Recommended development path

### Phase I — Fix the question and identify one specific operation

Choose **one source-scoped metaphysical relationship** that has nontrivial structure and might benefit from *manipulation*, not just animated explanation. Recommended initial candidate: **Plotinus' Intellect depends on the One** (a source-scoped atemporal relation), with an explicit note about the limits of our interpretation and analogies. Gurdjieff's mixed-direction nourishment is another candidate if material transformation proves more tractable.

Write a compact scene-semantic contract with:
- the source claim and its primary locator;
- relevant participants and their identity/nature distinctions;
- relation type, temporality, and invariants under manipulation;
- artistically motivated metaphors and what they select from the claim;
- exactly one interactive or dynamic operation that could uncover a question or structural implication;
- which diagram, depiction, text or interactive view is appropriate; motion not obligatory.

**Exit condition:** A claim, an operation and an interpretive question can be stated without inventing an unsupported dynamic or a generic new ontology. This is a design checkpoint, not a benchmark scoring threshold.

### Phase II — One honest bridge, not a new compiler

Build a small `source claim → semantic roles → visual correspondence → optional manipulation → observation` record and a demonstrator. Reuse any appropriate visual-language primitives and existing renderer components. Accept hand-directed construction and text. Record gaps discovered, including cases better expressed statically.

**Exit condition:** We can trace a significant visual choice back to a source-specified conceptual role and explain what manipulating it means. No claim of a general reusable system is needed.

### Phase III — Synthesize only what repeats

After more than one materially different example, consolidate genuinely reusable visual conventions, distinguish them from scene-specific iconography/art direction, and decide whether a shared intermediate schema or reusable tooling solves a recurring problem. The burden is on actual repeated need, not aesthetic similarity alone.

**Exit condition:** A reusable operation preserves its intended meaning across cases *without forcing equivalence*; partial and special-purpose results count.

### Phase IV — Produce public lore films when warranted

Build source-grounded positive narratives, retaining recognizability, art direction, metaphors and optional textual explanation. Don't call a film a formal reasoning system unless one actually exists. Use audience feedback to refine communication, never as a universal viability test.

## 5. What NOT to do next

- Do not produce another 90-second lecture-like slideshow to prove the project.
- Do not add more top-level ontology categories until a real example exposes a missing expressive distinction.
- Do not implement a bespoke general video renderer that duplicates `visual-language` or existing authoring tools.
- Do not require every frame, motif and metaphor to be formally justified.
- Do not demand universal self-explanatory meaning or an automated truth-preserving compiler as a success prerequisite.
- Do not use an arbitrary small benchmark to kill the broader artistic/research endeavor.
- Do not claim basic atemporal representability needs demonstration; that capability is already established.

## 6. Questions to revisit, not decide by fiat

- Is the interlingua primarily a formal logical language, a semantic scene-description system, or several interoperating layers?
- Which relations are meaningfully composable, and which need conventional/evocative symbols?
- Should `visual-language` provide notation patterns only, with a separate artistic authoring layer, or can the interface be richer?
- Which lore case best surfaces both atemporal and temporal relations without spending another sprint on the wrong domain?
- When is a manipulation a formally licensed inference versus a metaphorically provocative rearrangement?

**Project-manager recommendation:** Continue with narrowly scoped, source-anchored visual thinking. The next deliverable should be a **design/mapping exercise** on one real metaphysical relation—not another film, new ontology release, or benchmark debate.
