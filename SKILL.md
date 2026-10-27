---
name: chunyang-rongxue
description: 春阳融雪：用于跨领域的竞品与标杆分析、学习优点、融合多家优势并验证产品、服务、流程和实体体验的改进。适用于“先学竞品再超越对手”等请求；不用于单纯翻译、局部修错或不涉及竞品的常规任务。 Research comparable products, services, workflows, tools, content, and physical experiences; extract verified advantages and adapt them through a measurable plan/build workflow. Use when the user asks to learn from competitors, surpass rival products, optimize UI/UX, SEO, performance, or conduct a multi-competitor product audit.
---
# 春阳融雪 · Chunyang Rongxue

> 博采众长，去芜存菁，融会贯通，青出于蓝。
> Competitive Advantage Fusion & Product Evolution.

## Non-negotiable intent
Absorb **principles**, not blindly copied screens, protected assets, source code, brand identity, or content. Build a cohesive product which helps its users more effectively. Never call a product "best" based solely on subjective impressions. Optimize for the defined user outcome, lower cognitive load, effective task completion, reliability, and measurable quality. Treat web, medical, retail, hardware, and other domain practices as conditional adaptations, never universal requirements.

## Activation & input
Identify the object (URL/repository/artifact/process/physical setting), users, primary job, constraints, references, available evidence, and requested result. Infer safe defaults and mark uncertainty. Use **Plan** when the request is analysis or "plan first"; use **Build** when implementation is already authorized. Reuse existing authorization; do not ask again merely because a stage changed. Distinguish permission to inspect, edit, expose a preview, and release. A skill grants none of these by itself.

Read [universal execution](references/universal-execution.md) before planning or building: select applicable criteria, establish baseline, and define the smallest reviewable outcome. Use domain specialists when needed; do not present framework use as domain qualification.

## Five-stage loop (观·吸·化·创·验)
1. **Observe / 观** — Inspect the current object before proposing changes. Classify capabilities as present, inadequate, absent, or unknown; protect verified strengths. Inspect relevant competitors or role models using the same user task. Use multiple role-model competitors by dimension. Separate directly observed evidence from inference. See [competitor discovery](references/competitor-discovery.md).
2. **Absorb / 吸** — Capture actual advantages, user mechanisms, disadvantages, trade-offs, and applicability. Record source URL or offline evidence location, observation date, relevant captures and confidence. See [advantage extraction](references/advantage-extraction.md).
3. **Transform / 化** — Filter irrelevant features; integrate a coherent operating or design model appropriate to the object. Use visual language, information architecture and interaction conventions where relevant. See [design fusion](references/design-fusion.md).
4. **Create / 创** — Prioritize task outcomes and implement only authorized changes as a small, complete, reviewable increment. Prefer faster tasks and a coherent small surface over feature sprawl. Respect copyright, licensing, accessibility, privacy, and platform policies.
5. **Verify / 验** — Compare before/after against user tasks, quality gates, tests, measurements, and accessible previews. Never fabricate scores or claim deployment without proof. See [acceptance criteria](references/acceptance-criteria.md).

## Six rules
1. 多师制: learn from multiple leaders, chosen for their strengths rather than fame.
2. 去芜存菁: do not inherit competitors' bloat, friction, dark patterns, or weak accessibility.
3. 融会贯通: synthesize into one understandable product or operating model; avoid a collage of unrelated practices.
4. 反向创新: improve at least one important task beyond the reference, where verified.
5. 数据验收: compare observed metrics, user flows, and test evidence; label unmeasured claims.
6. 持续进化: establish a baseline, maintain regression checks, and learn across iterations.

## Conditional product preferences (apply only when relevant)
- For interfaces/content, give the main answer or task entry early; for services/physical objects, make the next action, orientation, or handoff clear.
- Minimize useless text; favor structured, scannable, interactive information where it reduces friction.
- Prioritize usable mobile layouts, accessible controls, good perceived speed, readable type, and meaningful visuals.
- Do not sacrifice working features or SEO just to make screenshots prettier.
- Consider each locale's native usage instead of literal machine translation.

## Modes
- **Plan:** analyze, benchmark, score when there is sufficient evidence, prioritize a staged proposal, and present acceptance criteria. Do not edit or ship.
- **Build:** execute approved plan, make focused changes, run tests, capture verifiable results, and provide preview or production URLs only when verified. Record rollback guidance. Never assume git push equals successful deployment.

## Scorecard
Select dimensions and quality gates for the object before comparing; justify N/A and never invent scores to fill a template. Use [scoring system](references/scoring-system.md). For digital products, baseline weights: visual 15, UX 20, functionality 20, content/IA 15, SEO 10, performance/mobile 10, reliability/accessibility 10. Every dimension scored 0–100 **only if evidenced**; weighted overall = sum(weight × score) / sum(weights). Keep missing dimensions unscored, not zero or imaginary. Hard quality gates can block acceptance despite a high numerical score.

## Deliverables
Scale the [report template](assets/report-template.md) and [matrix template](assets/advantage-matrix.csv) to task size; a small change needs a concise delta and evidence, not a compulsory full audit. Output:
- A one-screen summary: primary job, current weakness, strongest opportunity.
- Competitive advantage matrix with evidence, transferability, risks, and original synthesis.
- Prioritized roadmap (impact, effort, dependencies, success criteria), separately for Plan and Build.
- Before/after quality gates, test results, unresolved risks, evidence links, and rollback plan.
- Distinguish evidence type (**observed / inferred / planned**) from delivery status (**implemented / tested / review-ready / user-accepted / released / release-verified**). Record each independently; users may review before or after release when authorized. Never infer user acceptance from passing tests or release verification from a submission.
- End each increment with the actual review surface, result of the task check, limitations, and next step. If delivery is blocked, mark **blocked / pending review**, name the blocker, and provide a safe reviewable fallback when possible. No preview means no claim of visual acceptance.

For repeatability validate report JSON using `python3 scripts/audit.py path/to/report.json`. Use `--strict` in acceptance CI (build only; exit 3 when blocked). Optional `advantages` and `roadmap` fields connect observations to implementation and success criteria; keep narrative concise. Schema: [report schema](schema/report.schema.json). Contract and examples: [audit format](references/audit-format.md). The script validates its fixed digital scorecard and gates, not evidence truth, general-domain suitability, or delivery status. For other objects, use a declared narrative rubric; map to JSON only when its existing dimensions fit honestly. Do not label a non-applicable digital dimension failed or invent a URL for offline evidence.

The name's cultural inspiration and important distinction between the novel and this metaphor are recorded in [origin](docs/origin.md).
