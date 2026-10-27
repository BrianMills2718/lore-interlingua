# Visual Experiment 002 — One Life, Seven Qualities

**Tradition:** Alice A. Bailey, *Esoteric Psychology I*  
**Scene:** 24 seconds · 1024×576 · 24 fps · silent animated explainer  
**Status:** rendered; static semantic contract tests pass; no independent comprehension testing.

## Research question

Can the conventions from Experiment 001 (Gurdjieff's lunar nourishment) be reused for Bailey's seven rays *without* falsely equating qualitative influence with transfer of material/substance?

## Grounding

- **B01 — differentiation:** one divine Life manifests through seven rays/builders. Bailey's narrative allows personification; the scene illustrates structural differentiation, not the rays' complete ontology.
- **B02 — partition:** Rays I–III are Rays of Aspect, Rays IV–VII are Rays of Attribute.
- **B03 — qualification:** ray energies qualify living forms; the render depicts qualitative properties within example forms rather than transferred particles.

Primary texts (Lucis Trust):

- [The Seven Rays Enumerated](https://www.lucistrust.org/online_books/esoteric_psychology_volume_i/section_one_chapter_introductory_remarks/3_the_seven_rays_enumerated)
- [Esoteric Psychology I](https://www.lucistrust.org/online_books/esoteric_psychology_volume_i)

## Composition and semantic audit

| Convention | 001: Gurdjieff | 002: Bailey | Status |
|---|---|---|---|
| Identity-bearing bounded marks | Earth, Sun, Moon | One Life, ray identities, examples of forms | **Reused** |
| Differentiated connections | Different recipients and radiations | Seven different qualifications | **Reused structurally**, not semantically equated |
| Transient moving markers | Directional energetic transfer | Omitted | **Not transferable** |
| Recipient response | Moon luminosity (illustrative nourishment) | Texture/properties within form | **Modified** |
| Persistent scope | Earth's organic-life boundary | Three/four group brackets | **Reused as scope** |
| Non-depleting source | Not encoded | One Life remains unchanged | **New candidate** |
| Discrete color distinctions | Editorial | Editorial | **Never promote to universal semantic correspondence** |

**Critical limitation:** the lines from One Life to the seven rays introduce sequentially *for pedagogy*. Their temporal ordering should not imply metaphysical chronology or a physical division of substances. The rays' pattern signatures are experimental design decisions, not historical correspondences identified by Bailey.

The three sample forms are generic; they are not a claim that each human being has exactly one ray. The film is an explanatory illustration, **not yet a validated visual notation**. It needs captionless and static-baseline tests.

## Reproduce

From the repository root, install Pillow, NumPy and FFmpeg, then:

```bash
python experiments/002-seven-rays/render.py \
  --out /tmp/bailey-seven-rays.mp4 --contact /tmp/bailey-seven-rays.jpg
python -m unittest discover -s experiments/002-seven-rays -p 'test_*.py'
```

`scene.json` is the semantically tagged scene manifest. `render.py` is an art-directed renderer, **not** a generic interlingua-to-video compiler. The output is deterministic given the fonts, Pillow version, and FFmpeg encoder.

## Next gate

After comparing 001 and 002, build a deliberately **atemporal** grounding scene for Plotinus. Test whether viewers distinguish influence, transfer, differentiation, and existential grounding. Only consider promoting a shared visual primitive after captionless decoding across these cases.
