# Visual–Semantic Encyclopedia v0.1

**Status:** A usable but **provisional** visual-reasoning research atlas for [Lore Interlingua](../README.md), October 2026. It is not a settled philosophical upper ontology, a complete dictionary of metaphysical concepts, a production renderer, or a demonstrated shared visual language.

## Open the atlas

Open **[`index.html`](index.html)** in a modern desktop or mobile browser. The site is self-contained, runs without a server, internet access, or external JavaScript libraries, and has no analytics, user accounts, or server-side storage. External **source** and **project documentation** links open GitHub and therefore require a connection. The working atlas itself remains usable offline.

Explore the encyclopedia by searching entries, choosing navigation facets, or selecting any node in the relational atlas. Clicking a related concept opens its record. The selected record shows definitions, non-equivalences, exact source-corpus proposition text where available, visual hypotheses, and open research questions. The network graph displays **encyclopedia navigation relationships**, *not* metaphysical causal links or a map of reality.

Four distinct interactive studies illustrate visual reasoning tools:

- **Dependence vs. transfer:** reposition a dependent while a declared grounding relation persists; contrast this with an event showing a traveling packet. **These are different hypothetical relations**, not visual styles for the same physical mechanism.
- **Identity through deformation:** change the appearance of a labeled subject while keeping its referent marker, without claiming formal proof of metaphysical personal identity.
- **Constitutive part vs. group member:** compare composition with collection membership rather than treating all enclosures as the same relation.
- **Timeless relation vs. temporal event:** change a relation's **visibility** without changing its asserted existence, or construct a distinct hypothetical event where a link actually forms.

Other concepts deliberately share the nearest available **research sketch**, labeled as such. None has a guaranteed correct or canonical animation. Click **Animate** to move a slider; there is **no autoplay**. Motion is suppressed when the device has reduced-motion preference enabled.

The **Research notebook** prepares a copyable text note with the selected concept, demonstration mode, current parameter, and your observation. Notes remain in browser page memory while browsing; they are **not persisted**. Copy them manually before closing the page.

## Data model — one small navigation ontology

The canonical data is [`catalog.json`](catalog.json); [`catalog.js`](catalog.js) is a generated offline-friendly JavaScript wrapper. Rebuild with:

```bash
python scripts/build_encyclopedia.py
# or check that catalog.js is up to date:
python scripts/build_encyclopedia.py --check
```

Run these commands from the repository root. Tests run with the existing test suite:

```bash
python -m unittest discover -s tests -v
```

An **entry** has an ID, label, definition, editorial facets, important distinctions, typed relations to other entries, scoped example references, visual candidates and questions. Facets are for **navigation**, not a top-level claim that metaphysical kinds are disjoint. Relation types such as `contrasts` and `distinguishes` are **editorial semantic distinctions**, not theorem-proving logical connectives. This avoids importing a second ontology that conflicts with the existing [v0.2 interlingua](../docs/v0.2.md).

Every example links to an actual ID in the existing [v0.2 claim corpus](../data/v0.2.json) or the [Catholic source-scoped model](../research/catholic-world-model/v0.1.json). The statement is embedded for an offline *excerpt*; verify the primary source and full interpretive context before publishing a lore claim. In the catalog, an example records **how it is relevant to that entry**, never that all cited traditions agree with one another.

A **visual candidate** declares an intended mapping, important things it *does not assert*, experimental primitive references (drawn from the separate [`visual-language` project](https://github.com/BrianMills2718/visual-language/blob/main/catalog/primitives.yaml)), and a provisional status. The primitive references are non-executable pointers, **not** claims that `visual-language` currently provides a production-ready API, that the mark has been validated, or that a scene has been generated from v0.2.

## Editorial principles

1. **Source-relative meaning:** preserve which doctrine or model asserted a statement. A proposition appearing in an encyclopedia entry does not establish its truth in the external world.
2. **Distinctions first:** unities need not have physical parts, dependence need not be time-ordered, implication is not automatically causation, and participation is not the same as material transfer.
3. **Visual accountability:** every prominent mark in a research sketch needs a clear navigational, explanatory or artistic role. Decorative design is permitted but must not silently imply doctrine.
4. **Metaphorical surplus:** a luminous field or fluid can be evocative without literally being measurable matter. State the *selected correspondences* and the risks of a misleading dominant reading.
5. **No purity tests:** text, narration, religious iconography, character animation and 3D spatial models are welcome. The current sketches are *minimal research examples*, not the intended finished film style.
6. **Represent ↔ manipulate ↔ discover:** the editor should record questions a depiction exposes and improve the concepts, not merely produce images from a fixed schema.
7. **Preserve alternatives:** different visual metaphors may be useful backstage; a published film should still present one coherent lore account.

## Extending the encyclopedia

1. Choose **an actually needed** conceptual distinction from a source example or failed visual study; avoid speculative empty taxonomy.
2. Identify a concept's relation to the existing twelve entries. Use more than one facet when relevant.
3. Add an entry with a unique kebab-case ID, definition, distinguishing neighbors, source-scoped examples, mapping hypotheses, explicit non-claims, and a productive open question.
4. Point to known corpus IDs or to a source-specific record; do **not** manufacture a source claim to fill a category.
5. Rebuild `catalog.js` and run `tests/test_encyclopedia.py`. Test the browser interface with the offline document and keyboard controls.
6. Only **promote** a visual candidate after actual semantic and artistic work justifies reuse; this archive does not contain any accepted universal primitive.

## Known limitations and possible next work

- The map is curated and arranged for legible navigation. It is **not** calculated by logical subsumption or metaphysical distance.
- Crosslinks represent research relations; no OWL/RDF reasoner or upper ontology is installed. Adopting one should solve a concrete problem, not become a parallel project.
- The four demos are simplified and intentionally iconically sparse; they do **not** yet attain the Khutoryansky-style structural richness and mythic specificity desired in public films.
- Source citations are scoped repository IDs with embedded statements; not a substitute for reviewing primary texts or the specific translation choices.
- The encyclopedia's copyable notebook has no collaboration, file export or persistent storage.
- No viewer comprehension study has established that these sketches communicate the intended meaning to new viewers.

**Recommended next step:** add one **fully cast, tradition-specific visual scene** (e.g., Gurdjieff's organic-life mediation, which already exists as [Experiment 009](../experiments/009-cosmic-membrane/)) as an **embedded encyclopedia case**, linking its major marks, behaviors, source claims, and alternative art directions. Do not fabricate a generic renderer or hundreds of empty entries.

## Applied lore case 009 — Organic life as Earth’s cosmic membrane

The encyclopedia now has a **separate source-linked case library**: [`cases.json`](cases.json) is its editable record, [`cases.js`](cases.js) is the generated offline mirror, and [`cases-ui.js`](cases-ui.js) renders it beside the twelve existing concepts. No second upper ontology was invented, and the interlingua corpus remains canonical for the claim statements.

The first case ties **G02** (planetary mediation) and **G03** (differentiated radiation) to the animated marks of [Experiment 009](../experiments/009-cosmic-membrane/index.html). **G04** (the Moon’s nourishment) is explicitly **context only**: showing a moonward stream does not by itself depict that the Moon is maintained by it. This distinction matters more than merely collecting an attractive animation.

Use the **All visual marks / G02 / G03 / G04** selectors to inspect the mapping for every prominent visual element, including nonsemantic ornament and hidden diagnostic paths. The atlas links each of the relevant conceptual entries to the applied case, and clicking a case concept jumps back to its encyclopedia entry. The scene itself loads only on request, preserving its original interactive controls and source-specific captions. The shipped case HTML works offline; deeper source audits link to their canonical GitHub files and require an internet connection to open.

The **Research key** inside Experiment 009 is an optional diagnostic aid and is deliberately not a permanent film legend. This encyclopedia offers an extended semantic dictionary outside the audience-facing film, where it belongs.

To regenerate the independent case library's offline mirror:

```bash
python scripts/build_encyclopedia_cases.py
python scripts/build_encyclopedia_cases.py --check
python -m unittest discover -s tests -p 'test_encyclopedia_cases.py' -v
```

The atlas remains provisional: no viewer comprehension study, formally validated cross-tradition notation, or generic semantic-to-film compiler has been produced. Source claims are paraphrases scoped to Gurdjieff via Ouspensky. The third-party Gnostic reference film is **not** copied into this library.
