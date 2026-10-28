# Film 006 — Catholic Creation and Providence

**The World That Is Continually Created** is an 84-second artistic interpretation of Catholic doctrine, centered on the tension between continual dependence on God and real creaturely activity. It intentionally stays with one recognizable living environment rather than displaying a sequence of diagrammatic slides.

- `catholic_creation_providence.mp4` — finished narrated-by-text, original-ambient-score film.
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