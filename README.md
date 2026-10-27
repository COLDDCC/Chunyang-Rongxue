# 春阳融雪 · Chunyang Rongxue

> 博采众长，去芜存菁，融会贯通，青出于蓝。

A reusable competitive advantage fusion and product evolution Agent Skill for products, services, workflows, tools, content, and physical experiences. Apply domain-specific practices only where relevant.

See [SKILL.md](SKILL.md) for agent instructions, [the origin story](docs/origin.md), and [the complete workflow](SKILL.md#five-stage-loop-观吸化创验).

**Principle:** learn from many strong products, retain only what serves users, integrate coherent advantages, and verify outcomes instead of claiming unmeasured superiority.

## Quick start

Ask your agent: `使用春阳融雪分析并优化 <产品或仓库 URL>，先出方案再行动。`

The skill supports **Plan** (research without changing code) and **Build** (authorized implementation with evidence and acceptance checks).

## What it includes

- Five stages: Observe → Absorb → Transform → Create → Verify
- Six principles: multi-mentor, selective absorption, coherent fusion, innovation, evidence, iterative evolution
- Competitor advantage matrix and evidence grading
- Adjustable, weighted 100-point scorecard with non-negotiable quality gates
- Practical templates, acceptance checks, and an offline report validation script

## Install (v1.2.0)

Clone into your agent's skill directory using the matching folder name:

```bash
# Claude Code: personal skills
 git clone https://github.com/COLDDCC/Chunyang-Rongxue.git ~/.claude/skills/chunyang-rongxue
# Codex: personal skills (use this alternative, not both)
 git clone https://github.com/COLDDCC/Chunyang-Rongxue.git ~/.codex/skills/chunyang-rongxue
```

Follow your host's skill discovery rules; copying these files does not prove activation.
Python 3.10+ is sufficient for the audit and renderer; no runtime dependencies.
Run `python3 -m unittest discover -s tests -v` and
`python3 scripts/audit.py examples/sample-report.json` from the skill root.
For build acceptance add `--strict`; see [contract and exit codes](references/audit-format.md).
The sample is illustrative and deliberately incomplete.

See [evaluation prompts](tests/trigger-prompts.json) and [case protocol](examples/case-01/README.md).
A positive description review is not a measured trigger rate.
Repository releases can include documentation; agents only need SKILL.md and its linked resources.

## v1.2.0 changes

Add a [universal execution protocol](references/universal-execution.md): existing-capability inventory, task-based benchmarking, object-specific criteria, baseline failure classification, smallest reviewable increments and separate delivery states. Keep web/medical/media practices conditional. Expand routing fixtures and offline transfer scenarios; fixtures are not measured trigger accuracy. The existing JSON contract remains unchanged and validates digital scorecards only.

## v1.1.0 changes

Fix explicit N/A coverage, prevent Plan acceptance, and add strict build exit codes.
Add trace validation, JSON Schema, Markdown rendering, Chinese triggers, 16 routing
fixtures, regression evidence and a no-evidence forward test. Existing report JSON
remains valid; Plan acceptance behavior is intentionally corrected. Schema QA uses
`jsonschema==4.23.0` as a development-only dependency (installed in CI).
A full external product comparison and measured trigger rate remain pending.

Licensed under [MIT](LICENSE).
