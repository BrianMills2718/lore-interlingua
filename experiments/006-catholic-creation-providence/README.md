# Film 006 — Catholic Creation and Providence

**The World That Is Continually Created** is an 84-second captioned, artistically interpreted animation of Catholic doctrine, centered on the coexistence of continuous dependence on God and genuine creaturely activity. It intentionally stays with one recognizable living environment rather than displaying a sequence of diagrammatic slides.

- `film-preview.mp4` — compact GitHub-friendly playback preview (640×360, 12 fps). The full 960×540 and 854×480 cuts are produced locally by the renderer; a higher-quality copy accompanies the chat delivery.
- `render.py` — procedural Python/Pillow/NumPy rendering, ffmpeg encoding, reproducible frame times.
- `contact-sheet.jpg` — representative storyboard frames.
- `treatment.md` — doctrinal source, story structure, artistic/semantic choices, limitations and future experiments.

## Render

Requires Python 3.11+, Pillow, NumPy and ffmpeg:

```bash
python render.py --preview
python render.py
```

This is **not** a mathematically derived, automatic visualization of Catholic teaching. Naturalistic and symbolic decisions are explicitly artistic. The content is grounded in [Catechism §§290–308](https://www.vatican.va/content/catechism/en/part_one/section_two/chapter_one/article_1/paragraph_4_the_creator.index.html).

Part of the [Lore Interlingua](https://github.com/BrianMills2718/lore-interlingua) research series.
## Limitations / next critique

This is a **first production cut**, not a proven universal visual language. It remains a restrained procedural botanical illustration, not fully illustrated character animation. The continued-sustenance layer is a proposed artistic metaphor with known risks: it might resemble a physical field or seem to arrive only mid-film because it is revealed then. The living landscape and transient water-flow marks are intentionally distinguished from that proposed metaphysical relation. No audience comprehension testing has been performed.

See [the production treatment](treatment.md), [semantic contract](scene-contract.json), and [deterministic local tests](test_film.py). The video has an original ambient soundtrack but **no spoken narration**; integrated captions carry the verbal claims.
