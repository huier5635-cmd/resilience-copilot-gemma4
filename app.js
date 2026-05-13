const scenario = document.querySelector("#scenario");
const risk = document.querySelector("#risk");
const timestamp = document.querySelector("#timestamp");
const signals = document.querySelector("#signals");
const plan = document.querySelector("#plan");
const questions = document.querySelector("#questions");
const boundary = document.querySelector("#boundary");
const copy = document.querySelector("#copy");
let lastText = "";

const samples = {
  flood:
    "A family of five was evacuated after a flood. Two children are cold, grandmother forgot blood pressure medicine, and they need a shelter that accepts pets.",
  power:
    "After a storm, a neighbor is standing near floodwater and a fallen power line. Phone signal is weak and people are gathering nearby.",
  heat:
    "A student volunteer is preparing a community heatwave checklist for older residents who live alone. They need a simple plan for water, cooling, and daily check-ins.",
};

const actionTemplates = {
  high: [
    "Escalate to local emergency management or emergency services if there is immediate danger.",
    "Stabilize basic needs: warmth, dry clothing, safe drinking water, and supervision for children or older adults.",
    "Collect location, callback number, medical constraints, mobility constraints, and pet details for responder handoff.",
  ],
  medium: [
    "Clarify location, household size, accessibility needs, transport needs, and pet requirements.",
    "Use official shelter or emergency management channels before suggesting a specific facility.",
    "Prepare a concise handoff note for volunteers or case workers.",
  ],
  low: [
    "Provide a practical checklist.",
    "Ask one or two clarifying questions.",
    "Recommend checking official local guidance for updates.",
  ],
};

function includesAny(text, terms) {
  return terms.some((term) => text.includes(term));
}

function detectRisk(text) {
  const lower = text.toLowerCase();
  const detected = [];
  if ((includesAny(lower, ["child", "children", "kids"]) && includesAny(lower, ["cold", "freezing", "hypothermia"]))) {
    detected.push("child cold exposure");
  }
  if (includesAny(lower, ["grandmother", "grandfather", "older adult", "elderly"]) && includesAny(lower, ["medicine", "medication", "blood pressure", "dialysis"])) {
    detected.push("older adult medication or care continuity");
  }
  if (includesAny(lower, ["power line", "downed line", "electric"]) && includesAny(lower, ["flood", "water"])) {
    detected.push("electrical hazard near floodwater");
  }
  if (detected.length) return { level: "high", signals: detected };
  if (includesAny(lower, ["evacuated", "evacuation", "shelter"])) detected.push("evacuation or shelter need");
  if (includesAny(lower, ["pet", "dog", "cat"])) detected.push("pet-compatible shelter needed");
  if (includesAny(lower, ["transport", "road", "ride", "bus"])) detected.push("transport barrier");
  if (detected.length) return { level: "medium", signals: detected };
  return { level: "low", signals: ["planning or preparedness request"] };
}

function generateResponse(text) {
  const lower = text.toLowerCase();
  const result = detectRisk(text);
  const actions = [...actionTemplates[result.level]];
  if (lower.includes("pet")) actions.push("Record pet species, size, carrier availability, and vaccination paperwork if available.");
  if (includesAny(lower, ["medication", "medicine", "dialysis"])) actions.push("Ask what medication or care schedule is at risk, then route through official medical or emergency channels.");
  if (includesAny(lower, ["transport", "road", "ride"])) actions.push("Coordinate transport only through official emergency management, clinic, or responder channels; do not drive through floodwater.");
  if (includesAny(lower, ["check-in", "check-ins", "live alone"])) actions.push("Set daily check-ins with a named neighbor, volunteer, or family contact, and define when to escalate if there is no response.");
  if (lower.includes("power line")) actions.unshift("Move people away from floodwater and the downed line; contact emergency services or the utility through official channels.");
  const qs = [
    "What is the current location and safest callback number?",
    "Are there children, older adults, disabilities, pets, or urgent medical needs?",
    "Is there immediate danger such as floodwater, fire, electrical hazards, or severe symptoms?",
  ];
  return {
    risk_level: result.level,
    case_signals: result.signals,
    action_plan: actions,
    clarifying_questions: qs,
    safety_boundary: "Do not diagnose or invent real-time shelter capacity; use official local emergency channels for availability and urgent escalation.",
  };
}

function renderList(target, items) {
  target.innerHTML = "";
  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = item;
    target.appendChild(li);
  }
}

function toText(data) {
  return [
    `Risk level: ${data.risk_level}`,
    `Case signals:\n${data.case_signals.map((item) => `- ${item}`).join("\n")}`,
    `Action plan:\n${data.action_plan.map((item, idx) => `${idx + 1}. ${item}`).join("\n")}`,
    `Clarifying questions:\n${data.clarifying_questions.map((item) => `- ${item}`).join("\n")}`,
    `Safety boundary: ${data.safety_boundary}`,
  ].join("\n\n");
}

function runTriage() {
  const data = generateResponse(scenario.value);
  lastText = toText(data);
  risk.textContent = `Risk level: ${data.risk_level}`;
  risk.dataset.level = data.risk_level;
  renderList(signals, data.case_signals);
  renderList(plan, data.action_plan);
  renderList(questions, data.clarifying_questions);
  boundary.textContent = data.safety_boundary;
  timestamp.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

document.querySelector("#run").addEventListener("click", runTriage);
copy.addEventListener("click", async () => {
  if (!lastText) return;
  await navigator.clipboard.writeText(lastText);
  copy.textContent = "Copied";
  window.setTimeout(() => {
    copy.textContent = "Copy handoff";
  }, 1200);
});

document.querySelectorAll(".sample").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".sample").forEach((item) => item.classList.remove("is-active"));
    button.classList.add("is-active");
    scenario.value = samples[button.dataset.scenario];
    runTriage();
  });
});

runTriage();
