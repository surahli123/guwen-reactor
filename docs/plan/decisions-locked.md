# Decisions Locked + Contracts Spine (post-grill-me)

Authoritative input for revising `implementation-plan.md`. Authored from full session
context. Resolves D1–D4 (grill-me) + the `reconciliation.md` fix-list into exact contracts.

## 1. Decisions
- **D1 = A — constrained-field generation + structural audit.** The generator emits *structured claims* (not free prose); the deterministic hard gate **audits structure**. Semantic entailment = **advisory only** (LLM + human), never in the hard gate.
- **D2 = A — Chinese-anchored gold.** Every English gold `atomic_fact` is anchored to a specific Chinese `source_chunk_id`; one independent Chinese-literate denotation check; single-author limitation disclosed.
- **D3 = C — plot hard-gated, interpretation advisory.** Hard gate covers storyboard plot claims only. A light interpretive rubric runs over decoder + analogy and is **reported, never export-blocking**. Keep all 5 concepts. `interpretive_eval.py` = **P2, first on the cut-list**.
- **D4 = A — re-baselined schedule.** Split Phase 4 into **4a** (labeling core) + **4b** (drift/gate/CLI) across **D3.5–D5**; Phase 5 → D5–D6; wrappers D6–D8; **Day 10 = true buffer**. Cut order if any day >1.5×: advisory interpretive rubric → eval scene 3 → eval scene 2.

## 2. Contract A — StructuredClaim schema (replaces free-form extraction as centerpiece)
The generator emits claims directly in this shape; `claim_extractor` becomes a **structure validator**, not a free-text extractor.
```yaml
StructuredClaim:
  claim_id: str
  beat_id: str | null          # which required beat this serves (null = non-beat)
  claim_text: str
  source_fact_ids: [str]       # canon_gold fact ids this claim asserts it is grounded in
  assertion_type: enum         # action | motive | emotion | interpretation | visual
  hedging: enum                # asserted | hedged
  artifact_path: str           # e.g. storyboard.panels.P06.caption_en
```
Label set unchanged (8 labels). The gate ASSIGNS the label from structure (below) — the generator does not self-label.

## 3. Contract B — Deterministic structural-audit gate (rule order matters)
`evaluate_claims(claims, scene) -> {labeled, counts}`. Apply per claim, first match wins:
1. **Injection:** `detect_injection(claim_text)` → `PROMPT_INJECTION_ATTEMPT` → **blocks export** (fix C2 — now gated).
2. **Invalid fact-id:** any `source_fact_ids` not present in `canon_gold` → `CONTRADICTED`/`INVALID_FACT_ID` → **blocks** (fix C3 — new check).
3. **Forbidden delta:** normalized match (casefold + strip punct + collapse whitespace) against `forbidden_claims`; also flag a claim whose `claim_text` contradicts a covered fact → `CONTRADICTED` → blocks. (C5: normalization reduces brittleness; residual paraphrase risk is explicitly the advisory judge's job — disclose.)
4. **Unhedged motive/emotion:** `assertion_type in {motive, emotion}` AND `hedging == asserted` → `UNSUPPORTED_MOTIVATION` → **blocks**. (This is the subtle-drift catch, now deterministic via the declared field — no keyword guessing.)
5. **Unsupported asserted event:** an `action`/`visual` claim asserting a source event whose `source_fact_ids` do **not** cover it → `UNSUPPORTED_DETAIL` flagged **critical** → blocks (fix C1: UNSUPPORTED_DETAIL counts toward `unsupported_critical_claims` when it asserts a new source event; `CRITICAL_LABELS` / counting updated so D2 drift blocks).
6. Else supported/hedged-valid → `SUPPORTED` / `VALID_HEDGED_INTERPRETATION` / `CREATIVE_SAFE_FILLER` → does not block.

`counts.unsupported_critical_claims` = #(critical labels: CONTRADICTED, UNSUPPORTED_MOTIVATION, critical UNSUPPORTED_DETAIL, INVALID_FACT_ID, PROMPT_INJECTION_ATTEMPT).

## 4. Contract C — Coverage uses VALIDATED fact-ids (fix C4)
`supported_fact_ids` = union of `source_fact_ids` over claims labeled `SUPPORTED` **and** whose ids passed the validity check. A beat is covered iff **all** its `fact_ids ∈ supported_fact_ids`. `required_beat_coverage = covered/total`, gate ≥ 0.85. (Never from self-reported ids alone, never from keyword support.)

## 5. Contract D — Gold schema (D2)
`atomic_fact` gains **required** `source_chunk_ids: [str]`; `source_chunks[]` carry `text_zh`. New deliverable `data/gold/independent_check_notes.md` (denotation match, beats not prose). `docs/measured_results.md` discloses single-annotator gold + judge-advisory.

## 6. Contract E — evaluate_run (suite assembler) defined BEFORE the drift suite (fix F2)
New Task in Phase 4a: `evals/run_eval_suite.py::evaluate_run(run_dir) -> eval_report dict`, orchestrating validate-schema → structural audit → coverage → safety → workflow-integrity → gate. **Drift tests (4b) and CLI import it** — so it must exist first. Kills the forward-dependency.

## 7. Contract F — Single canonical gate definition (fix F4)
The export-gate list lives **once** in `specs/eval_plan.yaml`; `policy_gate.export_requires_met` loads it. No triplicate constants.

## 8. Contract G — Specificity test (fix F7, non-negotiable)
`evals/test_specificity.py`: a **valid hedged interpretation** (`assertion_type=interpretation|motive`, `hedging=hedged`, cites supporting facts) on an otherwise clean run → `export_status != BLOCKED`. Proves the gate does not over-block. Pairs with the drift suite (which proves it blocks bad claims).

## 9. Contract H — Sanitize generated content before judging (fix F5)
Add a step + `evals/test_safe_prompt.py` assertion: generated `claim_text` passes `sanitize()` (NFKC + zero-width strip) **before** the audit / `build_judge_prompt`. A zero-width-laced caption fixture must be normalized.

## 10. Contract I — Baseline pre-registration (fix C6 / owner's calibration rule)
Before running B1, write into `specs/eval_plan.yaml`: the expected **30–40% fail band**, and a **pre-registered adjustment rule** (what you change, in which direction, decided before seeing results) for an out-of-band baseline. Baseline scored by the **same** `evaluate_run`. No tuning-to-taste.

## 11. Contract J — Advisory interpretive layer (D3=C)
`guwen_core/interpretive_eval.py` (P2): computes acceptable-framing / distortion signal for `cultural_decoder` + `modern_analogy` against a light `interpretive_rubric.yaml`; result lands in `eval_report.interpretive_advisory`, **never** in `export_requires`. First on the cut-list.

## 12. Schedule re-baseline (D4=A)
- **D1** repo+specs+scene+gold-draft · **D2** gold (chinese-anchored, checked) + schemas
- **D3** source-guard + sanitizer + safe-prompt + **structured-claim generation contract**
- **D3.5–D4 (Phase 4a)** structure-validator + structural-audit gate + coverage + `evaluate_run` + **specificity test**
- **D4–D5 (Phase 4b)** drift suite (D1–D6) + safety + regen/DoW + approval/export/manifest + **CLI e2e green (NON-CUTTABLE)** + trace/workflow-integrity
- **D5–D6 (Phase 5)** fair baseline (pre-registered) + measured fractions + cached canvas
- **D6–D8** MCP + 3 skills + ADK split (upside)
- **D8–D9** video + writeup + ship · **D10** true buffer

## 13. Reconciliation fix checklist (every item MUST be visible in the revised plan)
F1 keyword→structural-audit ✓(D1) · F2 evaluate_run ordering · F3 schema gets assertion_type+hedging+source_fact_ids · F4 single gate def · F5 sanitize-generated test · F7 specificity test · F8/C6 baseline band pre-registered · F10/D4 schedule re-baseline · C1 UNSUPPORTED_DETAIL criticality · C2 injection gated · C3 fact-id validity check · C4 coverage from validated ids · C5 forbidden normalization + disclosed residual · C7 gold provenance/anchoring ✓(D2).
