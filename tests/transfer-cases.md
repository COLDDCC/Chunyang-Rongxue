# Offline transfer evaluation · 2026-10-27

Protocol: one independent agent, fresh thread, supplied the skill path and two task prompts; no parent reasoning or intended answers. No network, file edits or live changes permitted. Qualitative review only, not trigger accuracy or measured real-world improvement.

## Inputs

1. Coffee shop: improve pickup by learning from role models. Our store has pickup numbers and paper staffing; recorded mean wait 12 minutes. A has a live queue display and records 10 minutes under different peak conditions. B gives clear out-of-stock alternatives. Budget allows one small change. Produce a first reviewable plan.
2. Internal API: learn error recovery. Our client already retries automatically; an old compatibility test failed before any edits. Reference documentation claims idempotency keys, untested. Plan only; no service changes. Propose verification and improvement.

For both: distinguish evidence/unknowns, choose metrics and define acceptance.

## Observed output and assessment

| Scenario | Observed behavior | Assessment |
|---|---|---|
| Coffee shop | Preserved pickup numbers and staffing; did not attribute a two-minute reduction to A's screen because conditions differed | Respected baseline and comparison limits |
| Coffee shop | Proposed checking whether missing alternatives actually cause friction, then a paper substitute card if justified | Selected a small service-specific increment rather than a mandatory website feature |
| Coffee shop | Suggested matched-period observation, decision time, waiting time and error metrics; card sample plus records for review | Task-based review surface; proposed thresholds are hypotheses, not observed effects |
| API | Preserved existing retries; treated idempotency as a documented claim requiring tests | Avoided duplicating existing capability or fabricating validation |
| API | Proposed response-loss, duplicate/concurrent requests, changed payload and key-expiry cases | Used relevant error/recovery scenarios, not SEO/Hero criteria |
| API | Kept the existing compatibility failure unresolved pending diagnosis; did not discard assertions or modify the service | Respected validation integrity and Plan scope |

Limits: two synthetic task prompts, one independent agent, no live trials; physical-product, document, and other-domain transfer remain untested. Routing fixtures are examples, not a measured selection rate. No claim of universal domain expertise or production readiness.
