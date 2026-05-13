const scenario = document.querySelector("#scenario");
const risk = document.querySelector("#risk");
const timestamp = document.querySelector("#timestamp");
const signals = document.querySelector("#signals");
const plan = document.querySelector("#plan");
const resources = document.querySelector("#resources");
const questions = document.querySelector("#questions");
const language = document.querySelector("#language");
const handoff = document.querySelector("#handoff");
const boundary = document.querySelector("#boundary");
const copy = document.querySelector("#copy");
let lastText = "";

const samples = {
  flood:
    "A family of five was evacuated after a flood. Two children are cold, grandmother forgot blood pressure medicine, and they need a shelter that accepts pets.",
  power:
    "After a storm, a neighbor is standing near floodwater and a fallen power line. Phone signal is weak and people are gathering nearby.",
  language:
    "A Spanish-speaking family arrived at an evacuation center and cannot understand the registration instructions. One child has asthma medication, and the parent needs help explaining the care need safely.",
  resources:
    "A volunteer is triaging evacuees after a flood: one family has insulin that must stay cold, another has a dog, and an older adult needs accessible transport. Someone says a shelter can take everyone, but nobody has checked official sources.",
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
  if (includesAny(lower, ["pregnant", "prenatal", "pregnancy", "insulin"])) {
    detected.push("pregnancy or insulin continuity risk");
  }
  if (includesAny(lower, ["oxygen concentrator", "oxygen", "backup battery", "medical device"]) && includesAny(lower, ["power", "battery", "outage", "empty"])) {
    detected.push("oxygen or powered medical device risk");
  }
  if (detected.length) return { level: "high", signals: detected };
  if (includesAny(lower, ["evacuated", "evacuation", "shelter"])) detected.push("evacuation or shelter need");
  if (includesAny(lower, ["pet", "dog", "cat"])) detected.push("pet-compatible shelter needed");
  if (includesAny(lower, ["transport", "road", "ride", "bus"])) detected.push("transport barrier");
  if (includesAny(lower, ["dialysis", "appointment", "care"])) detected.push("care continuity concern");
  if (includesAny(lower, ["spanish-speaking", "interpreter", "translation", "language barrier", "cannot understand", "limited english", "cantonese", "mandarin", "chinese"])) detected.push("language access barrier");
  if ((includesAny(lower, ["rumor", "social media"]) && includesAny(lower, ["shelter", "beds", "capacity"]))) detected.push("unverified shelter capacity rumor");
  if (detected.length) return { level: "medium", signals: detected };
  return { level: "low", signals: ["planning or preparedness request"] };
}

function detectPreferredLanguage(text) {
  const lower = text.toLowerCase();
  if (includesAny(lower, ["spanish-speaking", "spanish"])) return "Spanish";
  if (includesAny(lower, ["chinese", "mandarin", "cantonese"])) return "Chinese";
  if (lower.includes("vietnamese")) return "Vietnamese";
  if (lower.includes("arabic")) return "Arabic";
  if (includesAny(lower, ["limited english", "does not speak english", "cannot understand", "language barrier", "interpreter", "translation"])) {
    return "Unknown non-English language";
  }
  return null;
}

function buildLanguageSupport(text) {
  const preferredLanguage = detectPreferredLanguage(text);
  if (!preferredLanguage) {
    return ["Ask whether the household prefers another language, plain-language instructions, or an accessible format."];
  }
  return [
    `Preferred language: ${preferredLanguage}.`,
    "Use a qualified interpreter or language-access volunteer before collecting sensitive medical, registration, or shelter details.",
    "Read back the action plan in the preferred language and confirm understanding before routing the case.",
    "Do not use children as interpreters for medical or safety-critical details.",
  ];
}

function buildOfficialResourceChecks(text, result) {
  const lower = text.toLowerCase();
  const checks = ["Local emergency management: verify current evacuation orders, road closures, and official shelter routing before sending people anywhere."];
  if (result.level === "high" || result.signals.some((signal) => ["oxygen", "floodwater", "electrical"].some((term) => signal.includes(term)))) {
    checks.push("Emergency services or utility emergency line: use for immediate danger, downed power lines, oxygen/powered-device failure, or life-safety escalation.");
  }
  if (includesAny(lower, ["shelter", "evacuat"])) {
    checks.push("Shelter operations desk: confirm accessibility, pet policy, intake requirements, and live capacity; do not rely on social media capacity claims.");
  }
  if (includesAny(lower, ["medication", "medicine", "dialysis", "insulin", "prenatal", "asthma", "oxygen", "care"])) {
    checks.push("Medical triage, clinic, pharmacy, or care coordinator: verify medication continuity, device power needs, dialysis/prenatal timing, and safe storage.");
  }
  if (includesAny(lower, ["transport", "road", "ride", "bus"])) {
    checks.push("Official transport desk or emergency management logistics: arrange accessible transport and avoid flooded roads.");
  }
  if (includesAny(lower, ["pet", "dog", "cat"])) {
    checks.push("Animal services or shelter pet desk: verify pet intake rules, carrier needs, and documentation.");
  }
  if (detectPreferredLanguage(text)) {
    checks.push("Language access line or qualified interpreter pool: confirm interpretation support before collecting medical or legal details.");
  }
  return checks;
}

function buildResponderHandoff(result, actions, qs, languageSupport, officialChecks) {
  return [
    `Risk: ${result.level}.`,
    `Signals: ${result.signals.join("; ")}.`,
    `Immediate routing: ${actions.slice(0, 2).join(" ")}`,
    `Official checks: ${officialChecks.slice(0, 2).join(" ")}`,
    `Open information: ${qs.slice(0, 2).join(" ")}`,
    `Language/access note: ${languageSupport[0]}`,
  ];
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
  if (includesAny(lower, ["pregnant", "prenatal", "insulin"])) actions.push("Route pregnancy, insulin, or prenatal-care continuity through official medical triage; record storage needs, timing, and callback details.");
  if (includesAny(lower, ["oxygen", "medical device", "backup battery"])) actions.unshift("Treat oxygen or powered medical device interruption as urgent; contact emergency services, utility medical priority channels, or clinical support.");
  if (includesAny(lower, ["spanish", "interpreter", "cannot understand", "limited english", "cantonese", "mandarin", "chinese"])) actions.push("Request a qualified interpreter or language-access volunteer before collecting sensitive medication or registration details.");
  if (includesAny(lower, ["rumor", "social media", "capacity", "beds"])) actions.push("Verify shelter capacity only through official emergency management or shelter operations before routing evacuees.");
  const qs = [
    "What is the current location and safest callback number?",
    "Are there children, older adults, disabilities, pets, or urgent medical needs?",
    "Is there immediate danger such as floodwater, fire, electrical hazards, or severe symptoms?",
  ];
  if (detectPreferredLanguage(text)) {
    qs.splice(1, 0, "What is the preferred language, and is a qualified interpreter available now?");
  }
  const languageSupport = buildLanguageSupport(text);
  const officialChecks = buildOfficialResourceChecks(text, result);
  const responderHandoff = buildResponderHandoff(result, actions, qs, languageSupport, officialChecks);
  return {
    risk_level: result.level,
    case_signals: result.signals,
    action_plan: actions,
    official_resource_checks: officialChecks,
    clarifying_questions: qs,
    language_support: languageSupport,
    responder_handoff: responderHandoff,
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
    `Official resource checks:\n${data.official_resource_checks.map((item) => `- ${item}`).join("\n")}`,
    `Clarifying questions:\n${data.clarifying_questions.map((item) => `- ${item}`).join("\n")}`,
    `Language support:\n${data.language_support.map((item) => `- ${item}`).join("\n")}`,
    `Responder handoff:\n${data.responder_handoff.map((item) => `- ${item}`).join("\n")}`,
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
  renderList(resources, data.official_resource_checks);
  renderList(questions, data.clarifying_questions);
  renderList(language, data.language_support);
  renderList(handoff, data.responder_handoff);
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
