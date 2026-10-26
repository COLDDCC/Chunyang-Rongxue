---
name: chunyang-rongxue
description: 春阳融雪：用于竞品分析、学习竞品优点、融合多家优势并验证产品或内容页改进。适用于“先学竞品再超越对手”“参考同行优化这篇文章/落地页/指南页”等请求；不用于单纯翻译、局部修错或不涉及竞品的常规任务。 Research competing digital products or content pages, extract and integrate their strongest verified advantages, and improve websites, articles, landing pages, mini programs, SaaS, or tools using a measurable plan/draft/build workflow. Use when the user asks to learn from competitors, surpass rival products or pages, optimize UI/UX, content, SEO, conversion, performance, or conduct a multi-competitor audit.
---
# 春阳融雪 · Chunyang Rongxue

> 博采众长，去芜存菁，融会贯通，青出于蓝。
> Competitive Advantage Fusion & Product Evolution.

## Non-negotiable intent
Absorb **principles**, not blindly copied screens, protected assets, source code, brand identity, or content. Build a cohesive product which helps its users more effectively. Never call a product "best" based solely on subjective impressions. Optimize for lower cognitive load, faster task completion, clear first-screen answers, smooth interaction, reliability, and measurable quality.

## Activation & input
Identify: product URL/repository, target users, primary job-to-be-done, **business goal and conversion action** (e.g. "book a consultation"), competitors (if supplied), platform, current constraints, available data, deployment permissions. Infer what is safe to infer and explicitly mark uncertainties. Pick a **profile**: `product` (apps, tools, SaaS, sites as a whole) or `content` (a single article, guide, landing or pricing page). See [content pages](references/content-pages.md).

## Modes
- **Plan:** analyze, benchmark, score when there is sufficient evidence, prioritize a staged proposal, and present acceptance criteria. Do not edit or ship.
- **Draft:** produce ready-to-use replacement files (rewritten page, copy, component, config) without repository access or deployment. Default when the user asks to "optimize/rewrite this article/page" and no repository is available. Drafts are labelled *planned*, never *implemented* or *deployed*.
- **Build:** execute approved plan, make focused changes, run tests, capture verifiable results, and provide preview or production URLs only when verified. Record rollback guidance. Never assume git push equals successful deployment.

Start in **Plan** unless the request clearly asks for a deliverable (then **Draft**). **Build** only after authorization; respect "plan first" instructions and any restriction on publishing or deployment.

## Five-stage loop (观·吸·化·创·验)
1. **Observe / 观** — Inspect the current product and relevant competitors. Use multiple role-model competitors by dimension. Separate directly observed evidence from inference. Filter search spam and note platform-gated sources. See [competitor discovery](references/competitor-discovery.md).
2. **Absorb / 吸** — Capture actual advantages, user mechanisms, disadvantages, trade-offs, and applicability. Record source URL, observation date, screenshots where possible, and confidence. See [advantage extraction](references/advantage-extraction.md).
3. **Transform / 化** — Filter irrelevant features; integrate a consistent visual language, information architecture, content strategy, and interaction model. See [design fusion](references/design-fusion.md).
4. **Create / 创** — Prioritize differentiators and implement only authorized changes. Prefer faster tasks and a coherent small surface over feature sprawl. Fill data gaps with **labelled estimates**, not silence or fabrication. Respect copyright, licensing, accessibility, privacy, and platform policies.
5. **Verify / 验** — Compare before/after against user tasks, quality gates, tests, measurements, and accessible previews. Run `scripts/check_numbers.py` on any drafted page with tables of figures. Never fabricate scores or claim deployment without proof. See [acceptance criteria](references/acceptance-criteria.md).

## Seven rules
1. 多师制: learn from multiple leaders, chosen for their strengths rather than fame.
2. 去芜存菁: do not inherit competitors' bloat, friction, dark patterns, or weak accessibility.
3. 融会贯通: synthesize into one understandable design system; avoid a collage of interfaces.
4. 反向创新: improve at least one important task beyond the reference, where verified.
5. 数据验收: compare observed metrics, user flows, and test evidence; label unmeasured claims.
6. 持续进化: establish a baseline, maintain regression checks, and learn across iterations.
7. 估算有据: when a figure the reader needs is unknowable in advance (live prices, fares, individual dosing), give a reasonable **range with basis, date and disclosure** instead of omitting it. Estimating is allowed; disguising an estimate as a quote, a measurement or a guarantee is not. See [estimates](references/estimates.md).

## Default product preferences (override when product/user requires)
- First screen should answer the primary user question or offer direct task entry.
- Minimize useless text; favor structured, scannable, interactive information where it reduces friction.
- Prioritize usable mobile layouts, accessible controls, good perceived speed, readable type, and meaningful visuals.
- Do not sacrifice working features or SEO just to make screenshots prettier.
- Consider each locale's native usage instead of literal machine translation (local currency next to foreign prices, local platforms, local units).
- Pages that exist to start an offline conversation should make the next step concrete ("send your report for a personal estimate"), not merely "contact us".

## Scorecard
Use [scoring system](references/scoring-system.md). Product baseline weights: visual 15, UX 20, functionality 20, content/IA 15, SEO 10, performance/mobile 10, reliability/accessibility 10. Content profile weights and dimension meanings are in [content pages](references/content-pages.md). Every dimension scored 0–100 **only if evidenced**; weighted overall = sum(weight × score) / sum(weights). Keep missing dimensions unscored, not zero or imaginary. When coverage is partial, say so in words next to the number. Hard quality gates can block acceptance despite a high numerical score.

## Deliverables
Use [report template](assets/report-template.md) and [matrix template](assets/advantage-matrix.csv). Output:
- A one-screen summary: primary job, current weakness, strongest opportunity, business goal.
- Competitive advantage matrix with evidence, transferability, risks, and original synthesis.
- Prioritized roadmap (impact, effort, dependencies, success criteria), separately for Plan and Build.
- In Draft/Build: the changed files themselves, plus a list of labelled estimates used.
- Before/after quality gates, test results, unresolved risks, evidence links, and rollback plan.
- Clearly distinguish **observed**, **inferred**, **estimated**, **planned**, **implemented**, **tested**, and **deployed**.

### Lite path (single page, quick turnaround)
For one article or landing page, the JSON report is optional. Deliver: the one-screen summary, 3–6 advantages with source URLs, the drafted page, its labelled estimates, and a passing `check_numbers.py` run. Use the full report when comparing several products or when results feed acceptance CI.

For repeatability validate report JSON using `python3 scripts/audit.py path/to/report.json`. Use `--strict` in acceptance CI (build only; exit 3 when blocked). Optional `summary`, `business_goal`, `estimates`, `advantages` and `roadmap` fields connect observations to implementation and success criteria; `python3 scripts/render_report.py report.json report.md` turns them into a complete Markdown report. Schema: [report schema](schema/report.schema.json). Contract and examples: [audit format](references/audit-format.md). The scripts validate structure and arithmetic, not the truth of observations.

The name's cultural inspiration and important distinction between the novel and this metaphor are recorded in [origin](docs/origin.md).
