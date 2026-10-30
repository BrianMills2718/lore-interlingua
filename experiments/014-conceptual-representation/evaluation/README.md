# Experiment 014 — Formative comprehension and notation-transfer protocol

**Status (2026-10-29):** A **ready-to-administer research instrument and analysis rubric**, *not* a completed human-participant study. No user observations, learning effects or notation-transfer findings are asserted.

## Purpose

Experiment 014 has one source-scoped model of Gurdjieff's organic-life mediation (G02), two ways to disclose it and five **candidate** visual correspondences. This follow-on protocol evaluates two **different outcomes**:

1. **Concept comprehension:** Can an unfamiliar viewer reconstruct the intended planetary world → organic life → Earth relation, distinguish reception from mediation, and avoid falsely asserting measured physical mechanisms?
2. **Learned notation transfer:** After instruction, can a viewer assign the *dashed reception* versus *solid mediation* convention correctly to a structurally related but unrelated **hypothetical** case whose participants are differently named and arranged?

The transfer diagram uses **Nara → Ivo → Selen** as an invented speaker/interpreter/listener scenario. It is a device for testing *sign interpretation*, **not** an interpretation of Gurdjieff, a source fact, or evidence that human translation and the cosmological relation operate by the same mechanism. The task reverses the left–right placement compared with the G02 workbench. Labels reveal arbitrary names, **not** relation roles.

## What to open

- [Participant assessment](index.html) — standalone, offline-friendly HTML/JS; no accounts, analytics, remote services or automatic response transmission.
- [Experiment 014 teaching/workbench view](../index.html) — concept overview, source-first and Earth-first disclosure. The assessment links to the chosen treatment with a `?mode=` query; the workbench preselects that explanation mode when opened. Because its mode controls remain accessible, the facilitator should instruct participants not to switch.
- [Model](../concept-model.json) · [notation](../notation.json) · [explanatory traversals](../presentations.json) · [storyboard treatments](../storyboard-treatments.json).

The study instrument is deliberately **separate** from the upstream conceptual model, notation and storyboard. Answer keys belong in the evaluator's analysis script, not in the participant's graphical legend or transferred-case diagram.

## Suggested administration (formative, not an efficacy trial)

1. **Recruit unfamiliar adults on a voluntary basis** and avoid collecting names, email addresses, credentials or health details. An initial **8–12 participants** can help identify misunderstandings; it cannot establish generalizable learning effects.
2. **Alternate the assigned exposition**: for participant 1 use *source-first* (`follow-influence`), for participant 2 use *Earth-first* (`trace-from-earth`), and so on. Record the assigned condition but do **not** interpret differences as causal proof with this small, uncontrolled design.
3. Ask each participant to read the assigned three beats of the workbench **once**. Both conditions use the same conceptual world and the same notation; only explanatory order differs. The participant declares completion in the assessment; the form does not independently verify exposure or prevent revisiting tabs. Avoid switching presentation modes during the assigned exposition.
4. Have the participant answer **three closed comprehension questions plus one open reconstruction**. On the form, these responses are locked before the transfer diagram appears.
5. Without re-opening the legend, present the **right-to-left transfer diagram** showing Nara, Ivo and Selen, with a dashed and a solid connection but **without labeling the relation types**. Have the participant answer four closed transfer questions and an optional open ambiguity/misreading question.
6. Use **Finish → Download JSON** to save an anonymous local response record. The form sends no answers to a server and does not use localStorage. If the participant does not wish to share, do not collect the file.
7. Score closed answers offline with `score_results.py`; **manually code the open-ended reconstruction** using the rubric below. Keep anonymous raw responses under appropriate access control outside this repository. Do not upload participant files to this public repo.

**No forced consent, artificial duration, or hidden surveillance is implemented.** Participants may leave or skip a question at any time. Because the lesson has a visible mode switch and answers are self-reported, the present tool supports **diagnostic interviewing**, not blinded randomized experimentation.

## Predeclared closed-item answer key

| Item | Correct answer (internal code) | Intended construct |
| --- | --- | --- |
| C1 | `planet_life_earth` | Reconstruct G02's source/intermediary/recipient chain |
| C2 | `mediated_relation_unavailable` | Distinguish an absent intermediary *within the represented relation* from an absolute claim about all natural forces |
| C3 | `no_physical_mechanism` | Distinguish symbolic relations from asserted wavelengths/particles/speeds |
| T1 | `dashed_nara_ivo` | Recognize the **reception** convention on a novel arrangement |
| T2 | `solid_ivo_selen` | Recognize the **mediation** convention |
| T3 | `ivo` | Identify the intermediary after the physical layout is reversed |
| T4 | `no_universal_mechanism` | Respect limits on what the marks assert in the changed case |

**No feedback or answer key is shown to participants** before exporting. The evaluator can run:

```bash
python experiments/014-conceptual-representation/evaluation/score_results.py anonymous-response.json
```

Scores are **separate**: comprehension closed 0–3 and notation-transfer closed 0–4, each with an *answered count* to distinguish omissions. An omitted answer is not silently imputed as correct; `score_results.py` also reports the number missing. Use descriptive error categories rather than arbitrary pass/fail cutoffs. An answer of `unsure` is a valid recorded response, not evidence of poor engagement.

## Open reconstruction rubric (manual, 0–2)

- **0:** No intelligible relationship or a materially inverted claim (e.g. organic life originates all planetary influence).
- **1:** Correct participant identities or one directed relation, but not a coherent account of **both reception and mediation**.
- **2:** Identifies a planetary source, organic-life reception/mediation, and Earth as recipient in their correct directions, **without claiming an established physical conversion mechanism**.

Code material misinterpretations separately: **direct-bypass**, **source-reversal**, **decorative-life**, **literal-particles**, **quantified-physics**, **universal-no-forces**, and **presentation-is-world-time**. Multiple codes may apply. A second independent coder can resolve ambiguous answers by discussion; preserve the original response and reasoning. Do not pretend the numeric 0–2 coding measures a person's internal “thoughtfeel.”

## Interpretation and design limitations

- These questions **cannot demonstrate** notation causes better learning than prose. There is **no text-only or untrained control group** and the source case is unfamiliar metaphysical content. The hypothetical transfer case has a clear arrow structure, so performance can reflect ordinary arrow literacy; shape-specific T1/T2 answers are therefore more relevant to learned mapping than the participant-role T3.
- The two variants share the same material and differ in **reveal order**, but participant self-pacing, choice of other workbench controls, exposure time and prior knowledge are uncontrolled.
- Using one hypothetical transfer case supports at most **local recognition after instruction**. It does not establish a universal notation, long-term retention or cross-tradition philosophical equivalence.
- If participants routinely confuse the dashed versus solid relations, mistake the intermediary for decoration, or infer exact cosmic physics, revise the candidate notation or its explanation before producing another film.
- Report **counts and individual error patterns**, not scientific claims about cognition, astrophysics, general efficacy, or the project's viability. Register future hypotheses and stronger comparison designs before deploying new participant-facing versions.

## Privacy and reproducibility

The browser app does **not** send responses through fetch, XHR, forms with a network action, cookies, or analytics. It does not save progress between page loads. Output is generated only when the participant requests a copy or file; no identifiers or time stamps are required. External links in the teaching workbench may open source/reference pages, which have their own privacy practices. The GitHub Pages host itself may keep ordinary infrastructure logs, which this instrument does not control.

The score script uses only Python's standard library. Regression tests verify question IDs, answer-key consistency, omission handling, the reverse-layout transfer diagram's text description, and local-only export behavior. Passing tests establish **tool consistency**, not construct validity or audience comprehension.
