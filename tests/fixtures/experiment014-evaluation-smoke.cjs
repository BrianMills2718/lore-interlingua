/* Dependency-free DOM smoke test. Does not model a real participant or browser. */
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const root = path.resolve(__dirname, "../..");
const file = path.join(root, "experiments", "014-conceptual-representation", "evaluation", "study.js");

class Element {
  constructor(id) {
    this.id = id;
    this.value = "";
    this.checked = false;
    this.disabled = false;
    this.hidden = false;
    this.href = "";
    this.attributes = {};
    this.listeners = {};
    this.textContent = "";
    this.children = [];
  }
  addEventListener(event, callback) { this.listeners[event] = callback; }
  dispatch(event) { assert.equal(typeof this.listeners[event], "function", this.id + " needs " + event + " handler"); this.listeners[event](); }
  click() { if (!this.disabled) this.dispatch("click"); }
  scrollIntoView() {}
  setAttribute(name, value) { this.attributes[name] = String(value); }
  removeAttribute(name) { delete this.attributes[name]; }
  appendChild(node) { this.children.push(node); }
  remove() { this.removed = true; }
  focus() {}
  select() {}
}
const elements = new Map();
function get(id) {
  if (!elements.has(id)) elements.set(id, new Element(id));
  return elements.get(id);
}
const ids = [
  "stage-setup", "stage-comprehension", "stage-transfer", "stage-finish",
  "progress-setup", "progress-comprehension", "progress-transfer", "progress-finish",
  "condition", "lesson-link", "exposure-complete", "begin-comprehension",
  "begin-transfer", "finish", "response-json", "download", "copy", "export-status",
  "C4", "T5"
];
ids.forEach(get);
get("begin-comprehension").disabled = true;
get("stage-comprehension").hidden = true;
get("stage-transfer").hidden = true;
get("stage-finish").hidden = true;

const selected = {};
const downloads = { created: [], revoked: [], anchors: [] };
const document = {
  getElementById: get,
  querySelector(query) {
    const matched = /^input\[name="(C[123]|T[1234])"\]:checked$/.exec(query);
    if (!matched) throw Error("Unrecognized query: " + query);
    return selected[matched[1]] ? {value:selected[matched[1]]} : null;
  },
  createElement(name) {
    if (name !== "a") throw Error("Only local download anchors are allowed");
    const link = new Element("download-anchor");
    link.addEventListener("click", function () { downloads.anchors.push({href:link.href, download:link.download}); });
    return link;
  },
  body: { appendChild(node) { if (node.id !== "download-anchor") throw Error("Invalid DOM append"); } }
};

const window = { location: { search: "?condition=trace-from-earth" } };
const URL = {
  createObjectURL(blob) { downloads.created.push(blob); return "blob:local-export"; },
  revokeObjectURL(uri) { downloads.revoked.push(uri); }
};
class Blob {
  constructor(parts, props) {
    this.parts = parts;
    this.type = props.type;
  }
}
vm.runInNewContext(fs.readFileSync(file, "utf8"), {window, document, Blob, URL, navigator: {}, console}, {filename:"study.js"});

assert.equal(get("condition").value, "trace-from-earth", "Assigned mode should be selected from URL");
assert.match(get("lesson-link").href, /\?mode=trace-from-earth$/);
assert.equal(get("begin-comprehension").disabled, true);
get("exposure-complete").checked = true;
get("exposure-complete").dispatch("change");
assert.equal(get("begin-comprehension").disabled, false);
get("begin-comprehension").click();
assert.equal(get("stage-setup").hidden, true);
assert.equal(get("stage-comprehension").hidden, false);
assert.equal(get("progress-comprehension").attributes["aria-current"], "step");

selected.C1 = "planet_life_earth";
selected.C2 = "unsure";
get("C4").value = "Planetary influences received by organic life are mediated toward Earth.";
get("begin-transfer").click();
assert.equal(get("stage-comprehension").hidden, true);
assert.equal(get("stage-transfer").hidden, false);
selected.C1 = "life_creates_planets"; // hidden and locked: should not change the captured record
selected.T1 = "dashed_nara_ivo";
selected.T2 = "dashed_nara_ivo";
selected.T3 = "ivo";
selected.T4 = "unsure";
get("T5").value = "The dashed versus solid association was difficult to remember.";
get("finish").click();
assert.equal(get("stage-transfer").hidden, true);
assert.equal(get("stage-finish").hidden, false);
const record = JSON.parse(get("response-json").value);
assert.equal(record.schema, "lore-interlingua-experiment-014-formative-v1");
assert.equal(record.condition, "trace-from-earth");
assert.equal(record.exposure_self_reported_complete, true);
assert.equal(record.comprehension.C1, "planet_life_earth");
assert.equal(record.comprehension.C2, "unsure");
assert.equal(record.comprehension.C3, null);
assert.equal(record.transfer.T1, "dashed_nara_ivo");
assert.equal(record.transfer.T2, "dashed_nara_ivo");
assert.equal(record.transfer.T3, "ivo");
assert.equal(record.transfer.T4, "unsure");
assert.equal(Object.hasOwn(record, "participant_name"), false);
assert.equal(Object.hasOwn(record, "timestamp"), false);

get("download").click();
assert.equal(downloads.created.length, 1);
assert.equal(downloads.created[0].type, "application/json;charset=utf-8");
assert.equal(downloads.anchors[0].download, "experiment-014-anonymous-response.json");
assert.equal(downloads.anchors[0].href, "blob:local-export");
assert.deepEqual(downloads.revoked, ["blob:local-export"]);

console.log("Experiment 014 evaluation flow passed");
