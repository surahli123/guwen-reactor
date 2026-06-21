# Water Bottle Finance Analyzer (WBFA) → Capstone bootstrap + recommendation

Written 2026-06-19 after a read-only Explore map of `~/Documents/projects/water_bottle_finance_analyzer/`.

## What WBFA actually is (the name is misleading)
A **"Boss Briefing Finance Agent" / "Operating Profit Trust Audit"** — a CEO-facing monthly
finance analyzer for Chinese e-commerce. Ingests multi-sheet Excel (sales/inventory/cost/
marketing/bank) → deterministic clean → operating-profit formula engine → **anomaly ranking
by business impact** → **trust-threshold gate** → delivers either a *Trusted Conclusion*
(evidence strong) or a *Diagnostic Report* (gaps named). FastAPI + pandas + openpyxl.
**Not LLM-driven, Excel-only, Chinese-coupled.** Has an OpenTelemetry tracing option + an
append-only SQLite audit log + a privacy/PII layer + a regression **eval harness**.

## The key insight
WBFA's reusable soul is exactly the **evaluation / trust layer** the demand research flagged
as the #1 demand (T1/T7/T8) and the user's professional edge:
- **Trust gate** (source coverage + formula coverage + reconciliation + confidence → gated output)
- **Anomaly taxonomy A–F** (input error / collection error / timing / definition / real business issue / unresolved)
- **Eval harness** with regression tests + trust-gate contracts
The user already built the hard "eval/trust scaffolding" — just wrapped in an enterprise
e-commerce vertical. Move that skeleton to a **public-demoable consumer vertical**.

## Reuse model: fork the PATTERNS, not the code
Explore verdict: ~0% cross-domain code reuse without refactor, but **50–60% reusable as
architecture + eval scaffolding**. Reusable: parser registry/adapter pattern
(`parser_adapters.py`, `parser_registry.py`), trust gate + anomaly ranking (`judgment.py`),
line-item aggregation (`metrics.py`), eval harness (`tests/test_eval_harness_regression.py`,
`docs/evals/evaluation-harness.zh-CN.md`), privacy/audit/tracing patterns. NOT reusable:
e-commerce profit formulas, hard-coded Chinese strings, Alibaba Cloud adapters, the 14
WBFA-specific Excel adapters.

## Capstone fit (Explore ranking)
- **E2 EOB/Claim Auditor — STRONGEST (near 1:1):** parse bill → categorize line items →
  rank billing anomalies → trust-gate ("overcharge found + appeal letter" only if confident,
  else "diagnostic: need X") → drafter. Maps onto WBFA modules almost directly.
- **E1 BenefitsFinder — 2nd:** judgment-tier mapping + ranking reusable; needs eligibility
  rules + income/household parsers + app drafter.
- **E4 TaxUnfreeze — solid:** bank-statement parser ≈ WBFA bank adapter; categorization ≈
  marketing-spend logic; formula engine → Schedule C.

## Why E2 is the recommendation
1. **Resolves the user's E1 concerns:** synthetic EOBs = no public-data-reliability problem;
   auditing arithmetic ≠ giving advice = low policy/liability risk.
2. **Cleanest, most "broken-ruler-proof" eval in the whole slate:** objective arithmetic
   ground truth + seeded error-trap test suite → discrepancy precision/recall + a plottable
   false-alarm vs missed-overcharge frontier + WBFA's trust-gate calibration. The eval IS
   the wow, and it's the user's domain.
3. **Highest WBFA reuse** → biggest head start on the hardest part (the trust/eval engine).
4. **Whitespace + very demoable:** "the agent caught a $1,300 balance-billing violation."
5. **Hits ≥3 concepts easily:** ADK multi-agent (parser + auditor + drafter) · MCP (PDF/OCR
   tool) · **Evaluation** (showpiece) · Security (health-financial PII + HITL on letters) ·
   Deployability. → 5.
   Track: Concierge (privacy-first personal finance) or Agents for Good (medical bills hit
   the vulnerable). E1/E4 = same skeleton → pitch as "extensible architecture" in the writeup.

## Open risk to confirm
**Is WBFA the user's personal project or employer/work IP?** If work IP, the public capstone
repo must be **clean-room (borrow design patterns only, no code copy)**. Either way the public
build is a fresh repo on a new domain, so this is manageable — but it changes how literally we
can reuse WBFA source.

## One-line recommended concept
> **"ClaimGuard": a privacy-first agent that audits your medical/insurance bills (EOBs) for
> arithmetic + balance-billing errors and drafts cited appeal letters — built on WBFA's
> trust-gate + anomaly-taxonomy + eval-harness architecture, generalized from enterprise
> Excel to consumer PDFs, with a seeded-error precision/recall + trust-gate-calibration
> eval harness as the showpiece.**
