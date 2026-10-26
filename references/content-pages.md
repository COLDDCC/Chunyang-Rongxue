# Content pages profile · 内容页

Use `"profile": "content"` when the target is a single article, guide, pricing explainer or landing page rather than a whole product. The seven score keys stay the same so reports remain comparable and machine-valid, but they mean different things.

## Dimension meanings and default weights
| Key | Meaning for a content page | Weight |
|---|---|---:|
| `visual` | Scannability: hierarchy, tables, whitespace, mobile reading comfort | 10 |
| `ux` | Answer-first: is the reader's question answered on the first screen; navigation, repetition, CTA placement | 20 |
| `functionality` | Intent coverage: does the page answer the full question (including totals, timelines, local currency) and link to tools that finish the job | 20 |
| `content` | Accuracy, sourcing, dates, internal consistency, authorship and review | 20 |
| `seo` | Title/description match search intent, canonical/hreflang, structured data, internal links, long-tail FAQ | 15 |
| `performance_mobile` | Load and layout on real phones | 10 |
| `reliability_accessibility` | Contrast, headings order, link text, table semantics | 5 |

Declare the weights before comparing. Adjust only with a stated reason.

## Business goal
Content pages usually exist to start something: a consultation, sign-up or purchase. Record `business_goal` (`objective`, `conversion_action`, `success_metric`). Judge CTAs by whether the next step is concrete and placed where the reader becomes ready (usually right after the cost or decision table), not by how many there are.

## Checklist
1. First screen: the answer in one block (range, local currency, what is excluded), then one obvious next step.
2. One table per decision; totals that add up (`scripts/check_numbers.py`).
3. Cover the questions readers ask next: total including travel or add-ons, time required, recurring costs, what changes the price.
4. Fill unknowable numbers with [labelled estimates](estimates.md); never with silence or false precision.
5. One clear data note instead of repeated disclaimers; sources and as-of dates at the end.
6. FAQ only for questions the body does not already answer word for word; target long-tail search intent.
7. Internal links inline where the reader needs them, not only in a footer list.
8. YMYL topics (health, money, legal): cite regulators or professional bodies; add a named reviewer only if a real, verifiable one exists.

## Verifying without repository access
Fetch tools may not expose `<head>`. Mark JSON-LD, hreflang and canonical status UNKNOWN until checked in source or with a rich results test; do not infer absence from a text extraction.
