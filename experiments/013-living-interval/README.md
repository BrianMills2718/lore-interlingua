# Experiment 013 — The Living Interval: One Connected Cosmology

**Primary deliverable:** 176-second continuous **MP4**, 1280×720, 24 fps, original stereo score, readable burned-in English captions; a smaller directly playable preview is also provided.

**Scope:** Gurdjieff's Ray of Creation and the organic-life interval as recorded by P. D. Ouspensky. The film combines structural content retained from [Experiment 012](../012-ray-of-creation/README.md) and living-world relationships retained from [Experiment 011](../011-sensitive-earth/README.md). It is **not** a replay or simple concatenation of either film.

## The integrated narrative

1. Begin with **all seven orders** visible in one persistent world. Select a Ray through the Absolute, All Worlds, All Suns, Sun, Planets, Earth and Moon, showing **1, 3, 6, 12, 24, 48, 96** orders of laws.
2. The **Law of Three** is explicitly named with active, passive and neutralizing forces; the temporary motion shows three relational roles, not substances.
3. Increase the visible constraint of a common recurrent motion motif while descending through the Ray. These curves are not individual laws or quantitative cosmological measurements.
4. Identify the **Law-of-Seven interval** between planetary world and Earth as a structural interruption in the cosmic octave. This is not a missing physical distance.
5. Move into Earth's visible living surface. Grass, plants, an animal and a gathering of people receive *planetary influences*, and local mediated responses move toward Earth from the living intermediary.
6. Pull back to show living Earth within the same selected Ray while **differentiated radiation** goes to Sun, planets and Moon. The three symbol styles represent qualitative differences without claiming detailed physical radiation types or proving lunar nourishment.
7. Reveal the wider persistent Ray again; the viewer has not watched seven successive acts of astronomical creation.

## Reproducible production

Files: `film.html` (offline stand-alone source/interactive scrubber), `earth_texture.jpg` (source-provenance image also embedded in HTML), `make_score.py` (original ambient score), `render.py` (deterministic browser-frame / ffmpeg pipeline), `build_film.py` (cumulative art-direction rebuild from 012), `captions.srt` (explanations for future narration), `scene-contract.json`, `CONTINUITY_AND_EXPLANATION.md`, and `test_film.py`.

Install Python modules `playwright`, `numpy`, `scipy`, `soundfile`, and local `chromium` / `ffmpeg`. From this directory:

```bash
python make_score.py
python render.py
```

For developmental changes from the previous film, run `python build_film.py` first. The build script reads `../012-ray-of-creation/film.html`. It preserves its scene/camera/texture environment and changes it through source-scoped additions. No network requests are needed for rendering. Generated full-resolution MP4s need not be tracked by Git because they are reproducible; a small review MP4 is tracked for direct GitHub access.

To validate contract and source structure:

```bash
python test_film.py
```

## Research status

This film is an **art-directed source-scoped prototype**, not empirical astrophysics, established universal visual notation, or a generic engine. See [continuity and explanatory audit](CONTINUITY_AND_EXPLANATION.md) for what is explained, what remains source-unknown, and what still needs better visual expression. The [cumulative imagery index](../../encyclopedia/imagery.html) documents what this film keeps and extends.
