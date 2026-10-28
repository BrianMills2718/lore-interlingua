# Experiment 009 — Are three symbols three different processes?

**Status:** Source-and-implementation audit, 2026-10-28. [Open the interactive study](009-encoding-audit.html) or read the [structured record](009-encoding-audit.json). The study is an internal design probe, **not** a second competing interpretation of Gurdjieff, a viewer-comprehension test or a source claim about measurable radiations.

## Precise question

Do the three distinct outgoing moving glyphs in Experiment 009 convey substantively different **relations/mechanisms**, or do they chiefly identify **different destinations** and nominal categories of radiation?

The source (Ouspensky reporting Gurdjieff) says that organic life on Earth receives planetary influences, transmits them toward Earth, and emits kinds of radiations required differently by the Sun, planets and Moon. It **does assert a difference in kind**, not simply three destinations. However, it does *not* identify wavelengths, speeds, particle shapes, propagation laws, conversion ratios or independently specified destination responses. See [Ouspensky's text](https://www.globalgreyebooks.com/online-ebooks/p-d-ouspensky_in-search-of-the-miraculous_complete-text.html), in the organic-life section, and [attributed excerpts](https://www.gurdjieff-hawaii.org/?page_id=160).

## Source-versus-renderer audit

| Source-bound claim | Existing visual implementation | Judgment |
| --- | --- | --- |
| **G02:** the planetary world acts on living organisms, which mediate influence to Earth | Cyan moving motes approach the living envelope; pale-green moving motes move inward toward Earth | **Two role-distinct relations**, but rendered with the same moving-dot idiom; detailed mediation not shown |
| **G03:** organic life emits different kinds of radiation toward Sun, planets and Moon | Three families of traveling markers follow curved trajectories from the living envelope to named recipients | **Recipient-directed categories** are visible; differentiated mechanisms are **not** |
| **G04:** Moon is supported by nourishment associated with organic life | Gold motes reach the Moon | **Context only.** Arrival is not the same as ongoing sustenance or maintenance |

The [original renderer](../../experiments/009-cosmic-membrane/index.html) uses one shared shape-travel operation for all outgoing streams. Its outgoing array specifies:

| Recipient | Graphic category | Programmed rate (path fraction per second) | Source warrant |
| --- | --- | --- | --- |
| Moon | Gold dots | 0.095 | Distinct recipient and kind, **not** glyph or speed |
| Sun | Purple squares | 0.067 | Distinct recipient and kind, **not** glyph or speed |
| Planetary world | Blue rings | 0.083 | Distinct recipient class and kind, **not** glyph or speed |

The code changes color, symbol, destination, and procedural movement rates while leaving the underlying operation—a repeated marker moving along a quadratic path—effectively unchanged. Different speed settings are presentation choices with no identified doctrinal counterpart.

## Three operations in the interactive study

1. **Original marks:** three distinguishable markers go to three recipients. This conveys the categorical claim in G03 but not three distinct causal processes.
2. **Uniform marks:** all three output glyphs become the same. Source, direction and recipients remain. **What disappears is the visible categorical difference**; the labels or narration can still state it. This isolates the graphic's real contribution.
3. **Swapped marks:** permute colors/shapes among recipients without changing source identity, destination roles or source assertions. If a drawing changes while the doctrine does not, the chosen glyph-to-recipient assignment is *conventional*. This does **not** imply the source's differentiation itself is arbitrary.

A further independent control **equalizes movement rates**. The source never claimed specific speeds, so normalizing them does not discard a sourced quantitative distinction. The G02 checkbox keeps the separate reception/mediation roles visible for contrast with G03.

These are **semantic counterfactuals on visual encodings**, not alternative worldviews within a public lore film. They reveal which properties of the marks carry information by construction. They do not measure what any unfamiliar viewer actually understands.

## Conclusions

- **Represented successfully:** one outgoing relation from organic life to several recipient classes; G03's qualitative differentiation through a conventional visual code.
- **Not represented:** a named mechanism for each kind, a physical transfer law, a functional account of receiver-specific requirements, or Moon maintenance from G04.
- **Potential misleading surplus:** unsourced differences in apparent speeds. Since every kind travels identically otherwise, a viewer may infer a fictitious three-part physical taxonomy.
- **Cross-claim weakness:** G02 (reception/mediation) and G03 (radiation) use similarly traveling motes even though their source-described roles differ. A better visual form for the *organic mediation* is worth investigating.

## Recommended design action

Retain the fact that radiations are **differentiated**. Treat color/shape as an openly provisional *nominal visual code* rather than three kinds of physical particles. Standardize output rates unless an explicitly artistic rhythm is useful and unlikely to imply source facts. Develop G02's **local differences in organic reception**: the source specifically contrasts grassy fields and gatherings of people receiving different influences. That gives us better source support for meaningful behavior at the living envelope. Avoid inventing receiver-specific physical absorption, Sun/Moon metabolism or lunar-maintenance effects unless separately grounded in the tradition and clearly cast.

In the next production treatment, consider whether the scene truly requires particle-like images at all. The visual language should be allowed to use organic, iconic or continuous-field analogies without implying that metaphorical physics has been demonstrated.

## Preservation of uncertainty

An art-directed film may remain evocative and nonliteral. **Parsimony does not mean every visible feature must be a formal proposition.** It means prominent features have accountable conceptual, explanatory or artistic reasons. This audit is also **not a benchmark-based go/no-go gate** for the broader project. Viewer interpretation and the existence of a reusable cross-tradition visual grammar remain untested.
