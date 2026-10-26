# Labelled estimates · 估算有据

Many figures a reader needs cannot be known in advance: live prices, airfares, hotel rates, individual medication doses, exchange rates, waiting times. Leaving them out makes a page useless; inventing precise numbers makes it misleading. A labelled estimate is the middle path.

## Estimate vs fabrication
| Allowed: labelled estimate | Not allowed: fabrication |
|---|---|
| A **range** wide enough to be honest ("US$70–180 per night") | A falsely precise single number ("US$127 per night") with no basis |
| States its **basis** (public fare comparison, published price list, typical clinical timeline, internal pricing model) | No basis, or a basis that does not exist |
| Carries an **as-of date** | Undated, implying it is current forever |
| Discloses what replaces it ("final price per written quote") | Presented as a quote, guarantee, measurement or statistical average |
| Rounded to the precision the basis supports | Spurious decimals that imply measurement |

Never estimate success rates, medical outcomes, rankings, traffic, savings percentages or legal status. These require cited evidence or must be omitted.

## Writing an estimate
1. Choose the reader's question ("how much will the trip cost in total?") and the components.
2. For each component find the best available basis. Prefer: official price lists > published comparison data > the operator's internal model > reasoned assumption. Record the source URL when one exists.
3. Give a range. Combine component ranges by adding lows and highs; keep scenario tiers (budget / typical / comfortable) consistent with the overall range.
4. Show local currency next to foreign currency with the rate and its date.
5. Disclose once, clearly, near the figure; collect the full data note at the end instead of repeating disclaimers in every section.
6. Run `python3 scripts/check_numbers.py page.md` so every total equals its parts in every copy of the figure.

## In the report
Record each estimate in the optional `estimates` array of the audit JSON:

```json
{"id": "e1", "claim": "Round-trip flight, Shanghai–Saipan, one adult",
 "value": "CNY 3,000–6,500", "basis": "Public fare comparison range, one stop",
 "as_of": "2026-10-26", "disclosure": "Estimate; booking-day fare applies",
 "sources": ["https://www.example.com/fares"]}
```

`audit.py` rejects estimates without basis, as-of date or disclosure. It cannot judge whether the basis is reasonable; a human reviewer must.

## Evidence levels still apply
Competitor observations keep E1/E2/E3. An estimate is about **our own published figures**, not about competitors. An E3 hypothesis about what users want is still validated before P0 implementation; a labelled estimate of a hotel rate is not a hypothesis and may ship with its disclosure.
