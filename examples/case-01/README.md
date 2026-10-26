# Case 01: validation baseline (real code; limited scope)

This is an actual regression study of Chunyang Rongxue's audit tool, not a
completed competitor/product redesign case or proof that this Skill outperforms a baseline.
Baseline: commit abf4163. Run from the repository root with Python 3.10+.

| Reproducible input | Baseline | Revised |
|---|---|---|
| Plan + complete scores + pass gates | acceptance eligible | plan_complete; ineligible |
| Private tool: SEO N/A, zero weight, redistribute to UX | partial; ineligible | full applicable coverage; eligible in build |
| Build + failed gate | exit 0 | exit 0 normally; exit 3 with --strict |
| Missing score at zero weight | partial | partial (not silently N/A) |
| E3-only P0 implementation | no trace validation | invalid; validate first |

Reproduce: `python3 -m unittest discover -s tests -v`.
Inspect `tests/test_boundaries.py` for exact inputs and assertions.
No UI screenshots apply to this CLI regression. No production UX or SEO improvement is claimed.

## Pending product comparison

For a full external case, freeze one small authorized product surface and its
primary task. Save dated competitor evidence, matching viewports, baseline,
changes and after screenshots. Give two fresh agents the same task, tools,
budget and frozen inputs; one uses this Skill, one receives the task alone.
Compare unsupported claims, useful transferable observations, completed changes,
measured task success and token/time costs. Record failures as well as successes.
Do not call this pending experiment complete or infer traffic gains from screenshots.

## Forward test: no evidence available

`offline-plan.json` is a synthetic task produced by an independent agent using
this Skill: plan improvements to a private expense tool without accessible
product/competitor pages. It is **not** an observed audit of a real expense product.
The result retains null scores, unknown gates, SEO N/A, and unverified candidate
hypotheses separately from observed advantages. Audit exits 0 with
`plan_incomplete`, null weighted score and acceptance ineligible. No external
product, traffic or trigger-rate claim follows from this single forward test.
