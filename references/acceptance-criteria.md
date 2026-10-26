# Acceptance criteria · 验

## Before implementation
- Capture product/competitor baseline, comparable user tasks, screenshots or reliable notes, and known uncertainties.
- Confirm target branch, protected workflows, permission to implement and permission to deploy.
- Agree measurable acceptance criteria for each priority (including rollback plan).

## After implementation
1. User task: core path works; no dead UI or confusing state.
2. Layout: desktop and realistic mobile viewports; overflow/typography/touch targets.
3. Accessibility: keyboard, focus, labels, contrast, reduced motion as appropriate.
4. SEO (public pages): indexability, titles, canonical/hreflang, structured data validity where used.
5. Performance: measure, don't assume; distinguish local/dev/prod.
6. Safety: privacy-sensitive data not leaked; dependency/license issues considered.
7. Automated/manual tests: command, environment, result and failures recorded.
8. Side-by-side: before vs after, difference and remaining disadvantage.
9. Release: provide actual commit/PR and deployment URL plus confirmation **only after verification**.
10. Rollback: reversibility and responsible follow-up documented.

Outcomes: PASS / FAIL / UNKNOWN / NOT_APPLICABLE. UNKNOWN is not PASS. Blockers override aggregate score.

Report evidence honestly: implemented != tested != merged != deployed. Avoid claims like "CI green" or "fully deployed" without checking.
