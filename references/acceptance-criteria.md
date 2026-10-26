# Acceptance criteria · 验

## Before implementation
- Capture product/competitor baseline, comparable user tasks, screenshots or reliable notes, and known uncertainties.
- Confirm target branch, protected workflows, permission to implement and permission to deploy.
- Agree measurable acceptance criteria for each priority (including rollback plan).

## After implementation (Build) / after drafting (Draft: items 1, 3–4 and 7–9 apply to the draft; release items do not)
1. User task: core path works; no dead UI or confusing state.
2. Layout: desktop and realistic mobile viewports; overflow/typography/touch targets.
3. Accessibility: keyboard, focus, labels, contrast, reduced motion as appropriate.
4. SEO (public pages): indexability, titles, canonical/hreflang, structured data validity where used.
5. Performance: measure, don't assume; distinguish local/dev/prod.
6. Safety: privacy-sensitive data not leaked; dependency/license issues considered.
7. Automated/manual tests: command, environment, result and failures recorded.
8. Numeric consistency: every total equals its parts in every copy of a figure (`python3 scripts/check_numbers.py page.md`); local-currency conversions state rate and date; estimates carry basis, date and disclosure ([estimates](estimates.md)).
9. Side-by-side: before vs after, difference and remaining disadvantage.
10. Release: provide actual commit/PR and deployment URL plus confirmation **only after verification**.
11. Rollback: reversibility and responsible follow-up documented.

Outcomes: PASS / FAIL / UNKNOWN / NOT_APPLICABLE. UNKNOWN is not PASS. Blockers override aggregate score.

Report evidence honestly: implemented != tested != merged != deployed. Avoid claims like "CI green" or "fully deployed" without checking.
