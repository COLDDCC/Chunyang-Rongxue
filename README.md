# 春阳融雪 · Chunyang Rongxue

> 博采众长，去芜存菁，融会贯通，青出于蓝。

A reusable competitive advantage fusion and product evolution Agent Skill for websites, content pages, mini programs, SaaS, and digital tools.

See [SKILL.md](SKILL.md) for agent instructions, [the origin story](docs/origin.md), and [the complete workflow](SKILL.md#five-stage-loop-观吸化创验).

**Principle:** learn from many strong products, retain only what serves users, integrate coherent advantages, and verify outcomes instead of claiming unmeasured superiority.

## Quick start

Ask your agent: `使用春阳融雪分析并优化 <产品或仓库 URL>，先出方案再行动。`

The skill supports **Plan** (research without changing code), **Draft** (ready-to-use replacement files without repository access) and **Build** (authorized implementation with evidence and acceptance checks). Use the `content` profile for a single article or landing page.

## What it includes

- Five stages: Observe → Absorb → Transform → Create → Verify
- Six principles: multi-mentor, selective absorption, coherent fusion, innovation, evidence, iterative evolution
- Competitor advantage matrix and evidence grading
- Adjustable, weighted 100-point scorecard with non-negotiable quality gates
- Labelled-estimate rules: give ranges with basis, date and disclosure instead of omitting or inventing figures
- Practical templates, acceptance checks, an offline report validator, a report renderer and a table-total checker

## Install (v1.2.0)

Clone into your agent's skill directory using the matching folder name:

```bash
# Claude Code: personal skills
 git clone https://github.com/COLDDCC/Chunyang-Rongxue.git ~/.claude/skills/chunyang-rongxue
# Codex: personal skills (use this alternative, not both)
 git clone https://github.com/COLDDCC/Chunyang-Rongxue.git ~/.codex/skills/chunyang-rongxue
```

Follow your host's skill discovery rules; copying these files does not prove activation.
Python 3.10+ is sufficient for the audit, renderer and number checker; no runtime dependencies.
Run `python3 -m unittest discover -s tests -v` and
`python3 scripts/audit.py examples/sample-report.json` from the skill root.
For build acceptance add `--strict`; see [contract and exit codes](references/audit-format.md).
The sample is illustrative and deliberately incomplete.

See [evaluation prompts](tests/trigger-prompts.json), [case protocol](examples/case-01/README.md) and the [content-page field case](examples/case-02/README.md).
A positive description review is not a measured trigger rate.
Repository releases can include documentation; agents only need SKILL.md and its linked resources.

## v1.2.0 changes

Lessons from a real content-page run (examples/case-02):
- **Draft mode** for deliverable rewrites without repository access; never acceptance-eligible.
- **Content profile** with page-specific dimension meanings and weights.
- **Labelled estimates** (rule 7): ranges with basis, as-of date and disclosure are allowed and
  validated; fabrication, false precision and estimated outcomes are not.
- **Business goal** (objective, conversion action, metric) recorded alongside the user job.
- `scripts/check_numbers.py` verifies Markdown table totals; it caught a real drift in case-02.
- `render_report.py` now renders summary, business goal and estimates, removing the duplicate
  hand-written report.
- Competitor discovery: SEO-spam filtering and platform-gated sources (screenshots as E1).
- Lite path for single-page work; three more routing fixtures.
All v1.1 reports remain valid.

## v1.1.0 changes

Fix explicit N/A coverage, prevent Plan acceptance, and add strict build exit codes.
Add trace validation, JSON Schema, Markdown rendering, Chinese triggers, 16 routing
fixtures, regression evidence and a no-evidence forward test. Existing report JSON
remains valid; Plan acceptance behavior is intentionally corrected. Schema QA uses
`jsonschema==4.23.0` as a development-only dependency (installed in CI).
A full external product comparison and measured trigger rate remain pending.

Licensed under [MIT](LICENSE).
