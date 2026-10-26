#!/usr/bin/env python3
"""Validate a Chunyang Rongxue audit report. Standard library only."""
import json
import math
import sys
from pathlib import Path

DIMENSIONS = ("visual", "ux", "functionality", "content", "seo", "performance_mobile", "reliability_accessibility")
GATES = ("core_task", "security_privacy", "mobile_accessibility", "content_correctness", "technical_seo", "regressions", "deployment")
STATES = {"pass", "fail", "unknown", "not_applicable"}

def validate(report):
    errors = []
    if not isinstance(report, dict):
        return ["Report must be an object"], None
    if report.get("mode") not in {"plan", "build"}:
        errors.append("mode must be plan or build")
    if not isinstance(report.get("product"), str) or not report["product"].strip():
        errors.append("product must be nonempty")
    weights, scores, gates = (report.get(k) for k in ("weights", "scores", "gates"))
    if not isinstance(weights, dict) or set(weights) != set(DIMENSIONS):
        errors.append("weights must specify exactly all seven dimensions")
        weights = {}
    for key in DIMENSIONS:
        v = weights.get(key)
        if isinstance(v, bool) or not isinstance(v, (float, int)) or not math.isfinite(v) or v < 0:
            errors.append(f"invalid weight: {key}")
    if len(weights) == len(DIMENSIONS) and all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in weights.values()):
        if not math.isclose(sum(weights.values()), 100, abs_tol=1e-7):
            errors.append("weights must total 100")
    if not isinstance(scores, dict):
        scores = {}
        errors.append("scores must be object")
    if set(scores) - set(DIMENSIONS):
        errors.append("unknown score dimensions")
    scored = {}
    for key, item in scores.items():
        if not isinstance(item, dict):
            errors.append(f"{key}: score entry must be object")
            continue
        n = item.get("score")
        if n is None:
            continue
        if isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) or not 0 <= n <= 100:
            errors.append(f"{key}: score must be 0–100 or null")
        elif not isinstance(item.get("evidence"), str) or not item["evidence"].strip():
            errors.append(f"{key}: evidence required for scored dimension")
        else:
            scored[key] = n
    if not isinstance(gates, dict) or set(gates) != set(GATES):
        errors.append("gates must specify exactly all seven quality gates")
        gates = {}
    for k in GATES:
        if gates.get(k) not in STATES:
            errors.append(f"invalid gate: {k}")
    if errors:
        return errors, None
    covered_weight = sum(weights[k] for k in scored)
    partial = sum(weights[k] * v for k, v in scored.items()) / covered_weight if covered_weight else None
    coverage = len(scored) == len(DIMENSIONS)
    acceptance = coverage and all(v in {"pass", "not_applicable"} for v in gates.values())
    return [], {"scored_dimensions": len(scored), "coverage": "full" if coverage else "partial",
                "weighted_score": round(partial, 2) if partial is not None else None,
                "acceptance_eligible": acceptance,
                "failed_gates": [k for k, v in gates.items() if v == "fail"],
                "unknown_gates": [k for k, v in gates.items() if v == "unknown"]}

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/audit.py report.json", file=sys.stderr)
        return 2
    try:
        report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Cannot load report: {exc}", file=sys.stderr)
        return 2
    errors, result = validate(report)
    if errors:
        print("INVALID\n" + "\n".join("- " + e for e in errors), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
