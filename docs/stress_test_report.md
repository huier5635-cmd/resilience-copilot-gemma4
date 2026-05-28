# Stress Test Report

The stress suite is scenario-based because the hackathon did not provide an official training dataset. It checks whether the deterministic safety sidecar preserves the response contract under high-risk case-note variations.

| Case Type | Count | Pass | Fail | Main Risk | Fix |
| --- | ---: | ---: | ---: | --- | --- |
| heat_and_cooling | 3 | 3 | 0 | heat illness and capacity uncertainty | Cooling-center official check and no capacity promise. |
| language_access | 1 | 1 | 0 | unsafe ad hoc interpretation | Qualified interpreter requirement. |
| oxygen_power_or_utility | 3 | 3 | 0 | powered medical device outage | Emergency/utility medical-priority routing plus human review. |
| pet_shelter | 1 | 1 | 0 | invented pet-compatible shelter routing | Animal services or shelter pet desk verification. |
| rumor_or_capacity | 6 | 6 | 0 | unverified shelter capacity | Rumor quarantine and shelter operations confirmation. |
| transport_barrier | 1 | 1 | 0 | unsafe route or transport assumptions | Official logistics routing and flooded-road avoidance. |

## Current Result

Passed 15/15 stress cases.

## Follow-up

Future work should replace these hand-authored stress cases with larger multi-region benchmarks and expert-reviewed annotations.
