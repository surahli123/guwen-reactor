# Reconciliation — eng-review + Codex adversarial

Synthesis of `eng-review.md` (in-context) + `adversarial-codex.md` (independent).
`VERIFIED_AGAINST: chore/init-planning-archive @ 49b4da8`. Purpose: separate **clear fixes** (apply) from **owner decisions** (grill-me agenda).

## A. Cross-model convergence (highest confidence — both reviewers agree)
1. **The deterministic faithfulness mechanism is the weak point.** It can *false-pass* serious unsupported claims and *false-block* valid hedged interpretations. (eng F1/F7 + Codex P0×4 + biggest-risk.) → This is THE issue.
2. **Phase 4 = schedule fiction.** 9 sub-tasks on the non-cuttable "D4." (eng F10 + Codex P1.)
3. **No specificity / over-block guard; baseline band unenforced.** (eng F7/F8 + Codex P1 baseline-theater.)

## B. Codex-only catches the eng-review missed (concrete plan bugs)
- **C1 [P0]** `UNSUPPORTED_DETAIL` is NOT in `CRITICAL_LABELS`, so it can't raise `unsupported_critical_claims` — but drift D2 expects exactly that to block. **My code contradicts my own test.** (plan:172 vs 573)
- **C2 [P0]** `PROMPT_INJECTION_ATTEMPT` is labeled but **never counted or gated** in `evaluate_claims`/`export_requires_met`; drift D6 can't actually block. (plan:438/614)
- **C3 [P0]** "All cited fact-ids valid" is a hard-gate line with **no implementing task**; invalid-id citation spoof uncovered. (plan:41)
- **C4 [P0]** **Coverage has no trustworthy source of supported fact-ids.** `beat_coverage(supported_fact_ids,...)` assumes fact-level support the label-only evaluator never produces. Self-reported ids → spoofable; keyword → theatrical omission detection. (plan:596)
- **C5 [P1]** Exact-string forbidden match is brittle — "pockets the gold" / "keeps it for himself" evade the forbidden set; with unsupported-detail non-critical, paraphrased contradictions false-pass.
- **C6 [P1]** Precision is **denominator-gameable** — saying less raises `supported/total`; 3-beat coverage is a coarse checklist, not a faithfulness metric.
- **C7 [P1]** **Gold epistemics:** English gold facts vs the "no English translation ingested" rule — provenance of the English ground truth is unspecified; one beat-check by the builder is near-circular.

## C. Clear fixes (apply after the architecture decision — several depend on it)
- Add `assertion_strength` + `claim_type` to the `Claim` schema (eng F3).
- Make `evaluate_run` (suite assembler) its own task **before** the drift suite (eng F2 forward-dependency).
- Wire injection + fact-id-validity into `export_requires_met`; fix `UNSUPPORTED_DETAIL` criticality so D2 blocks (C1/C2/C3).
- Coverage must consume **validated** supported-fact-ids, not labels or self-reports (C4).
- Add a **specificity test**: valid hedged interpretation + clean run → `export_status != BLOCKED` (eng F7).
- Add a step+test that **generated captions are sanitized before judging** (eng F5).
- Single canonical gate definition (load `eval_plan.yaml`), kill the 3-way duplication (eng F4).
- Pre-register the baseline band + adjustment rule so it can't be tuned to look weak (C6/baseline-theater).

## D. OWNER DECISIONS → grill-me agenda
The fixes above mostly hinge on **D1**. Resolve these with the owner before rewriting tasks:

- **D1 — Eval architecture (load-bearing).**
  - *Option A (Codex P2, recommended):* drop free-form claim extraction as the centerpiece. Constrain GENERATION to structured, beat-anchored fields `{beat_id, claim_text, source_fact_ids, assertion_type, hedging}`. The deterministic gate then **audits structure** (required-beat coverage, forbidden deltas, missing/invalid fact-ids, **unhedged motive/emotion fields**, safety, manifest, approval) — all genuinely deterministic. Semantic entailment is **explicitly advisory** (LLM + human). "Less grand, far more defensible."
  - *Option B:* keep free-form extraction, patch it with `assertion_strength` + fact-id anchoring + entailment heuristics. Lighter diff, but still trying to fake entailment deterministically — the exact thing both reviewers flagged.
  - *Option C:* hybrid — structured generation for the gated storyboard claims, free-form allowed for ungated decoder/analogy.
- **D2 — Gold epistemics (C7).** How is the English gold produced credibly given "no English translation ingested"? Options: builder-authored English facts from the Chinese (own translation, disclosed) + 1 independent Chinese-literate check; vs anchor gold to *Chinese* fact spans and make English claims point to chunk-ids; vs accept + disclose single-annotator limitation loudly.
- **D3 — Scope / dilution (Codex strategic).** Wrappers (MCP/skills/ADK) vs depth on the trust gate. The winning demo is educator artifact + trust gate + approval. Keep all 5 concepts, or narrow to a rock-solid "constrained-source audit harness"?
- **D4 — Feasibility re-baseline.** Spread Phase 4 across ~D3.5–D5; let Phase 5 absorb slip, not the Day-10 buffer. Confirm.

## Verdict
Plan is structurally sound and honestly scoped, but the **eval core needs a design decision (D1), not just patches** — both reviewers say the current mechanism reads as *staged, not measured*, which is fatal for a DS-judged capstone. Resolve D1–D4 in grill-me, then revise the affected Phase 1/3/4/5 tasks once.
