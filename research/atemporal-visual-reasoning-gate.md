# First-principles appraisal — atemporal visual reasoning

**Status:** Revised 2026-10-27 after a project-management correction. This supersedes the earlier benchmark-based *go/no-go gate*, which remains visible in Git history. **Current disposition: continue a bounded architectural investigation; suspend the ineffective slideshow-style production pipeline; do not make the fate of the research program contingent on a small benchmark.**

## Decision problem: five distinct questions

1. **Conceptual coherence:** Can we describe the intended capability without contradiction? What would count as representation, manipulation, and discovery? Do we require complete translation of every metaphysical concept (probably untenable), or useful selective representations?
2. **Possibility in principle:** Can symbols, spatial relations, motion, text, and interaction convey timeless as well as temporal distinctions? Can exploration of a representation reveal properties without falsely asserting that the represented world changes? A constructive instance establishes **local possibility**, not universal expressive adequacy.
3. **Tractability:** Can the capability be decomposed into learnable and buildable subproblems using existing ideas and tools? What are the hard unknowns: conceptual translation, visual semantics, aesthetic direction, formal manipulation, and user interpretation?
4. **Path / intellectual leverage:** Is there a sequence of work in which solving one problem unlocks the next, with discoveries carried forward into a reusable vocabulary? Does any abstraction do useful work rather than becoming a second project?
5. **Value:** Would a partial system—supporting visual thought, artistic investigation and communication in some domains—be worthwhile? Value is a goal-relative judgment, not a theorem or a score fixed by a benchmark.

**Do not infer impossibility from underperforming examples.** A benchmark compares particular implementations under chosen tasks and viewers. It does not bound all possible representations, establish a universal impossibility, or decide the worth of an open-ended artistic-research program.

## First-principles reasoning

### A. Atemporal subject matter poses no inherent contradiction to dynamic representation

Separate **domain time** (whether the depicted reality itself changes), **presentation time** (the order in which we encounter the representation), and **manipulation time** (the order in which we modify a representation, instance, or viewpoint).

An unchanged relationship can be revealed progressively or explored by moving a representation. This does not require assigning a time coordinate to the underlying relationship.

**Constructive example:** In Euclidean geometry, deforming a valid triangle changes its angles but preserves their sum. The movement is in a sequence of *instances inspected*, not a history of the theorem becoming true. This shows one instance of the needed distinction, not that Catholic eternity or Plotinian dependence is equivalent to geometry.

### B. Representation and reasoning are already separable

A visual **depiction** makes a concept perceptible. A visual **reasoning operation** changes a representation according to declared rules, or explores a metaphor to generate hypotheses. A **discovery** can be a new question or structural distinction, not only a proven consequence. Distinguish:
- rule-preserving transformations (licensed conditional on explicit semantics);
- analogical exploration (suggestive, not deductive);
- aesthetic/interpretive discovery (valuable without formal inference).

These modes can coexist within one artistic practice.

### C. Generality is graded rather than all-or-nothing

The weakest goal—*make any single lore film*—is trivial and already partly achieved. A stronger one—*reuse a visual vocabulary across related conceptual relationships*—is plausible but unproven. Stronger still—*systematically compose and manipulate structures to reveal implications*—requires explicit semantic constraints and successful examples. **A universal automatic compiler from arbitrary metaphysics to intuitively legible cinema is not a justified requirement.**

The project may succeed with a partial, artistically directed, multimodal medium. It must not be judged as failing merely because one metaphysical concept still needs text or a conventional symbol.

### D. A credible path can be identified without pretending the result is guaranteed

Use proven or plausible building blocks: conceptual source modeling; compositional diagrams; traditional iconography and metaphor; temporal visual notation; typed identities/relations; interactive manipulation; a disciplined research log.

**Critical uncertainty:** The cross-domain translation layer may fail to preserve distinctions while producing communicatively useful visuals. We do not currently possess a demonstrated general semantic compiler, and examples from mathematics do not settle that problem.

## Decision rubric — assessed by argument, not scores

| Question | Present assessment | What could change the assessment |
| --- | --- | --- |
| Is it coherent to depict atemporal relationships dynamically? | **Yes in principle** if domain time and presentation/manipulation time are separated. | A requirement that insists all animation depicts actual physical/historical change would contradict this, but that is not our goal. |
| Is some visual reasoning possible? | **Yes for some domains**, as illustrated by standard geometric/diagrammatic constructions. | An argument showing our exact desired class of semantics cannot be mapped meaningfully; no such argument exists. |
| Can we encompass all metaphysical lore faithfully and intuitively? | **No established justification.** Treat as an open, probably overbroad aspiration. | A rigorous compositional translation framework and many independent cases could improve confidence, never prove unbounded universality. |
| Is there a meaningful partial architecture? | **Yes, provisional:** source lore → explicit conceptual relations → artistic visual construction ↔ manipulation → questions/insights → source/model revision. | Discovering that each stage necessarily erases distinctions essential to the next would require major revision. |
| Is the project's value nontrivial even if partial? | **Potentially**, because expression, private visual thought, and cumulative conventions may each be independently valuable. | Artistic goals, opportunity costs, and practical usefulness are decisions by the project owner, informed by examples but not dictated by a benchmark. |

**Disposition:** Continue as exploratory artistic and conceptual R&D. Discontinue the current practice of using polished videos or slideshow comparisons as evidence of fundamental project viability. Restrict effort on general automation until reusable semantics appear.

## Architecture path, with explicit questions

**Step 1 — specify a minimal distinction, not a complete cosmology:** an entity's identity, its relationship to another, and whether that relationship is temporal, persistent, or atemporal. Do not assume these are all geometrically the same.

**Step 2 — use a constructive exemplar:** e.g., the existing triangle invariant pilot `experiments/008-atemporal-invariant`. Ask what it *demonstrates logically* about the distinction between changing instances and invariant claims, and what it does not show about metaphysics. The current construction is sufficient as a calibration artifact; further benchmark work is optional.

**Step 3 — translate one metaphysical case:** an explicitly scoped passage from Plotinus or Catholic theology with an atemporal relationship. Specify the tradition's interpretation and where any analogical visual convention is selective, not literal.

**Step 4 — make one manipulate-and-discover operation:** the viewer can vary viewpoint, arrangement, or hypothesis and inspect what remains constant. We must distinguish exploratory edits of an idea from edits to the tradition's asserted doctrine.

**Step 5 — assess the conceptual gap and dependency chain:** Did the experiment expose a principled obstacle, a representational choice needing art direction, or a missing formal distinction? Identify a *specific next subproblem with an apparent solution path* before investing heavily.

**Step 6 — iterate or narrow based on reasoning:** keep work if there are promising unexplored routes and value in the partial capability. Narrow if generality is overclaimed. Pause or spike a particular technical approach if it depends on impossible conditions, duplicates mature prior art without benefit, or has no credible route forward relative to goals/resources. Poor results from one implementation alone warrant redesigning that implementation, not abandoning the research vision.

## Role of experiments

Experiments and viewer tests are **diagnostic evidence** about interpretation, usability and performance. They can reveal hidden assumptions, provide counterexamples to design claims, expose implementation flaws, or show practical limitations. They are not a constitutional go/no-go vote on possibility or project value.

If tests are run, avoid claiming any universal conclusion. Their role is to sharpen the conceptual model and decide which *local design* to pursue.

## Current constraints and immediate work

- Preserve the `visual-language` research; don't build a duplicate visual-notation framework.
- No additional full lore movie as an attempted project-validity demonstration.
- Do not overbuild an ontology to give an illusion of progress.
- Next substantive analysis: articulate one compelling **atemporal metaphysical relation** and two possible representational mechanisms, reasoning through each mechanism's invariants, ambiguities, and affordances before coding anything else.
- Explicitly separate what our system **expresses**, what it **licenses us to infer**, and what it merely **suggests**.

## Links

- [Visual reasoning as an instrument](../docs/visual-reasoning-instrument.md)
- [Communication-first artistic design](../docs/communication-first-design.md)
- [Existing triangle pilot](../experiments/008-atemporal-invariant/)
- [Visual Language — notation literacy](https://github.com/BrianMills2718/visual-language/blob/main/experiments/001-notation-literacy.md)
- [Issue #15](https://github.com/BrianMills2718/lore-interlingua/issues/15)
