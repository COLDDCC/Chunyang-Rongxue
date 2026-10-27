# Acceptance criteria · 验

## Before implementation
- Capture product/competitor baseline, comparable user tasks, screenshots or reliable notes, and known uncertainties.
- Resolve the target/version, review surface, release path and protected workflows where applicable. Reuse existing implementation/release authorization; ask only when genuinely missing.
- Agree measurable acceptance criteria for each priority (including rollback plan).

- Classify current capabilities and capture existing check failures before editing. Select applicable criteria using [universal execution](universal-execution.md).

## After implementation
1. User task: core path works; no dead UI or confusing state.
2. Presentation/use: inspect the real artifact under relevant conditions. For interfaces: desktop/mobile, overflow, typography and touch targets; for other objects: actual task context.
3. Accessibility: keyboard, focus, labels, contrast, reduced motion as appropriate.
4. SEO (public pages): indexability, titles, canonical/hreflang, structured data validity where used.
5. Performance: measure, don't assume; distinguish local/dev/prod.
6. Safety: privacy-sensitive data not leaked; dependency/license issues considered.
7. Automated/manual tests: command, environment, result and failures recorded.
8. Side-by-side: before vs after, difference and remaining disadvantage.
9. Review and release: provide a verified accessible review surface; label unavailable previews pending. When release is applicable and authorized, verify the actual distributed/operational version. A commit/PR or upload alone is insufficient.
10. Rollback: reversibility and responsible follow-up documented.

Classify failures as introduced, pre-existing, stale-check or environment-limited, with evidence and disposition. Do not weaken checks to manufacture a pass. See universal execution for completion states.

Outcomes: PASS / FAIL / UNKNOWN / NOT_APPLICABLE. UNKNOWN is not PASS. Blockers override aggregate score.

Report evidence honestly: implemented != tested != merged != deployed. Avoid claims like "CI green" or "fully deployed" without checking.
