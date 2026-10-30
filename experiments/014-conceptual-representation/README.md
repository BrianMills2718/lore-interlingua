# Experiment 014 — Conceptual representation before the storyboard

**Status (2026-10-29):** working, *provisional* interactive concept view plus **two manual storyboard treatments** grounded in the original Experiment 014 model. This is not a film, a universal rendering engine, a tested teaching method, a validated notation, or an empirical evaluation of viewer comprehension.

**Purpose:** test whether a **single source-scoped concept model** can support distinct explanations while retaining the same relationships, then investigate **comprehension** and **reusable notation**. The model is upstream of the storyboard. A storyboard **linearizes** (orders the explanation of) that model; it does not create its metaphysical claims.

## Research question and boundaries

> Can one representation of organic-life mediation support both a source-first and an Earth-first explanation without changing the conceptual roles, and can viewers eventually understand and reuse the candidate conventions?

- **Lore scope:** Gurdjieff's organic-life interval as reported by P. D. Ouspensky; in the local corpus, claim **G02**. This is one claim, not a compressed version of all of Film 013.
- **Source:** Ouspensky, *In Search of the Miraculous*, discussion of organic life as a mediating link (often chapter 7; editions vary). The [Gurdjieff Foundation of Hawaii attributed excerpts](https://www.gurdjieff-hawaii.org/?page_id=160) include the grass-covered-field versus human-gathering comparison. [Corpus G02](../../data/v0.2.json), [Experiment 010](../010-living-intermediary/README.md), and [Film 013 audit](../013-living-interval/CONTINUITY_AND_EXPLANATION.md) are the local precedents. Source-linked wording is a reported *cosmological* claim, not independently verified physics or a new independent textual audit.
- **Exclusions:** G03 outgoing radiations, G04 lunar nourishment, Law-of-Three/Seven mechanics, an all-purpose interlingua, and physical simulation.
- **Experiment type:** research/specification with proposed visual relations, not an audience-facing public film.

## Three separate artifacts

| File | Authority within this experiment |
| --- | --- |
| [concept-model.json](concept-model.json) | Participants, concept facets, roles, source references, two differently typed relationships, requirements, nonclaims and the three kinds of time. **This is upstream of presentation.** |
| [notation.json](notation.json) | Five **candidate** visual correspondences for the model's three roles and two relationship types, with intended readings and explicit nonclaims. Conventions are not accepted or viewer-tested. |
| [presentations.json](presentations.json) | Two **explanatory traversals** referencing IDs in the unchanged model and notation; these encode reveal order, not source-world chronology. |
| [storyboard-treatments.json](storyboard-treatments.json) | Two **manual editorial storyboard treatments**: three shot beats per traversal, with framing, suggested presentation duration, caption, narration and explicit nonclaims. They are not rendered films. |
| [index.html](index.html) | An **offline interactive workbench**: whole-model view, source-first reveal, Earth-first reveal, participant inspector, notation audit and two treatments. |

**Open the workbench:** open [`index.html`](index.html) directly in a modern browser after downloading/cloning the repository. It needs no web server, npm, remote CDN or external scripts: [`study-data.js`](study-data.js) is generated from the four JSON records so `file://` access works. Use the mode controls and Previous/Next buttons to compare reveal order; inspect a participant to see its facets without changing the current storyboard beat. The graph is a conceptual relation, not a simulation. The page contains no autoplay and uses text alternatives to describe what is visible.

Regenerate/verify the **derived** offline browser bundle after changing a source record:

```sh
python scripts/build_experiment_014_study.py
python scripts/build_experiment_014_study.py --check
python -m unittest discover -s tests -p 'test_experiment_014_workbench.py' -v
```

These checks include a dependency-free Node interaction smoke test when Node is available. All browser presentation sources are inspected via static HTML/CSS/JavaScript; the tests are not evidence of viewer comprehension, accessibility certification or a visually polished film.

**Concept whole, then detail:** 'organic-life' remains a single concept with inspectable facets. Grassland and a gathering of people are examples within it, not obligatory atomic graph nodes. This avoids making the viewer reconstruct a whole concept from a pile of unrelated marks. It is a design hypothesis, not a claim that the subjective experience called 'thoughtfeel' has been independently validated as a teaching method.

## The invariant meaning

**Planetary world** —[reception]→ **organic life** —[mediation]→ **Earth**.

- **Reception:** planetary influences are received by organic life.
- **Mediation:** organic life mediates those influences toward Earth; the represented *mediated* relation requires the intermediary.
- **Not asserted:** that any drawn mark is a literal particle; that we know its speed, energy or physiology; that bare ground experiences no other forces; that different kinds of received influences are exactly two physical classes.

These are **two role-distinct relationships**, not an automatically conserved stream. A localized visual response may communicate participation, but it must not silently invent a physical transduction law. The relationship model records no numerical kinetics or chronology.

## Same model, two explanatory orders

| Traversal | Beat 1 | Beat 2 | Beat 3 |
| --- | --- | --- | --- |
| **Follow the influence** | Focus planetary world | Reveal reception at living subjects | Reveal mediation toward Earth |
| **Trace from Earth** | Focus Earth | Reveal its living intermediary | Trace back to the planetary source |

The same three concept anchors remain present in every beat. Each final beat makes both relationships available. The workbench implements **selective disclosure** without simulating a physical time course; the storyboard treatments add editorial framing and proposed words but do not alter the G02 model. **Reveal order is not domain-event order**: introducing Earth first does not mean Earth caused planetary influences; introducing a connection before its upstream source is a labeled conceptual relation, not an animation of a response preceding its cause. Source roles and claim IDs cannot be overridden inside a traversal.

## Notation and validation

The five mappings in [notation.json](notation.json) are deliberately modest: source, intermediary, recipient, reception, mediation. The crucial proposed distinction is that an incoming contact **ends at** a living participant, whereas an inward response **begins from** that participant toward Earth. Figurative art, sound and words remain legitimate; graphical similarity alone does not prove reusable meaning.

Run the built-in contract checks (Python 3.11+, no extra dependencies for this test):

    python -m unittest discover -s tests -p 'test_experiment_014.py' -v

These tests check ID resolution, the required role/relationship chain, notation coverage, and that the two traversals cover the same model despite different reveal orders. Regression cases intentionally corrupt a reference or relationship. **Passing tests does not validate the source interpretation, prove film generation, or establish comprehension.**

## Future manual study (not performed in this PR)

1. Explain the candidate signs with one example. Present each traversal with equivalent factual language and accessible captions; keep participant identities constant.
2. Ask unfamiliar participants to identify source/intermediary/recipient, explain why life matters, and distinguish reception from mediation. Collect unintended inferences about physical particles or automatic direct transmission.
3. Test **transfer** by presenting a second clearly framed, non-Gurdjieff mediation example using the same relationship conventions. Compare correct interpretation against confusing signs or labels. A second example must be separately justified, not assumed doctrinally equivalent.
4. Record whether the participant reconstructed the relations, not merely whether the animation looked appealing; revise any dominant misleading correspondence. An initial small formative sample can expose problems but cannot establish population-level effectiveness.

**Prototype delivery:** one inspectable view and two storyboard treatments now exist, reusing the same source-scoped data. What is **not yet established** is whether an unfamiliar viewer reconstructs the relation correctly or whether the notation transfers to a different, independently warranted example. Next, perform a formative comprehension and misreading study rather than increasing cinematic polish.

**Project alignment:** [Charter](../../docs/PROJECT_CHARTER.md) · [Current status](../../docs/PROJECT_STATUS.md) · [visual reasoning method](../../docs/visual-reasoning-instrument.md).
