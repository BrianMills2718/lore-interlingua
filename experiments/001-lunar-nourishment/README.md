# Visual Experiment 001 — The Earth as Transmitter

**Status:** first art-directed prototype; *not* evidence of a learned cross-domain notation or tested comprehension.

A 28-second, 1024×576, 24 fps animated explanation of Gurdjieff's account of organic life as a receptor of celestial influences and a source of differentiated radiations, including nourishment for the Moon.

## Build

Requires Python 3.10+, Pillow, NumPy, and `ffmpeg` on `PATH`.

```bash
python -m pip install pillow numpy
python experiments/001-lunar-nourishment/render.py \
  --out /tmp/visual-experiment-001.mp4 \
  --contact /tmp/visual-experiment-001-contact.jpg
```

Everything is procedural. The source does not require downloaded images, music, or fonts; it uses the system DejaVu Sans font.

## Source and semantic boundaries

- **Primary reading:** P. D. Ouspensky, *In Search of the Miraculous*, chapter 7, the discussion of organic life as Earth's organ of perception and radiation, plus related passages on the Moon.
- Supporting extract: https://www.gurdjieff-hawaii.org/?page_id=160
- **G02**: terrestrial organic life mediates planetary influences to Earth.
- **G03**: differentiated radiations are emitted toward the Sun, planets, and Moon.
- **G04**: the Moon depends on terrestrial organic life for nourishment.

`scene.json` binds these propositions to visual operations and distinguishes semantic claims from editorial choices.

## Four sequences

| Interval | Concept | Visual treatment |
|---|---|---|
| 0–3 s | Attribution | One opening disclaimer/title |
| 3–9 s | Reception | Transient cool pulses from celestial actors toward living Earth |
| 9–15 s | Mediation | Organic-life boundary brightens and receives influences |
| 15–22 s | Lunar nourishment | A distinct outgoing pattern directed to the Moon, with a restrained recipient response |
| 22–28 s | Differentiated radiations | Additional output patterns oriented toward the Sun and the planetary world |

## Visual-grammar candidates (not established standards)

- **Attached ring/marker:** a persistent system or medium with a localized role.
- **Directed moving pulses:** a transient influence or transfer event.
- **Boundary reception:** a medium that mediates rather than merely holds its input.
- **Different pulse shapes:** different asserted types of output, not a global color-code.
- **Recipient response:** indicates maintenance/dependence, not a measured physical process.

## Art direction versus semantics

Icons representing Sun/Earth/Moon, relative size, celestial layout, starfield, line curvature, typography, timing, pauses, palette, and moon-glow treatment were manually designed. They are **not derived** by a universal grammar from the data model.

This separation is deliberate. The formal model preserves the kind of relationship; an art-directed renderer communicates it, subject to safeguards against making unsupported claims.

## Current limitations and open tests

1. Pulses are naturally interpreted as **material particles** even though the input influence is not specified as literal corpuscles. Test a non-particle encoding.
2. The later output pulses have different shapes, but this convention is not yet learned or validated. Test unfamiliar domains.
3. The Moon's brightness increase may suggest rapid physical growth. Prefer an abstract maintenance cue in the next iteration.
4. Earth as a ring around a sphere compresses diverse living beings into one medium. Test scale/cross-section depictions.
5. Captions explain the meaning; the imagery's **independent intelligibility has not been tested**. A true notation test must compare captionless decoding to a static baseline.
6. Source evidence is secondhand (Ouspensky's report), not an independently verified physical mechanism.

## Next work

**Hold the visual grammar provisional.** Ask an unfamiliar viewer to decode a captionless clip and compare it with a static diagram; then apply the candidate `transient-transfer` convention to Bailey's Seven Rays or another non-material concept. Record failures and only promote conventions that survive cross-domain transfer.
