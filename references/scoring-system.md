# Evidence-based scoring

## Select a rubric first

The dimensions below are defaults for digital products, not a universal definition of quality. For services, processes, physical objects or other experiences, declare suitable dimensions and measures before comparing. Apply gates only where relevant; retain safety, task correctness and material regressions when applicable. Explain N/A. For custom narrative rubrics use the same evidence, coverage and comparable-condition rules. The bundled JSON validator supports only its fixed seven dimensions; do not force-fit unrelated criteria or claim it validates a custom rubric.

## Digital defaults (sum to 100)
| Dimension | Weight |
|---|---:|
| Visual design | 15 |
| Interaction and UX | 20 |
| Functional completeness | 20 |
| Information architecture and content | 15 |
| SEO and discoverability | 10 |
| Performance and mobile experience | 10 |
| Reliability and accessibility | 10 |

Use scores 0–100 for each dimension only with sufficient direct or documented evidence. Weighted result = Σ(weight × score) / Σ(weight) for all **scored** dimensions. Exclude explicitly justified N/A dimensions with zero weight. If missing any applicable dimension, report **partial coverage** and avoid presenting the number as a fully comparable overall score. Capture rationale and evidence for every score. Don't confuse an agent's taste with user research.

Weights may change by use case, but must be declared before comparison, nonnegative, and add to 100. Compare competitors and our product with identical rubric and tasks. Don't announce a ranking if score coverage/conditions differ.

## Default anchors
- 0–19: major failures or unusable.
- 20–39: severe friction, substantial coverage gaps.
- 40–59: usable in places, noticeable problems.
- 60–79: generally effective, identifiable opportunities.
- 80–89: strong, consistent user experience.
- 90–100: unusually polished, demonstrably excellent in tested tasks.

These are provisional judgment anchors, not scientific measurements.

## Hard gates
Never mark accepted if any applicable blocker is unresolved: core task failure; serious security/privacy issue; unusable mobile or keyboard-critical workflow; severe accessibility blocker; materially wrong content/pricing; broken routing/canonicals; major regression or failure to verify deployment. Mark unknown when untested, never silently pass.

## Success measures
Prefer task success, time-to-complete, steps, failures, web vitals, accessibility audits, tests, organic query performance (where appropriate), and genuine feedback. Compare before vs after using dates/devices/conditions.
