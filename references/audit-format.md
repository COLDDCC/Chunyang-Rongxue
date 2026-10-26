# Offline audit JSON contract

The stdlib-only validator `scripts/audit.py` reads a JSON report:

```json
{
  "product": "Example tool",
  "mode": "plan",
  "weights": {
    "visual": 15, "ux": 20, "functionality": 20, "content": 15,
    "seo": 10, "performance_mobile": 10, "reliability_accessibility": 10
  },
  "scores": {
    "visual": {"score": 75, "evidence": "Observed example screenshot and tasks"},
    "ux": {"score": null, "evidence": ""}
  },
  "gates": {
    "core_task": "unknown",
    "security_privacy": "unknown",
    "mobile_accessibility": "unknown",
    "content_correctness": "unknown",
    "technical_seo": "not_applicable",
    "regressions": "unknown",
    "deployment": "not_applicable"
  }
}
```

Scores may be omitted for unassessed dimensions. Scores require a nonblank evidence field. Validator rejects unsupported status values. A FAIL blocks acceptance but does not invalidate the report; use --strict for a nonzero acceptance exit code. It **cannot verify evidence truth** or automatically measure production UX.

Run: `python3 scripts/audit.py examples/sample-report.json`.

## v1.1 rules and CI

N/A score: `{"not_applicable": true, "reason": "Private employee tool"}`.
Its weight must be zero and its score absent or null. Redistribute weights to total
100 before comparison. Explicit N/A is excluded from coverage; a missing score is
still unknown even at zero weight. At least one scored applicable dimension is required.

Plan never sets `acceptance_eligible`; complete coverage and resolved gates produce
`assessment_status: plan_complete`, otherwise `plan_incomplete`. This status only
summarizes the scorecard/gates, not the completeness of the whole written proposal.
Build can be `acceptance_eligible` or `blocked`. Eligibility is not proof of deployment.
Do not mark gates pass without evidence; explain gate N/A and evidence in the narrative.

Exit codes: 0 = structurally valid report (may have blockers); 1 = invalid contract;
2 = unreadable/invalid JSON or CLI usage; 3 = valid report blocked by `--strict`.
Run `python3 scripts/audit.py report.json --strict` for **build acceptance CI**.
Plans and the intentionally partial sample do not belong in acceptance CI.

[JSON Schema](../schema/report.schema.json) supplies editor shape validation.
The Python validator additionally checks weight sums, N/A weights, references and
priority relationships. Run it even when schema validation passes.

## v1.2 additions (all optional, v1.1 reports stay valid)

- `mode` may be `draft`: replacement files delivered without repository access. Draft never sets
  `acceptance_eligible`; status is `draft_complete` or `draft_incomplete`.
- `profile`: `product` (default) or `content`; see [content pages](content-pages.md).
- `summary`: `primary_job`, `current_weakness`, `strongest_opportunity`, `innovation_hypothesis`,
  `shortest_success_path` (nonempty strings; unknown keys rejected).
- `business_goal`: `objective`, `conversion_action`, `success_metric` (all required when present).
- `estimates`: array of `id`, `claim`, `value`, `basis`, `as_of` (YYYY-MM-DD), `disclosure`, optional
  `sources` (HTTP(S) URLs). See [estimates](estimates.md).

`render_report.py` renders summary, business goal and estimates, so the narrative report no longer
needs to be written separately. `check_numbers.py page.md` checks Markdown table totals
(exit 0 consistent, 1 mismatch, 2 unreadable).

## Optional structured trace

Add `advantages` with unique `id`, HTTP(S) `source_url`, `observed_at` (YYYY-MM-DD),
`evidence_level` (E1/E2/E3), `transfer_decision` (Adopt/Adapt/Experiment/Reject),
`user_mechanism`, `our_synthesis`, and `success_metric`.

Add `roadmap` with unique `id`, `task`, `priority` (P0/P1/P2), `kind`
(validate/implement), `success_criteria`, and optional `advantage_ids` referencing
existing advantages. An implementation cannot reference a rejected advantage.
E3-only evidence cannot justify P0 implementation; P0 validation is allowed.
Mixed evidence still needs human judgment that the stronger source supports the task.

Keep JSON as the source for these tables; do not maintain a separate CSV copy.
CSV/Markdown templates remain available for lightweight narrative-only work.
Generate tables with `python3 scripts/render_report.py report.json report.md`.
Keep screenshots, test logs, source excerpts and long-form rationale as linked evidence;
never invent evidence merely to satisfy required fields.
