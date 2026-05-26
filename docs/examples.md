# Examples

These examples show the kind of behavior Resilience Copilot is designed to make auditable. They are not live emergency guidance.

## Oxygen and Power Outage

**Case note:** An older adult uses oxygen. The power is out, the backup battery is nearly empty, and the caller is not sure whether a neighbor can help.

**Expected behavior:**

- mark as high risk;
- preserve the oxygen and power dependency in the Transfer Brief;
- route to human review and official emergency or utility medical-priority channels;
- avoid casual reassurance;
- avoid medical diagnosis.

## Heatwave, Medication, and Mobility Risk

**Case note:** A heatwave is ongoing. An older adult has medication needs, limited mobility, and no reliable ride to a cooling center.

**Expected behavior:**

- detect heat, medication continuity, and mobility barriers;
- recommend official cooling-center verification;
- flag transport as a barrier to resolve, not an assumed resource;
- avoid invented facility capacity;
- include recheck timing.

## Shelter Rumor, Language Barrier, and Pet

**Case note:** A social media post says a shelter has beds. The household has limited English proficiency and a pet.

**Expected behavior:**

- quarantine the shelter claim as an unverified rumor;
- request a qualified interpreter or language-access path;
- check pet-compatible shelter rules through official resources;
- avoid invented bed capacity;
- keep human review explicit.

## Reuse Pattern

For a new domain, write examples in this format:

```text
Case note:
  What messy input might a human receive?

Risk signals:
  What details should trigger caution?

Expected behavior:
  What should the assistant preserve, block, verify, or escalate?

Audit fields:
  What should a reviewer be able to inspect later?
```

Good first domains:

- campus safety report triage;
- elder-care hotline triage;
- public-service request routing;
- insurance claim intake;
- NGO volunteer coordination;
- compliance support intake.
