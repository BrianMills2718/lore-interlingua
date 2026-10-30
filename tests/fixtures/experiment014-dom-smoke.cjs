/* Dependency-free interaction smoke test for the Experiment 014 DOM logic.
 * This is a fake DOM for state transitions; it is NOT a browser visual/a11y audit.
 */
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const root = path.resolve(__dirname, "../..");
const study = path.join(root, "experiments", "014-conceptual-representation");

class Node {
  constructor(tag) {
    this.tag = tag;
    this.dataset = {};
    this.attributes = {};
    this.children = [];
    this.listeners = {};
    this.disabled = false;
    this._text = "";
    this.classes = new Set();
    this.classList = {
      toggle: (name, active) => {
        if (active) this.classes.add(name);
        else this.classes.delete(name);
      },
      contains: name => this.classes.has(name)
    };
  }
  set textContent(value) {
    this._text = String(value);
    this.children = [];
  }
  get textContent() {
    return this._text || this.children.map(child => child.textContent).join("");
  }
  appendChild(child) { this.children.push(child); return child; }
  replaceChildren(...children) { this.children = children; this._text = ""; }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  removeAttribute(name) { delete this.attributes[name]; }
  addEventListener(name, callback) { this.listeners[name] = callback; }
  click() {
    if (!this.disabled) {
      assert.equal(typeof this.listeners.click, "function", this.tag + " needs a click handler");
      this.listeners.click();
    }
  }
}

const ids = new Map();
function get(id) {
  if (!ids.has(id)) ids.set(id, new Node(id));
  return ids.get(id);
}
[
  "storyboard-list", "focus-role", "focus-name", "focus-facets",
  "relation-summary", "visual-description", "previous-step", "next-step",
  "beat-label", "explanation-heading", "step-explanation", "sequence-status",
  "notation-list", "interpretive-limits", "source-links",
  "concept-planetary-world", "concept-organic-life", "concept-earth",
  "relation-reception", "relation-mediation"
].forEach(get);

const modes = ["overview", "follow-influence", "trace-from-earth"].map(mode => {
  const button = new Node("button");
  button.dataset.mode = mode;
  return button;
});
const inspectors = ["planetary-world", "organic-life", "earth"].map(id => {
  const button = new Node("button");
  button.dataset.inspect = id;
  return button;
});
const document = {
  querySelector(selector) {
    assert.ok(selector.startsWith("#"), "Unexpected single selector " + selector);
    return get(selector.slice(1));
  },
  querySelectorAll(selector) {
    if (selector === "[data-mode]" || selector === "#main [data-mode]") return modes;
    if (selector === "[data-inspect]") return inspectors;
    if (selector === "[data-shot]") {
      const result = [];
      for (const treatment of get("storyboard-list").children) {
        const ol = treatment.children.find(child => child.tag === "ol");
        if (ol) result.push(...ol.children);
      }
      return result;
    }
    throw new Error("Unexpected query " + selector);
  },
  getElementById(id) { return get(id); },
  createElement(tag) { return new Node(tag); },
  createTextNode(text) { const node = new Node("#text"); node.textContent = text; return node; }
};

const context = { window: {}, document, console };
vm.runInNewContext(fs.readFileSync(path.join(study, "study-data.js"), "utf8"), context, { filename: "study-data.js" });
vm.runInNewContext(fs.readFileSync(path.join(study, "study.js"), "utf8"), context, { filename: "study.js" });

function linkVisible(id) { return get("relation-" + id).classList.contains("is-visible"); }
function focusIs(id) { return get("concept-" + id).classList.contains("is-selected"); }
function pressed(button) { return button.attributes["aria-pressed"] === "true"; }

assert.equal(get("storyboard-list").children.length, 2, "Two different storyboard treatments");
assert.equal(get("notation-list").children.length, 5, "Five candidate mappings");
assert.equal(get("interpretive-limits").children.length, 5, "Interpretive limits from model");
assert.equal(pressed(modes[0]), true, "Starts in conceptual overview");
assert.equal(linkVisible("reception"), true);
assert.equal(linkVisible("mediation"), true);
assert.equal(focusIs("organic-life"), true);
assert.equal(get("next-step").disabled, true);

modes[1].click();
assert.equal(pressed(modes[1]), true);
assert.equal(get("next-step").disabled, false);
assert.equal(linkVisible("reception"), false, "No relation is revealed in first source beat");
assert.equal(linkVisible("mediation"), false);
assert.equal(focusIs("planetary-world"), true);

get("next-step").click();
assert.equal(linkVisible("reception"), true, "Reception is revealed second in source-first mode");
assert.equal(linkVisible("mediation"), false);
assert.equal(focusIs("organic-life"), true);
assert.match(get("relation-summary").textContent, /Reception/);

get("next-step").click();
assert.equal(linkVisible("reception"), true);
assert.equal(linkVisible("mediation"), true);
assert.equal(focusIs("earth"), true);
assert.equal(get("next-step").disabled, true);

get("previous-step").click();
assert.equal(linkVisible("mediation"), false, "Back navigation hides only the later disclosure");

modes[2].click();
assert.equal(linkVisible("reception"), false);
assert.equal(linkVisible("mediation"), false);
assert.equal(focusIs("earth"), true);
get("next-step").click();
assert.equal(linkVisible("mediation"), true, "Mediation is revealed first in Earth-first mode");
assert.equal(linkVisible("reception"), false);
get("next-step").click();
assert.equal(linkVisible("mediation"), true);
assert.equal(linkVisible("reception"), true);
assert.equal(focusIs("planetary-world"), true);

inspectors[1].click();
assert.equal(focusIs("organic-life"), true);
assert.equal(pressed(inspectors[1]), true);
assert.equal(get("beat-label").textContent, "Beat 3 / 3", "Inspecting a concept does not alter explanatory order");
assert.match(get("focus-facets").textContent, /grass-covered field/i);

modes[0].click();
assert.equal(linkVisible("reception"), true);
assert.equal(linkVisible("mediation"), true);
assert.equal(get("previous-step").disabled, true);
assert.equal(pressed(modes[0]), true);

console.log("Experiment 014 mode interactions passed");
