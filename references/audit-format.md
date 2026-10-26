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

Scores may be omitted for unassessed dimensions. Scores require a nonblank evidence field. Validator refuses unsupported status values and blocking FAIL; prints whether assessment has full coverage and is eligible for acceptance. It **cannot verify evidence truth** or automatically measure production UX.

Run: `python3 scripts/audit.py examples/sample-report.json`.
