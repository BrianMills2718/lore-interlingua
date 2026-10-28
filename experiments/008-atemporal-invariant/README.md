# Experiment 008 — Atemporal invariant calibration

> **Historical/provisional record.** This file retains earlier examples and proposed next steps; current project decisions are in [Project Charter](../../docs/PROJECT_CHARTER.md), [Current State](../../docs/PROJECT_STATUS.md), and [Experiment Registry](../../docs/EXPERIMENT_REGISTRY.md). Do not treat a past "gate" as a program-level stop rule.


**Status: first playable probe, NOT a validated visual grammar or proof of metaphysical translation.**

[Open the local interactive construction](index.html) in a browser (after downloading or cloning the repository). It uses only local HTML/CSS/SVG/JavaScript, with no dependencies.

## What is being tested?

We separate **domain time**, **presentation time**, and **manipulation time**. The interior-angle sum of a nondegenerate Euclidean triangle is always 180° (a timeless mathematical relation). Dragging one triangle's vertex *changes the represented instance*, not that invariant rule. Revealing the angle total is a change in presentation; interacting with the triangle occurs in manipulation time. No mathematical law "develops" merely because the display animates or responds.

The prototype draws three color-coded angle wedges and assembles their magnitudes into a single 180° bar. The user can drag the apex, use sliders, hide labels, and reveal/hide the answer. No scene transitions and no unsupported labels about God, emanation, or cosmic energy.

**There is also a static baseline** described alongside the construction. A future controlled comparison should make its static visual treatment equally polished, not just plain text.

## Why this case?

- It is simple enough to specify a correct relation and programmatically check the geometry.
- It lets us test the separation between representing a process and using a temporal process to *explore* a non-temporal rule.
- It does **not** by itself show that motion is superior to a static Euclidean proof, or that the technique transfers to Plotinus or Catholic eternity.

## Local verification already performed

- Chromium/Playwright smoke test: toggled reveal, hid labels, changed both sliders, and rendered an intact page; **no JavaScript exceptions**.
- For a 5 × 4 grid of nondegenerate triangle positions, the browser's directly calculated angle sum differed from 180° by at most **2.85 × 10⁻¹⁴ degrees** due to floating-point rounding.
- This is program correctness, **not a human comprehension result**.
- No unfamiliar viewers have been tested; no gain versus an equally developed static baseline has been demonstrated.

## Optional diagnostic tasks — original gate superseded

1. Show a viewer the static diagram and the manipulable version, matched for visual clarity.
2. Ask what changes and what stays invariant; allow an unfamiliar viewer to predict before revealing the sum.
3. Record whether scrubbing/manipulation prompts an insight that the static visual did not, or whether it merely adds motion and attention cost.
4. Only then attempt the distinct source-scoped Plotinian **atemporal grounding** case. Do not equate mathematical angle invariance with metaphysical dependence.
5. Interpret results as evidence about this **particular construction**. The old benchmark-based kill gate has been withdrawn: see the [revised first-principles appraisal](../../research/atemporal-visual-reasoning-gate.md). Neither successful nor unsuccessful triangle animation decides the viability of visualizing metaphysical concepts.

This prototype is deliberately an *internal mathematical calibration*, not a lore film; the one-coherent-lore requirement governs public lore films, not research instruments.
