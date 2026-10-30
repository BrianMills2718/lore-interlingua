/* Experiment 014 formative study: browser-local stage controller.
 * No network requests, analytics, cookies, persistent storage or participant IDs.
 * All answer keys are kept in the offline scorer, not in this script.
 */
(function () {
  "use strict";

  const allowed = new Set(["follow-influence", "trace-from-earth"]);
  const comprehensionNames = ["C1", "C2", "C3"];
  const transferNames = ["T1", "T2", "T3", "T4"];
  const state = { stage: "setup", condition: "follow-influence", comprehension: null, transfer: null, exposure: false };
  const get = function (id) { return document.getElementById(id); };

  function radioAnswers(names) {
    const answers = {};
    names.forEach(function (name) {
      const selected = document.querySelector('input[name="' + name + '"]:checked');
      answers[name] = selected ? selected.value : null;
    });
    return answers;
  }

  function setStage(name) {
    ["setup", "comprehension", "transfer", "finish"].forEach(function (key) {
      get("stage-" + key).hidden = key !== name;
      const progress = get("progress-" + key);
      if (key === name) progress.setAttribute("aria-current", "step");
      else progress.removeAttribute("aria-current");
    });
    state.stage = name;
    get("stage-" + name).scrollIntoView({ block: "start", behavior: "instant" });
  }

  function updateAssignedCondition() {
    const choice = get("condition").value;
    state.condition = allowed.has(choice) ? choice : "follow-influence";
    get("lesson-link").href = "../index.html?mode=" + state.condition;
  }

  function collect() {
    return {
      schema: "lore-interlingua-experiment-014-formative-v1",
      condition: state.condition,
      exposure_self_reported_complete: state.exposure,
      comprehension: state.comprehension,
      transfer: state.transfer,
      note: "Anonymous local-form responses. No source-world claims or viewer-outcome conclusions are implied by this file."
    };
  }

  function moveToComprehension() {
    if (state.stage !== "setup" || !get("exposure-complete").checked) return;
    updateAssignedCondition();
    state.exposure = true;
    get("condition").disabled = true;
    setStage("comprehension");
  }

  function moveToTransfer() {
    if (state.stage !== "comprehension") return;
    state.comprehension = Object.assign(radioAnswers(comprehensionNames), {
      C4: get("C4").value.trim()
    });
    setStage("transfer");
  }

  function moveToFinish() {
    if (state.stage !== "transfer") return;
    state.transfer = Object.assign(radioAnswers(transferNames), {
      T5: get("T5").value.trim()
    });
    get("response-json").value = JSON.stringify(collect(), null, 2) + "\n";
    setStage("finish");
  }

  function download() {
    if (state.stage !== "finish") return;
    const blob = new Blob([get("response-json").value], { type: "application/json;charset=utf-8" });
    const uri = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = uri;
    anchor.download = "experiment-014-anonymous-response.json";
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    // A locally generated object URL, not a remote endpoint.
    URL.revokeObjectURL(uri);
    get("export-status").textContent = "Download requested. Check the browser's saved files.";
  }

  async function copy() {
    if (state.stage !== "finish") return;
    const value = get("response-json").value;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await navigator.clipboard.writeText(value);
        get("export-status").textContent = "Response JSON copied.";
        return;
      } catch (_) {
        // Some local file:// browsers disallow clipboard access.
      }
    }
    get("response-json").focus();
    get("response-json").select();
    get("export-status").textContent = "Select/copy the highlighted JSON manually, or use Download.";
  }

  // The assigned order can be passed in a local file:// or Pages URL. Invalid values are ignored.
  const search = (window.location && window.location.search) || "";
  const matched = /(?:\?|&)condition=(follow-influence|trace-from-earth)(?:&|$)/.exec(search);
  if (matched) get("condition").value = matched[1];
  updateAssignedCondition();

  get("condition").addEventListener("change", updateAssignedCondition);
  get("exposure-complete").addEventListener("change", function () {
    get("begin-comprehension").disabled = !get("exposure-complete").checked;
  });
  get("begin-comprehension").addEventListener("click", moveToComprehension);
  get("begin-transfer").addEventListener("click", moveToTransfer);
  get("finish").addEventListener("click", moveToFinish);
  get("download").addEventListener("click", download);
  get("copy").addEventListener("click", copy);
})();
