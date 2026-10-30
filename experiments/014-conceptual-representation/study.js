/* Experiment 014 · A small, non-rendering inspection interface.
 * The upstream semantics come only from the generated, source-scoped data bundle.
 * The drawings are candidate notation; no claim of measured cosmic mechanism.
 */
(function () {
  "use strict";

  const data = window.LI_EXPERIMENT_014;
  const pageError = document.querySelector("#storyboard-list");
  if (!data || !data.model || !data.notation || !data.presentations || !data.storyboards) {
    if (pageError) pageError.textContent = "Unable to load the offline study data. Keep study-data.js beside index.html.";
    return;
  }

  const model = data.model;
  const byConcept = new Map(model.concepts.map(function (item) { return [item.id, item]; }));
  const byRelation = new Map(model.relationships.map(function (item) { return [item.id, item]; }));
  const variants = new Map(data.presentations.variants.map(function (item) { return [item.id, item]; }));
  const treatments = new Map(data.storyboards.treatments.map(function (item) { return [item.id, item]; }));

  const state = { mode: "overview", step: 0, focus: "organic-life" };
  const $ = function (selector) { return document.querySelector(selector); };
  const $$ = function (selector) { return Array.from(document.querySelectorAll(selector)); };
  const overviewText = "The whole model is visible. Planetary influences are received by organic life, which mediates their relation toward Earth. Inspect a concept or choose an explanatory order.";
  const relationText = {
    reception: "Reception: planetary influences are received by organic life (dashed indication).",
    mediation: "Mediation: organic life mediates those influences toward Earth (solid indication)."
  };

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function activePresentation() {
    return state.mode === "overview" ? null : variants.get(state.mode);
  }

  function activeStep() {
    const presentation = activePresentation();
    return presentation ? presentation.steps[state.step] : null;
  }

  function visibleRelations() {
    const step = activeStep();
    return step ? step.visible_relationships : model.relationships.map(function (r) { return r.id; });
  }

  function inspect(id) {
    if (!byConcept.has(id)) return;
    state.focus = id;
    draw();
  }

  function selectMode(id) {
    if (id !== "overview" && !variants.has(id)) return;
    state.mode = id;
    state.step = 0;
    const step = activeStep();
    state.focus = step ? step.focus : "organic-life";
    draw();
  }

  function changeStep(delta) {
    const presentation = activePresentation();
    if (!presentation) return;
    const next = state.step + delta;
    if (next < 0 || next >= presentation.steps.length) return;
    state.step = next;
    state.focus = presentation.steps[next].focus;
    draw();
  }

  function writeInspector() {
    const concept = byConcept.get(state.focus);
    if (!concept) return;
    $("#focus-role").textContent = concept.role.toUpperCase();
    $("#focus-name").textContent = concept.label;
    const area = $("#focus-facets");
    const items = element("ul");
    concept.facets.forEach(function (facet) {
      items.appendChild(element("li", null, facet));
    });
    area.replaceChildren(items);
    if (concept.example_variations && concept.example_variations.length) {
      area.appendChild(element("p", "example-detail", "Inspectable examples: " + concept.example_variations.join(" · ")));
      area.appendChild(element("p", "example-detail", concept.variation_limit));
    }
    $$("[data-inspect]").forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.inspect === state.focus));
    });
    model.concepts.forEach(function (item) {
      const group = document.getElementById("concept-" + item.id);
      if (group) group.classList.toggle("is-selected", item.id === state.focus);
    });
  }

  function drawRelations() {
    const revealed = new Set(visibleRelations());
    model.relationships.forEach(function (relation) {
      const group = document.getElementById("relation-" + relation.id);
      if (group) group.classList.toggle("is-visible", revealed.has(relation.id));
    });

    const summary = model.relationships
      .filter(function (relation) { return revealed.has(relation.id); })
      .map(function (relation) { return relationText[relation.id] || (relation.source + " → " + relation.target); });
    $("#relation-summary").textContent = summary.length
      ? summary.join(" ")
      : "No relationship has been disclosed yet. All three participants remain present; hidden lines are not absent from the model.";

    const text = "Three persistent participants: planetary world (source), organic life (intermediary), and Earth (recipient). " +
      (summary.length ? summary.join(" ") : "The explanatory sequence has not yet revealed a relationship.") +
      " These are conceptual relationships, not measurable physical transmissions.";
    $("#visual-description").textContent = text;
  }

  function drawStep() {
    const presentation = activePresentation();
    const step = activeStep();
    $("#previous-step").disabled = !step || state.step === 0;
    $("#next-step").disabled = !step || state.step >= presentation.steps.length - 1;
    $$("#main [data-mode]").forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.mode === state.mode));
    });

    if (!step) {
      $("#beat-label").textContent = "Concept overview";
      $("#explanation-heading").textContent = "The whole relation";
      $("#step-explanation").textContent = overviewText;
      $("#sequence-status").textContent = "Both relations are visible";
    } else {
      const treatment = treatments.get(presentation.id);
      const shot = treatment ? treatment.shots[state.step] : null;
      $("#beat-label").textContent = "Beat " + (state.step + 1) + " / " + presentation.steps.length;
      $("#explanation-heading").textContent = presentation.title;
      $("#step-explanation").textContent = step.intent +
        (shot ? " " + shot.narration + " This treatment is a reveal order, not the chronology of a physical event." : "");
      $("#sequence-status").textContent = "Presentation beat " + (state.step + 1) + " of " + presentation.steps.length;
    }

    $$("[data-shot]").forEach(function (card) {
      const active = !!step && card.dataset.variant === state.mode &&
        Number(card.dataset.beat) === step.order;
      card.classList.toggle("is-current", active);
      if (active) card.setAttribute("aria-current", "step");
      else card.removeAttribute("aria-current");
    });
  }

  function draw() {
    writeInspector();
    drawRelations();
    drawStep();
  }

  function addCardLine(target, className, name, value) {
    const text = element("p", className);
    const label = element("strong", null, name + " ");
    text.appendChild(label);
    text.appendChild(document.createTextNode(value));
    target.appendChild(text);
  }

  function renderStoryboards() {
    const area = $("#storyboard-list");
    const sections = data.storyboards.treatments.map(function (treatment) {
      const article = element("article", "treatment");
      article.appendChild(element("h3", "treatment-title", treatment.title));
      article.appendChild(element("p", "treatment-order", "Three manually authored beats · suggested durations are presentation time only"));
      const list = element("ol");
      treatment.shots.forEach(function (shot) {
        const card = element("li", "shot-card");
        card.dataset.shot = shot.id;
        card.dataset.variant = treatment.id;
        card.dataset.beat = String(shot.beat);
        const heading = element("div", "shot-heading");
        heading.appendChild(element("span", null, "SHOT " + shot.id + " · BEAT " + shot.beat));
        heading.appendChild(element("span", "time", String(shot.suggested_seconds) + " seconds"));
        card.appendChild(heading);
        card.appendChild(element("p", "shot-caption", shot.caption));
        addCardLine(card, "shot-framing", "Frame:", shot.framing);
        addCardLine(card, "shot-voice", "Words:", shot.narration);
        addCardLine(card, "shot-limit", "Does not assert:", shot.nonclaim);
        list.appendChild(card);
      });
      article.appendChild(list);
      return article;
    });
    area.replaceChildren.apply(area, sections);
  }

  function renderAudit() {
    const key = $("#notation-list");
    const mappings = data.notation.mappings.map(function (mapping) {
      const row = element("div");
      row.appendChild(element("dt", null, mapping.id.replace(/-/g, " ")));
      row.appendChild(element("dd", null, mapping.intended_meaning));
      row.appendChild(element("dd", null, "Not asserted: " + mapping.not_asserted.join("; ") + "."));
      return row;
    });
    key.replaceChildren.apply(key, mappings);
    const limits = $("#interpretive-limits");
    limits.replaceChildren.apply(limits, model.interpretive_limits.map(function (limit) {
      return element("li", null, limit);
    }));
    const sources = $("#source-links");
    const links = model.sources.map(function (source, i) {
      const a = element("a", null, source.work);
      a.href = source.url;
      a.rel = "noopener noreferrer";
      a.target = "_blank";
      return [a, i < model.sources.length - 1 ? document.createTextNode("; ") : null];
    }).flat().filter(Boolean);
    sources.replaceChildren.apply(sources, links);
  }

  $$("[data-mode]").forEach(function (button) {
    button.addEventListener("click", function () { selectMode(button.dataset.mode); });
  });
  $$("[data-inspect]").forEach(function (button) {
    button.addEventListener("click", function () { inspect(button.dataset.inspect); });
  });
  $("#previous-step").addEventListener("click", function () { changeStep(-1); });
  $("#next-step").addEventListener("click", function () { changeStep(1); });

  renderStoryboards();
  renderAudit();
  // Optional entry-mode parameter for the standalone formative study.
  // This selects an explanatory order; it never changes the source model.
  const requestedMode = /(?:\\?|&)mode=(follow-influence|trace-from-earth)(?:&|$)/
    .exec((window.location && window.location.search) || "");
  if (requestedMode) selectMode(requestedMode[1]);
  else draw();
}());
