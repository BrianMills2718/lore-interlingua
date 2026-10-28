# Rescue gate: atemporal structure versus temporal representation

**Status:** Proposed go/no-go experiment. Owner decision from 2026-10-27 discussion: **continue the bounded research question, stop the current cinematic-diagram pipeline**. This is not a commitment to a general-purpose metaphysical animation compiler.

## Why
Experiments 001–007 improved semantic specificity and artistic treatment but still primarily delivered sequences of diagrammatic statements or illustrations. The failure mode is repeated: animation of presentation is mistaken for dynamic visual reasoning. The user's key requirement is stronger: represent both things inside and outside time, and help users **represent, manipulate and discover** conceptual relationships.

The next experiment must directly test whether a visible operation can reveal something about a *timeless* relation without implying that the relation itself evolves in time.

## Distinguish three clocks

1. **Domain/ontological time:** Does the modeled process or entity change in its own world? May be absent.
2. **Presentation time:** When does a viewer see or attend to a part of the structure?
3. **Manipulation time:** When does the viewer change an instance, viewpoint, parameter, or representation to inspect invariants?

Visual movement need not signify a physical event in the depicted world. A continuous change of representation can expose an invariant relation; a historical change should have a distinctly modeled transition.

## Two-stage test — no polished film yet

### Stage A: Calibration on an uncontroversially atemporal formal truth

**Example:** The interior angles of a Euclidean triangle sum to 180 degrees for every valid triangle. As the viewer drags a vertex, the particular triangle changes but this relation remains true.

- Same semantic claim, three treatments: **best static explanation**, **passive reveal/animated slides**, **directly manipulable continuous visual construction**.
- Make angle measures and sum visible as a stable relation; optionally reconfigure copies of the angles into a straight angle. No gratuitous transitions, decorative star fields, or narrator-led slide sequence.
- Explicitly separate varying the triangle instance from changing a mathematical law.
- Viewer tasks: identify what changed and what stayed invariant; manipulate to test an edge case; predict the outcome before seeing it; explain whether the theorem was temporally created.
- Programmatic invariant checks should cover nondegenerate triangles; test near-degenerate cases for rendering clarity but do not claim the theorem extends to invalid zero-area triangles.
- Reuse the [visual-language](https://github.com/BrianMills2718/visual-language) repository's notation literacy and freeze-frame/static-comparison framework. Do not build a competing general renderer for this pilot.

**Why a math calibration?** We know which statements are true independently of artistic preference. The experiment can fail clearly.

### Stage B: Transfer to one coherent metaphysical source

**Candidate:** Plotinus' One, Intellect and Soul as a single source-scoped *atemporal dependence* account (primary text: *Enneads* V.1/V.2). Do not reinterpret it as a history of three objects being created in sequence merely because the viewer sees them sequentially.

- Use the same distinction between **domain time** and **presentation/manipulation time**, but do not import the triangle's exact pictures or assume metaphysical grounding is mathematically the same relation as an angle sum.
- Represent the account with supported names, analogical imagery, and artistic freedom.
- Ask whether a viewer can distinguish **unchanging grounding** from **temporal causal sequence** and whether exploration yields a meaningful question about dependence/source depletion.
- Document source interpretation separately from rendering and user reception. No claim that the animation proves Plotinus true.

## Predeclared comparison / decision gate

Run one small study with **at least six unfamiliar viewers** if recruitment is possible; otherwise explicitly report only a designer/internal pilot and withhold any audience-effectiveness claim.

Matched tasks compare a strong static representation, a passive animation, and a manipulable dynamic version. Record:
- correct identification of *what changes* versus *what remains fixed*;
- unintended temporal-causation or material-transfer readings;
- explanation/prediction task accuracy and response effort;
- genuinely new questions or distinctions prompted by manipulating the scene;
- whether the representation transfers at least one **semantic distinction** to Plotinus without forced equivalence.

**Pass for further research:** The interactive treatment produces a clear explanatory or reasoning advantage over the best static/slideshow alternative on at least one prespecified task, without a dominant false temporal reading; and Stage B preserves the domain/presentation-time distinction. Interpret six-person data only as a pilot, not general statistical proof.

**Revise once:** If Stage A is promising but Stage B fails through a specific repairable mapping, revise that mapping once and rerun a bounded comparison.

**Spike / narrow:** If a reasonable pilot cannot outperform a static representation at *any* specified reasoning task, or if even after one revision the cross-domain concept consistently requires labels that do all explanatory work, stop the *generative visual reasoning language* track. Preserve the **artistic lore film** track as a separate viable creative endeavor; do not pretend its aesthetic value validates a computational visual language.

**Do not merge success criteria:** Better art, clear diagrams, accurate theological research, and valid formal manipulation are four different accomplishments.

## Scope & effort cap

- One small math construction and one small metaphysical transfer case; no new upper ontology, rendering framework, polished 90-second film, or multi-tradition atlas.
- Reuse existing static/animation libraries, including Manim if it reduces effort, and existing `visual-language` principles.
- Maintain a single source-of-truth semantic specification and record interpretation risks.
- Do not claim a general-purpose grammar or return to Catholic trilogy until this gate is reviewed.

## Prior art

- [3Blue1Brown — linear transformations](https://www.3blue1brown.com/lessons/linear-transformations/) demonstrates dynamic inspection of mathematically fixed relationships.
- [Bret Victor — Media for Thinking the Unthinkable / Explorable Explanations](https://worrydream.com/) illustrates interactive representations as reasoning media.
- [Category-theoretic string-diagram reasoning](https://doi.org/10.1016/j.jlamp.2015.12.004) illustrates visually lawful manipulation of relations.
- [Visual Language experiments](https://github.com/BrianMills2718/visual-language/tree/main/experiments) already define strong static baselines and notation-literacy tests.

## Exit deliverables

1. Source-grounded explanation and treatment for both cases.
2. Usable controls for the manipulable construction and a matched static baseline.
3. Programmatic correctness tests for the mathematical example.
4. Evidence table of viewer interpretations and discovered questions (or an explicit "not tested").
5. Written go/no-go decision; no self-certification from an appealing rendering.
