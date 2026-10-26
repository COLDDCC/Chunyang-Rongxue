#!/usr/bin/env python3
"""Validate a Chunyang Rongxue audit report. Standard library only."""
import argparse
import json
import math
import sys
from pathlib import Path
from datetime import date
from urllib.parse import urlparse

DIMENSIONS = ("visual", "ux", "functionality", "content", "seo", "performance_mobile", "reliability_accessibility")
GATES = ("core_task", "security_privacy", "mobile_accessibility", "content_correctness", "technical_seo", "regressions", "deployment")
STATES = ("pass", "fail", "unknown", "not_applicable")
MODES = ("plan", "draft", "build")
PROFILES = ("product", "content")
SUMMARY_FIELDS = ("primary_job", "current_weakness", "strongest_opportunity", "innovation_hypothesis", "shortest_success_path")
GOAL_FIELDS = ("objective", "conversion_action", "success_metric")
ESTIMATE_FIELDS = ("id", "claim", "value", "basis", "as_of", "disclosure")

def validate(report):
    errors = []
    if not isinstance(report, dict):
        return ["Report must be an object"], None
    if report.get("mode") not in MODES:
        errors.append("mode must be plan, draft or build")
    if report.get("profile", "product") not in PROFILES:
        errors.append("profile must be product or content")
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
    excluded = set()
    for key, item in scores.items():
        if not isinstance(item, dict):
            errors.append(f"{key}: score entry must be object")
            continue
        na = item.get("not_applicable", False)
        if not isinstance(na, bool):
            errors.append(f"{key}: not_applicable must be boolean")
        if na is True:
            if weights.get(key) != 0 or item.get("score") is not None:
                errors.append(f"{key}: N/A requires zero weight and no score")
            if not isinstance(item.get("reason"), str) or not item["reason"].strip():
                errors.append(f"{key}: N/A requires a reason")
            excluded.add(key)
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
    errors.extend(validate_extensions(report))
    if errors:
        return errors, None
    covered_weight = sum(weights[k] for k in scored)
    partial = sum(weights[k] * v for k, v in scored.items()) / covered_weight if covered_weight else None
    coverage = bool(scored) and set(scored) == set(DIMENSIONS) - excluded
    ready = coverage and all(v in {"pass", "not_applicable"} for v in gates.values())
    acceptance = report["mode"] == "build" and ready
    mode = report["mode"]
    if mode == "build":
        status = "acceptance_eligible" if acceptance else "blocked"
    else:
        status = f"{mode}_complete" if ready else f"{mode}_incomplete"
    return [], {"scored_dimensions": len(scored), "coverage": "full" if coverage else "partial",
                "weighted_score": round(partial, 2) if partial is not None else None,
                "acceptance_eligible": acceptance,
                "assessment_status": status,
                "profile": report.get("profile", "product"),
                "estimates": len(report.get("estimates", [])),
                "not_applicable_dimensions": sorted(excluded),
                "covered_weight": covered_weight,
                "failed_gates": [k for k, v in gates.items() if v == "fail"],
                "unknown_gates": [k for k, v in gates.items() if v == "unknown"]}

def _is_date(value):
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def validate_narrative(report):
    """Optional summary, business goal and labelled estimates (v1.2)."""
    errors = []
    summary = report.get("summary")
    if summary is not None:
        if not isinstance(summary, dict) or set(summary) - set(SUMMARY_FIELDS):
            errors.append("summary must be an object with known fields only")
        elif any(not _text(v) for v in summary.values()):
            errors.append("summary fields must be nonempty strings")
    goal = report.get("business_goal")
    if goal is not None:
        if not isinstance(goal, dict) or any(not _text(goal.get(f)) for f in GOAL_FIELDS):
            errors.append("business_goal requires nonempty objective, conversion_action and success_metric")
    estimates = report.get("estimates", [])
    if not isinstance(estimates, list):
        return errors + ["estimates must be an array"]
    seen = set()
    for item in estimates:
        if not isinstance(item, dict):
            errors.append("estimate must be object")
            continue
        for field in ESTIMATE_FIELDS:
            if not _text(item.get(field)):
                errors.append(f"estimate: nonempty {field} required")
        if item.get("id") in seen:
            errors.append("duplicate estimate id")
        seen.add(item.get("id"))
        if not _is_date(item.get("as_of")):
            errors.append("estimate: as_of must be YYYY-MM-DD")
        sources = item.get("sources", [])
        if not isinstance(sources, list) or any(not isinstance(u, str) or urlparse(u).scheme not in {"http", "https"} or not urlparse(u).netloc for u in sources):
            errors.append("estimate: sources must be HTTP(S) URLs")
    return errors


def validate_extensions(report):
    """Validate optional traceable advantages/roadmap without requiring verbose reports."""
    errors = validate_narrative(report)
    advantages = report.get("advantages", [])
    roadmap = report.get("roadmap", [])
    if not isinstance(advantages, list) or not isinstance(roadmap, list):
        return ["advantages and roadmap must be arrays"]
    ids = {}
    for item in advantages:
        if not isinstance(item, dict):
            errors.append("advantage must be object")
            continue
        for field in ("id", "source_url", "observed_at", "evidence_level", "transfer_decision", "user_mechanism", "our_synthesis", "success_metric"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"advantage: nonempty {field} required")
        identifier = item.get("id")
        if isinstance(identifier, str):
            if identifier in ids:
                errors.append("duplicate advantage id")
            ids[identifier] = item
        url = urlparse(item.get("source_url") if isinstance(item.get("source_url"), str) else "")
        if url.scheme not in {"https", "http"} or not url.netloc:
            errors.append("advantage: source_url must be HTTP(S) URL")
        try:
            value = item.get("observed_at")
            if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
                raise ValueError()
        except (ValueError, TypeError):
            errors.append("advantage: observed_at must be YYYY-MM-DD")
        if item.get("evidence_level") not in ("E1", "E2", "E3"):
            errors.append("advantage: invalid evidence_level")
        if item.get("transfer_decision") not in ("Adopt", "Adapt", "Experiment", "Reject"):
            errors.append("advantage: invalid transfer_decision")
    task_ids = set()
    for item in roadmap:
        if not isinstance(item, dict):
            errors.append("roadmap task must be object")
            continue
        for field in ("id", "task", "success_criteria"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"roadmap: nonempty {field} required")
        identifier = item.get("id")
        if isinstance(identifier, str):
            if identifier in task_ids:
                errors.append("duplicate roadmap id")
            task_ids.add(identifier)
        if item.get("priority") not in ("P0", "P1", "P2"):
            errors.append("roadmap: invalid priority")
        if item.get("kind") not in ("validate", "implement"):
            errors.append("roadmap: kind must be validate or implement")
        refs = item.get("advantage_ids", [])
        if not isinstance(refs, list) or any(not isinstance(x, str) or x not in ids for x in refs):
            errors.append("roadmap: unknown advantage reference")
            continue
        if item.get("kind") == "implement" and any(ids[x].get("transfer_decision") == "Reject" for x in refs):
            errors.append("roadmap: cannot implement rejected advantage")
        if item.get("priority") == "P0" and item.get("kind") == "implement" and refs and all(ids[x].get("evidence_level") == "E3" for x in refs):
            errors.append("roadmap: E3-only P0 requires validation before implementation")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report")
    parser.add_argument("--strict", action="store_true", help="Exit 3 unless a build report is acceptance eligible")
    args = parser.parse_args(argv)
    try:
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Cannot load report: {exc}", file=sys.stderr)
        return 2
    errors, result = validate(report)
    if errors:
        print("INVALID\n" + "\n".join("- " + e for e in errors), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 3 if args.strict and not result["acceptance_eligible"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
