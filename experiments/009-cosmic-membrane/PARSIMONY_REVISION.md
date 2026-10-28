# Experiment 009 — Semantic parsimony revision

**Status:** Current revised animation study. This supersedes the earlier temporary eSpeak narrated cut, which remains a historical artifact. The current 16-second preview uses embedded subtitles and **no synthetic speech**.

## Implementation

- **Removed by default:** all thin structural path curves from the displayed scene. Moving marks already make the directional relationships visible; the paths risk suggesting additional physical conduits. The research-only **Diagnostic paths** checkbox can reveal them for investigation.
- **Removed:** the inaccurate permanent bottom legend, which collapsed differently encoded outgoing streams into one gold marker.
- **Added:** optional, semantically matched **Research key**, outside the audience-facing Canvas. Cyan motes indicate incoming influences; light green motes indicate mediation toward Earth; gold dots, purple squares and blue rings represent radiation toward Moon, Sun and planetary sphere respectively. These are invented *visual coding choices*, not measured categories of radiation.
- **Added:** short source-scoped subtitles in the film Canvas, with optional checkbox control for exploratory studies.
- **Retained:** named principal entities and the heterogeneously branching organic envelope. Glows around celestial bodies are illustrative lighting, not extra metaphysical objects; background stars suggest cosmic setting. Their decorative role should not be mistaken for formal cosmic levels.
- **Retained selectively:** three orbital planetary sources as an illustrative plurality, not an assertion of exactly three planets or exactly three influences.

## Reason for every prominent mark

| Mark | Intended contribution |
| --- | --- |
| Earth | Terrestrial recipient of mediated influences |
| Branching living envelope | Organic life as diverse, receptive and radiative mediator |
| Three planetary bodies | Schematic plurality of planetary sources |
| Cyan moving points | Incoming planetary influences |
| Light green moving points | Mediation into Earth |
| Gold moving dots toward Moon | Radiation toward Moon |
| Purple moving squares toward Sun | Radiation toward Sun |
| Blue moving rings toward planets | Radiation toward planetary sphere |
| Background stars and moderate glows | Nonsemantic environmental depth and visual legibility |
| Subtitles | Explain the Gurdjieff/Ouspensky claim for a first-time viewer |

Any future new major visual feature should state **why it exists and what is lost if removed**. This is semantic parsimony, not a ban on artistic ornament.

## Verification

The local Playwright/Chromium rendering had no JavaScript exceptions. The paths checkbox defaults off; research-key toggle worked and remained outside the video Canvas. The rendered subtitle-only file has 192 frames at 12fps (16 seconds), H.264 video, and no audio stream. No audience study or metaphysical truth claim is made.

Run `python render_subtitled.py` after installing Playwright/Chromium and ffmpeg. See [narration and source audit](narration-and-audit.md). The previous eSpeak-based [renderer](render_narrated.py) is preserved only for historical reproduction, not recommended as an audience-facing default.
