# E2 vs E6 — Weighted Decision Table

Written 2026-06-19. Final head-to-head before locking the capstone idea.
Weights reflect the user's stated priorities (office-hours): broad recognition,
demo drama, and eval-cleanliness are top (×3); visualization, risk, feasibility,
"clearly an agent" (×2); asset reuse (×1). Scores 1–5 (higher better) are the
assistant's estimates — the user can re-weight.

- **E2 ClaimGuard** — agent that audits medical/insurance bills (EOBs) for errors + drafts appeals. Concierge/Good. Bootstraps WBFA.
- **E6 FamilyOps** — family "mental load" agent: reads messy school emails/forms → daily "action needed" briefing + drafts. Concierge. Bootstraps PAA.

| Dimension (weight) | E2 ClaimGuard | E6 FamilyOps | Winner |
|---|---|---|---|
| Broad recognition / raw engagement (×3) | 5 (r/technology "AI cut hospital bill $195k→$33k with **Claude**" **36,998↑/1,047c** — single highest signal in the whole scan, and it IS the product; + r/HealthInsurance pain cluster 785↑/699↑/418↑) | 5 (parenting cluster, 5,346↑) | tie |
| Demo drama / share-ability (×3) | 5 (recovered $1,300 live) | 3 ("don't miss the permission slip") | E2 |
| Eval cleanliness / ground-truth (×3) | 5 (objective arithmetic + injected real error taxonomy) | 3 ("what counts as an action item" is subjective) | E2 |
| Visualization potential (×2) | 4 (bill markup + appeal + $ reveal) | 4 (morning-briefing card) | tie |
| Policy / privacy risk (×2) | 4 (audit ≠ advice) | 3 (family + child PII) | E2 |
| Solo 17-day feasibility (×2) | 4 (synthetic EOBs easy) | 4 (synthetic school emails) | tie |
| "Clearly an agent" (×2) | 4 (parser+auditor+drafter) | 4 (extractor+briefer+drafter) | tie |
| Existing-asset reuse (×1) | 5 (WBFA trust-gate 1:1) | 4 (PAA Gmail/Cal/Telegram) | E2 |
| **Weighted total (max 90)** | **82** | **67** | **E2** |

## Reading it (UPDATED after opencli deep reads, 2026-06-20)
- **Smoking gun for E2:** r/technology `1ojbymi` — "Grieving family uses AI chatbot to
  cut hospital bill from $195,000 to $33,000 — family says **Claude** highlighted
  duplicative charges, improper coding, and other violations." **36,998↑ / 1,047c** — the
  single highest-engagement signal in the entire research, and it literally IS the E2
  product, built with Claude. Demand + feasibility + public imagination = PROVEN, not
  hypothetical. Corroborating r/HealthInsurance pain cluster: ER denied $30k "not medically
  necessary" (785↑/179c, `1qesut7`), UHC overbilling 10h on phone (699↑, `1qf1txa`),
  118 dunning letters / $5k (418↑, `1u6yi30`).
- That lifts E2's broad-recognition 4→5, erasing E6's only edge. E6 remains strong and
  real (r/Parenting 5,346↑/842c verified via full read — quote confirmed verbatim) but no
  longer leads on any single dimension.
- **The wedge the smoking gun reveals:** since an ad-hoc Claude chat ALREADY cut a bill,
  E2's differentiation is NOT "can AI do this" (proven) but "a reliable, reproducible agent
  with a trustworthy **eval scorecard** + HITL guardrails against hallucinated violations."
  The evaluation harness goes from nice-to-have to the *reason the project exists*.
- **Verdict: E2, decisively (82 vs 67).** Lock it.

## Evidence note
E6 engagement = verified via full opencli thread read (`1qnzyla`, post score 5,342 +
comment tree). E2 demand = re-validated via opencli (the `1ojbymi` Claude thread +
r/HealthInsurance cluster). Caveat: an unscoped "hospital billing error" search returned
off-topic viral noise (Kamala/cats/Epstein); the clean signal is the subreddit-scoped
results above.
