const scenario = document.querySelector("#scenario");
const risk = document.querySelector("#risk");
const timestamp = document.querySelector("#timestamp");
const signals = document.querySelector("#signals");
const reviewReason = document.querySelector("#review-reason");
const playbook = document.querySelector("#playbook");
const plan = document.querySelector("#plan");
const resources = document.querySelector("#resources");
const sourceVerification = document.querySelector("#source-verification");
const transferBrief = document.querySelector("#transfer-brief");
const questions = document.querySelector("#questions");
const language = document.querySelector("#language");
const handoff = document.querySelector("#handoff");
const packet = document.querySelector("#packet");
const household = document.querySelector("#household");
const audit = document.querySelector("#audit");
const caseExport = document.querySelector("#case-export");
const boundary = document.querySelector("#boundary");
const copy = document.querySelector("#copy");
const copyPacket = document.querySelector("#copy-packet");
const copyJson = document.querySelector("#copy-json");
const briefReview = document.querySelector("#brief-review");
const briefPlaybooks = document.querySelector("#brief-playbooks");
const briefRoutes = document.querySelector("#brief-routes");
const briefEvidence = document.querySelector("#brief-evidence");
let lastText = "";
let lastPacketText = "";
let lastJsonText = "";

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
    "A senior with diabetes is overheated during an extreme heat outage, has insulin that needs safe storage, speaks limited English, has no car, and needs routing to a cooling center without anyone promising capacity.",
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

const playbookRules = [
  {
    id: "PB-LIFE-SAFETY-ESCALATE",
    title: "Immediate life-safety escalation",
    signals: ["high", "electrical hazard near floodwater", "oxygen or powered medical device risk", "immediate flood danger"],
    summary: "Escalate immediate danger through emergency services or official local responders before giving routine logistics advice.",
  },
  {
    id: "PB-SHELTER-CAPACITY",
    title: "Official shelter capacity verification",
    signals: ["evacuation or shelter need", "unverified shelter capacity rumor"],
    summary: "Confirm live shelter capacity, accessibility, intake rules, and routing through official emergency management or shelter operations.",
  },
  {
    id: "PB-MEDICATION-CONTINUITY",
    title: "Medication and care continuity",
    signals: ["older adult medication or care continuity", "pregnancy or insulin continuity risk", "care continuity concern"],
    summary: "Route medication, insulin storage, dialysis, oxygen, prenatal, and asthma needs through official medical triage, clinic, pharmacy, or care coordinator channels.",
  },
  {
    id: "PB-ACCESSIBLE-TRANSPORT",
    title: "Accessible transport routing",
    signals: ["transport barrier"],
    summary: "Arrange accessible transport through official emergency management logistics, clinic, shelter, or responder channels; avoid flooded roads.",
  },
  {
    id: "PB-PET-SHELTER",
    title: "Pet-compatible shelter intake",
    signals: ["pet-compatible shelter needed"],
    summary: "Verify pet policy, species/size limits, carrier needs, vaccination paperwork, and animal-service options before routing a household.",
  },
  {
    id: "PB-LANGUAGE-ACCESS",
    title: "Qualified language access",
    signals: ["language access barrier"],
    summary: "Use qualified interpreters or language-access volunteers for medical, legal, registration, and shelter details; confirm understanding in the preferred language.",
  },
  {
    id: "PB-HEAT-COOLING-CENTER",
    title: "Heat response and cooling-center routing",
    signals: ["cooling center or heat safety routing", "heat illness with medication or mobility risk"],
    summary: "Route heat exposure, cooling-center access, welfare checks, medication storage, and transport needs through public health or official emergency-management heat-response channels.",
  },
  {
    id: "PB-LOW-RISK-PREPAREDNESS",
    title: "Preparedness without over-escalation",
    signals: ["low", "planning or preparedness request"],
    summary: "Give a practical checklist, ask concise follow-up questions, and point to official local guidance for changing conditions.",
  },
];

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
  if (includesAny(lower, ["power line", "downed line", "electric"]) && includesAny(lower, ["flood", "floodwater", "water"])) {
    detected.push("electrical hazard near floodwater");
  }
  if (includesAny(lower, ["pregnant", "prenatal", "pregnancy", "insulin"])) {
    detected.push("pregnancy or insulin continuity risk");
  }
  if (includesAny(lower, ["oxygen concentrator", "oxygen", "backup battery", "medical device"]) && includesAny(lower, ["power", "battery", "outage", "empty"])) {
    detected.push("oxygen or powered medical device risk");
  }
  if (includesAny(lower, ["heat illness", "overheated", "no cooling"]) && includesAny(lower, ["insulin", "diabetes", "older adult", "elderly", "wheelchair", "mobility"])) {
    detected.push("heat illness with medication or mobility risk");
  }
  const hasHighSignal = detected.length > 0;
  if (includesAny(lower, ["evacuated", "evacuation", "shelter"])) detected.push("evacuation or shelter need");
  if (includesAny(lower, ["pet", "dog", "cat"])) detected.push("pet-compatible shelter needed");
  if (includesAny(lower, ["transport", "road", "ride", "bus", "no car", "drive", "driving"])) detected.push("transport barrier");
  if (includesAny(lower, ["dialysis", "appointment", "care", "asthma"])) detected.push("care continuity concern");
  if (includesAny(lower, ["spanish-speaking", "interpreter", "translation", "language barrier", "cannot understand", "limited english", "cantonese", "mandarin", "chinese", "vietnamese", "arabic"])) detected.push("language access barrier");
  if ((includesAny(lower, ["rumor", "social media"]) && includesAny(lower, ["shelter", "beds", "capacity"]))) detected.push("unverified shelter capacity rumor");
  if (includesAny(lower, ["cooling center", "heat outage", "no cooling", "overheated", "extreme heat", "heat illness"])) detected.push("cooling center or heat safety routing");
  if (hasHighSignal) return { level: "high", signals: detected };
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

function buildHumanReviewReason(text, result) {
  const lower = text.toLowerCase();
  const reasons = [];
  if (result.level === "high") {
    reasons.push("life-safety escalation: high-risk signals require a human responder before final routing.");
  } else if (result.level === "medium") {
    reasons.push("official resource verification: responder review is needed before sending people to a site or service.");
  } else {
    reasons.push("preparedness check: human review is optional unless local conditions change.");
  }
  if (includesAny(lower, ["insulin", "dialysis", "oxygen", "medication", "medicine", "prenatal", "asthma", "medical device"])) {
    reasons.push("medical continuity: medication, device, or care timing needs official medical or clinical confirmation.");
  }
  if (includesAny(lower, ["rumor", "capacity", "beds", "shelter can", "cooling center"])) {
    reasons.push("capacity uncertainty: live shelter or cooling-center availability must come from official operations staff.");
  }
  if (includesAny(lower, ["transport", "road", "ride", "bus", "no car"])) {
    reasons.push("transport safety: route and vehicle availability need official logistics confirmation.");
  }
  if (detectPreferredLanguage(text)) {
    reasons.push("language-access-sensitive: qualified interpretation is needed before collecting medical, legal, or registration details.");
  }
  if (result.signals.some((signal) => ["electrical", "floodwater", "oxygen"].some((term) => signal.includes(term)))) {
    reasons.push("immediate hazard: emergency services or utility channels may need to act before routine shelter routing.");
  }
  const seen = new Set();
  return reasons.filter((reason) => {
    const key = reason.split(":", 1)[0];
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
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
  if (includesAny(lower, ["cooling center", "heat outage", "no cooling", "overheated", "extreme heat", "heat illness"])) {
    checks.push("Public health heat line or cooling-center coordinator: verify cooling-center hours, accessible intake, hydration support, medication storage, and welfare-check options.");
  }
  if (includesAny(lower, ["transport", "road", "ride", "bus", "no car"])) {
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

function buildSourceVerification(text, result, officialChecks) {
  const lower = text.toLowerCase();
  const ledger = ["Known: case details are user- or volunteer-reported and must be treated as operational notes until official staff verify live conditions."];
  if (includesAny(lower, ["rumor", "social media", "heard", "probably", "may have beds", "capacity", "beds"])) {
    ledger.push("Rumor quarantine: do not repeat social-media, word-of-mouth, bed-count, or capacity claims until official shelter operations confirms them.");
  }
  if (includesAny(lower, ["shelter", "cooling center", "road", "transport", "ride", "bus", "no car"])) {
    ledger.push("Freshness check: verify timestamp, current route status, facility hours, intake rules, accessibility, and transport availability before sharing directions.");
  }
  if (includesAny(lower, ["insulin", "dialysis", "oxygen", "medication", "medicine", "prenatal", "asthma", "medical device"])) {
    ledger.push("Clinical source check: route medication, oxygen, insulin, dialysis, prenatal, or device-power details through medical triage, clinic, pharmacy, or care coordinator confirmation.");
  }
  if (detectPreferredLanguage(text)) {
    ledger.push("Language source check: use a qualified interpreter for safety-critical details; do not treat child or ad hoc translation as verified.");
  }
  if (result.level === "high") {
    ledger.push("Escalation evidence: record callback, location, official route contacted, and what remains unknown before final responder decision.");
  }
  ledger.push(`Official channels to verify first: ${officialChecks.slice(0, 3).map((item) => item.split(":", 1)[0]).join(" | ")}.`);
  ledger.push("Public message rule: say what is known, what is unknown, and what is being checked; avoid unverified numbers or guarantees.");
  return ledger;
}

function buildTransferBrief(text, result, humanReviewReason, playbookReferences, officialChecks, sourceLedger, questions, languageSupport) {
  const playbookIds = playbookReferences.map((item) => item.split(" - ", 1)[0]);
  const routeLabels = officialChecks.slice(0, 3).map((item) => item.split(":", 1)[0]);
  const preferredLanguage = detectPreferredLanguage(text) || "none";
  return [
    "ICS 201 alignment: concise transfer note for situation summary, current actions, resource status, communications, and prepared-by handoff.",
    `Incident snapshot: risk=${result.level}; signals=${result.signals.join(" | ")}; playbooks=${playbookIds.join(" | ")}.`,
    "Immediate objectives: protect life safety first, verify official routes, collect callback/location/access needs, and keep final routing with a human responder.",
    "Safety constraints: do not diagnose, do not promise live capacity, do not guarantee routes or transport, and do not use child or ad hoc interpreters for sensitive details.",
    `Resource status: pending confirmation through ${routeLabels.join(" | ")}; unresolved resources stay unknown until staff confirm them.`,
    `Communications: record callback, current location, preferred language=${preferredLanguage}, official channel contacted, time checked, and next owner.`,
    `Unresolved questions: ${questions.slice(0, 2).join(" ")}`,
    `Verification carryover: ${sourceLedger.slice(0, 2).join(" ")} ${languageSupport[0]}`,
    "Operational period check: re-verify facility hours, road status, transport ETA, welfare-check status, and capacity before each routing decision.",
  ];
}

function selectPlaybookReferences(result) {
  const signalSet = new Set([result.level, ...result.signals]);
  const refs = playbookRules
    .filter((rule) => rule.signals.some((signal) => signalSet.has(signal)))
    .map((rule) => `${rule.id} - ${rule.title}: ${rule.summary}`);
  if (!refs.length) {
    const fallback = playbookRules.find((rule) => rule.id === "PB-LOW-RISK-PREPAREDNESS");
    refs.push(`${fallback.id} - ${fallback.title}: ${fallback.summary}`);
  }
  return refs.slice(0, 5);
}

function buildResponderHandoff(result, humanReviewReason, playbookReferences, actions, qs, languageSupport, officialChecks, sourceLedger, transferBriefItems) {
  return [
    `Risk: ${result.level}.`,
    `Signals: ${result.signals.join("; ")}.`,
    `Human review reason: ${humanReviewReason.slice(0, 2).join(" ")}`,
    `Playbook basis: ${playbookReferences.slice(0, 2).map((item) => item.split(":", 1)[0]).join(" ")}.`,
    `Immediate routing: ${actions.slice(0, 2).join(" ")}`,
    `Official checks: ${officialChecks.slice(0, 2).join(" ")}`,
    `Source verification: ${sourceLedger.slice(0, 2).join(" ")}`,
    `Transfer brief: ${transferBriefItems.slice(1, 3).join(" ")}`,
    `Open information: ${qs.slice(0, 2).join(" ")}`,
    `Language/access note: ${languageSupport[0]}`,
  ];
}

function buildResponderPacket(result, humanReviewReason, playbookReferences, officialChecks, sourceLedger, transferBriefItems, qs, languageSupport) {
  const playbookIds = playbookReferences.map((item) => item.split(" - ", 1)[0]);
  const primaryRoute = result.level === "high" && officialChecks.length > 1 ? officialChecks[1] : officialChecks[0];
  return [
    `Case priority: ${result.level}.`,
    `Human review reason: ${humanReviewReason.slice(0, 2).join(" ")}`,
    `Playbook IDs: ${playbookIds.join(", ")}.`,
    `Primary official route: ${primaryRoute}`,
    `Source verification: ${sourceLedger.slice(0, 2).join(" ")}`,
    `Transfer brief: ${transferBriefItems[1]} ${transferBriefItems[4]}`,
    `Missing information: ${qs.slice(0, 2).join(" ")}`,
    `Language/access cue: ${languageSupport[0]}`,
    "Do not promise: live shelter capacity, medical conclusions, road safety, or transport availability without official confirmation.",
    "Copy packet: risk, signals, callback/location, official route, open items, and access needs.",
    `Signal summary: ${result.signals.join("; ")}.`,
  ];
}

function buildHouseholdMessage(text, result, officialChecks, qs, languageSupport) {
  const preferredLanguage = detectPreferredLanguage(text);
  const message = [
    "Plain English holding note: we are treating this as a priority case and routing it through official local channels.",
    "Please keep the safest callback number available and tell the volunteer your current location.",
    "We cannot confirm a shelter bed, road safety, medical next steps, or transport availability until official staff verify them.",
  ];
  if (result.level === "high") {
    message.push("If immediate danger worsens, contact emergency services or local responders now.");
  }
  if (preferredLanguage) {
    message.push(`Preferred language: ${preferredLanguage}; use a qualified interpreter before collecting sensitive details.`);
    message.push("This is not a full translation of medical, legal, or registration details.");
  } else {
    message.push(languageSupport[0]);
  }
  message.push(`Official channel to check first: ${officialChecks[0]}`);
  message.push(`Open question to answer next: ${qs[0]}`);
  return message;
}

function buildAuditTrace(text, result, humanReviewReason, playbookReferences, officialChecks, sourceLedger, transferBriefItems) {
  const playbookIds = playbookReferences.map((item) => item.split(" - ", 1)[0]);
  const routeLabels = officialChecks.map((item) => item.split(":", 1)[0]);
  return [
    `risk_level=${result.level}`,
    `signals=${result.signals.join(" | ")}`,
    `playbook_ids=${playbookIds.join(" | ")}`,
    `official_routes=${routeLabels.join(" | ")}`,
    `source_verification=${sourceLedger.map((item) => item.split(":", 1)[0]).join(" | ")}`,
    `transfer_brief=${transferBriefItems.slice(0, 6).map((item) => item.split(":", 1)[0]).join(" | ")}`,
    `language=${detectPreferredLanguage(text) || "none"}`,
    "human_review_required=true",
    `human_review_reason=${humanReviewReason.map((reason) => reason.split(":", 1)[0]).join(" | ")}`,
    "blocked_claims=medical conclusions | live shelter capacity | road safety | transport availability",
    "response_contract=official-routes-first | no-invented-capacity | qualified-interpreter-when-needed",
  ];
}

function fingerprint(text) {
  let hash = 2166136261;
  for (const char of text.toLowerCase().trim().replace(/\s+/g, " ")) {
    hash ^= char.charCodeAt(0);
    hash = Math.imul(hash, 16777619);
  }
  return `RC-${(hash >>> 0).toString(16).padStart(8, "0")}`;
}

function buildCaseExport(text, result, humanReviewReason, playbookReferences, officialChecks, sourceLedger, transferBriefItems, questions) {
  const playbookIds = playbookReferences.map((item) => item.split(" - ", 1)[0]);
  const routeLabels = officialChecks.map((item) => item.split(":", 1)[0]);
  const reviewLevel = {
    high: "immediate_escalation",
    medium: "responder_review",
    low: "preparedness_check",
  }[result.level];
  return {
    contract_version: "resilience-copilot-exp029",
    case_fingerprint: fingerprint(text),
    risk_level: result.level,
    review_level: reviewLevel,
    signals: result.signals,
    human_review_reason: humanReviewReason,
    playbook_ids: playbookIds,
    official_routes: routeLabels,
    source_verification: sourceLedger,
    transfer_brief: transferBriefItems,
    required_human_review: true,
    blocked_claims: ["medical conclusions", "live shelter capacity", "road safety", "transport availability"],
    language: detectPreferredLanguage(text) || "none",
    missing_information: questions.slice(0, 3),
    response_contract: [
      "official-routes-first",
      "no-invented-capacity",
      "qualified-interpreter-when-needed",
      "human-responder-final-decision",
      "ics-style-transfer-brief",
    ],
  };
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
  if (includesAny(lower, ["cooling center", "heat outage", "no cooling", "overheated", "extreme heat", "heat illness"])) actions.push("Route heat exposure, cooling-center access, welfare checks, medication storage, and hydration support through public health or official emergency-management heat-response channels.");
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
  const playbookReferences = selectPlaybookReferences(result);
  const humanReviewReason = buildHumanReviewReason(text, result);
  const sourceLedger = buildSourceVerification(text, result, officialChecks);
  const transferBriefItems = buildTransferBrief(text, result, humanReviewReason, playbookReferences, officialChecks, sourceLedger, qs, languageSupport);
  const responderHandoff = buildResponderHandoff(result, humanReviewReason, playbookReferences, actions, qs, languageSupport, officialChecks, sourceLedger, transferBriefItems);
  const responderPacket = buildResponderPacket(result, humanReviewReason, playbookReferences, officialChecks, sourceLedger, transferBriefItems, qs, languageSupport);
  const householdMessage = buildHouseholdMessage(text, result, officialChecks, qs, languageSupport);
  const auditTrace = buildAuditTrace(text, result, humanReviewReason, playbookReferences, officialChecks, sourceLedger, transferBriefItems);
  const structuredExport = buildCaseExport(text, result, humanReviewReason, playbookReferences, officialChecks, sourceLedger, transferBriefItems, qs);
  return {
    risk_level: result.level,
    case_signals: result.signals,
    human_review_reason: humanReviewReason,
    playbook_references: playbookReferences,
    action_plan: actions,
    official_resource_checks: officialChecks,
    source_verification: sourceLedger,
    transfer_brief: transferBriefItems,
    clarifying_questions: qs,
    language_support: languageSupport,
    responder_handoff: responderHandoff,
    responder_packet: responderPacket,
    household_message: householdMessage,
    audit_trace: auditTrace,
    case_export: structuredExport,
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
    `Human review reason:\n${data.human_review_reason.map((item) => `- ${item}`).join("\n")}`,
    `Playbook references:\n${data.playbook_references.map((item) => `- ${item}`).join("\n")}`,
    `Action plan:\n${data.action_plan.map((item, idx) => `${idx + 1}. ${item}`).join("\n")}`,
    `Official resource checks:\n${data.official_resource_checks.map((item) => `- ${item}`).join("\n")}`,
    `Source verification ledger:\n${data.source_verification.map((item) => `- ${item}`).join("\n")}`,
    `Transfer brief:\n${data.transfer_brief.map((item) => `- ${item}`).join("\n")}`,
    `Clarifying questions:\n${data.clarifying_questions.map((item) => `- ${item}`).join("\n")}`,
    `Language support:\n${data.language_support.map((item) => `- ${item}`).join("\n")}`,
    `Responder handoff:\n${data.responder_handoff.map((item) => `- ${item}`).join("\n")}`,
    `Responder packet:\n${data.responder_packet.map((item) => `- ${item}`).join("\n")}`,
    `Household message:\n${data.household_message.map((item) => `- ${item}`).join("\n")}`,
    `Audit trace:\n${data.audit_trace.map((item) => `- ${item}`).join("\n")}`,
    `Structured case export:\n${JSON.stringify(data.case_export, null, 2)}`,
    `Safety boundary: ${data.safety_boundary}`,
  ].join("\n\n");
}

function renderDecisionBrief(data) {
  const review = {
    high: "Immediate escalation",
    medium: "Responder review",
    low: "Preparedness check",
  }[data.risk_level];
  briefReview.textContent = review;
  briefReview.dataset.level = data.risk_level;
  briefPlaybooks.textContent = `${data.playbook_references.length} playbooks`;
  briefRoutes.textContent = `${data.official_resource_checks.length} routes`;
  briefEvidence.textContent = data.audit_trace.includes("human_review_required=true") ? "Audit ready" : "Trace ready";
}

function runTriage() {
  const data = generateResponse(scenario.value);
  lastText = toText(data);
  lastJsonText = JSON.stringify(data.case_export, null, 2);
  lastPacketText = [
    `Risk level: ${data.risk_level}`,
    "Human review reason:",
    ...data.human_review_reason.map((item) => `- ${item}`),
    "Responder packet:",
    ...data.responder_packet.map((item) => `- ${item}`),
    "Source verification ledger:",
    ...data.source_verification.map((item) => `- ${item}`),
    "Transfer brief:",
    ...data.transfer_brief.map((item) => `- ${item}`),
    "Audit trace:",
    ...data.audit_trace.map((item) => `- ${item}`),
  ].join("\n");
  risk.textContent = `Risk level: ${data.risk_level}`;
  risk.dataset.level = data.risk_level;
  renderDecisionBrief(data);
  renderList(signals, data.case_signals);
  renderList(reviewReason, data.human_review_reason);
  renderList(playbook, data.playbook_references);
  renderList(plan, data.action_plan);
  renderList(resources, data.official_resource_checks);
  renderList(sourceVerification, data.source_verification);
  renderList(transferBrief, data.transfer_brief);
  renderList(questions, data.clarifying_questions);
  renderList(language, data.language_support);
  renderList(handoff, data.responder_handoff);
  renderList(packet, data.responder_packet);
  renderList(household, data.household_message);
  renderList(audit, data.audit_trace);
  caseExport.textContent = lastJsonText;
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

copyPacket.addEventListener("click", async () => {
  if (!lastPacketText) return;
  await navigator.clipboard.writeText(lastPacketText);
  copyPacket.textContent = "Copied";
  window.setTimeout(() => {
    copyPacket.textContent = "Copy packet";
  }, 1200);
});

copyJson.addEventListener("click", async () => {
  if (!lastJsonText) return;
  await navigator.clipboard.writeText(lastJsonText);
  copyJson.textContent = "Copied";
  window.setTimeout(() => {
    copyJson.textContent = "Copy JSON";
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
