# Eng Review — implementation-plan.md

Reviewer lens: eng-manager (plan-eng-review framework). Target: `docs/plan/implementation-plan.md`.
Mode: substance-only (skill's per-finding AskUserQuestion deferred to the gauntlet's grill-me stage; Codex outside-voice deferred to the dedicated `/adversarial-review` stage). **No rubber-stamping.**

Finding format: `[SEV] (confidence N/10) location — issue`.

## Step 0 — Scope challenge
Scope is already disciplined (10-day floor, cut-list, V2 tags). **No scope reduction needed** — if anything the plan is *honest about cutting*, not over-built. One smell: **Phase 4 packs 9 sub-tasks onto "D4," the single non-cuttable day** (see F10). That's a scheduling fiction, not a scope problem.

## 1. Architecture

- **[P0] (9/10) faithfulness_eval.py (Task 4.2) — the deterministic evaluator is keyword matching, not entailment.** `_supported_by_fact` flags support when *any* gold-fact word >4 chars appears in the claim → false "support" on shared vocabulary. `_motive_in_gold` is effectively a constant (true only if a gold fact literally contains "because"/"envy" — G01 never does), so **every** motive-marker claim becomes `UNSUPPORTED_MOTIVATION`, including a *valid hedged interpretation*. The wow rests on this. A skeptical DS (the owner) will see a keyword matcher dressed as an eval. **The subtle-motive catch (D3) cannot be done by keywords** — it needs the claim's `assertion_strength` (HEDGED vs asserted-as-fact) + fact-id anchoring. The spec's corrected caption literally carries `assertion_strength: HEDGED`; the evaluator ignores it.
- **[P0] (9/10) Tasks 4.4 & 4.8 — forward dependency: `evaluate_run` is imported before it exists.** Drift tests (4.4) and the CLI e2e (4.8) both `from evals.run_eval_suite import evaluate_run`, but `evaluate_run` is only created in 4.8 — and 4.4 runs first. The single-scorer design is right; its *position* is wrong. Define the suite assembler (`evaluate_run` = extract→eval→coverage→safety→gate) as its own task **before** the drift suite.
- **[P1] (8/10) schema_validator.py (1.1) — Claim model lacks `assertion_strength` and `claim_type`.** Without them the evaluator can't deterministically separate `VALID_HEDGED_INTERPRETATION` / `CREATIVE_SAFE_FILLER` from `UNSUPPORTED_MOTIVATION`. The 8 labels exist but the inputs to choose between them don't. Root cause of F1.

## 2. Code quality

- **[P1] (8/10) DRY — the hard gate is encoded three times:** `policy_gate._EXPORT_*` constants, `specs/eval_plan.yaml`, and the `export_requires` block. Three sources of truth → silent drift when one changes. Make `eval_plan.yaml` canonical and load it, or a single `gates.py`.
- **[P1] (8/10) Global Constraints say "sanitize generated content before judging" but no task wires or tests it.** It's asserted in prose (2.1 commit note, 3.1/4.1 "applied") with zero test. Exactly the silent gap the owner's verification rules target. Needs a step + test: a zero-width-laced caption is sanitized before `build_judge_prompt`.
- **[P2] (7/10) `_supported_by_fact`/`_motive_in_gold` violate the plan's own "no placeholders / [FULL-CODE]" promise** — they're toy heuristics. Either elevate to fact-id-anchored logic or relabel as reference heuristics with the real check named.

## 3. Tests (coverage diagram)

```
EVAL CORE PATHS                                  SPECIFICITY (does it OVER-block?)
[+] faithfulness_eval.evaluate_claims
  ├── [★★ ] forbidden → CONTRADICTED (4.2)        ├── [GAP] valid HEDGED interp PASSES — NO TEST
  ├── [★★ ] subtle motive → UNSUP_MOTIVE (4.2)    ├── [GAP] CREATIVE_SAFE_FILLER allowed — NO TEST
  ├── [★★ ] injection → PROMPT_INJECTION (4.2)    └── [GAP] supported factual claim PASSES — weak
  └── [★  ] supported → SUPPORTED (keyword only)
[+] drift_injector D1–D6 (4.4)  [★★★ all BLOCK]   [+] baseline calibration
[+] coverage omission (4.3)     [★★  fails <0.85]   └── [GAP] 30–40% fail-band NOT asserted (5.1)
COVERAGE: blocking paths strong; SPECIFICITY paths absent.
```
- **[P0] (9/10) No test proves the gate ALLOWS a valid hedged interpretation.** Every drift test proves BAD→BLOCKED; nothing proves GOOD→PASS. A gate that blocks *everything* passes 100% of the current suite. This is a broken ruler in the other direction — the eval has no specificity test. Add: corrected hedged caption + clean fixture → `export_status != BLOCKED`.
- **[P1] (8/10) The 30–40% baseline fail-band is mentioned but never asserted (5.1).** Owner's calibration rule: >80% pass or <30%/>50% fail = redesign. Add a check (or explicit disclose-and-adjust step) so the ruler is validated, not assumed.
- **[P2] (7/10) Claim-extraction reproducibility spot-check (spec §3.3, 8/10) is missing as a task.** If extraction is unreliable the whole gate is built on sand.

## 4. Performance / feasibility

- **[P1] (7/10) Phase 4 = 9 sub-tasks on "D4," the non-cuttable day.** Realistically 2–3 days of work. The 1.5× circuit breaker fires on day one. Re-baseline: Phase 4 spans ~D3.5–D5; let Phase 5 measured-numbers absorb the slip, not the Day-10 buffer.
- **[P2] (6/10) The regen demo needs a committed corrected-caption fixture.** Video climax = drift→regen→pass, but regen is `[CONTRACT] G_GEMINI`. For the cached judged path, commit the known corrected caption as a fixture so the demo doesn't depend on live convergence.

## NOT in scope (deferred, with rationale)
- LLM-judge calibration study, interpretive-distortion *gate*, clarity human study — `V2` per the 10-day reconciliation (binding 200/210).
- ADK Builder/Critic real loop — P2 upside; CLI path is the judged path.
- Streamlit/SRT/slideshow — P3 bonus.

## What already exists (reuse, don't rebuild)
- `guwen-v3/` ships drafted `threat_model`, `eval_plan`, `AGENTS`, `behavior.feature`, `rater_label_sheet`, `writeup_outline` — Phase 0/1 should **copy-and-trim**, not author from scratch (the plan says this; hold to it).
- The canon_gold for G01 (facts/beats/forbidden) is fully specified in the v3 spec §3.5 — Task 1.3 is transcription, not design.

## Failure modes (new codepaths)
| Path | Realistic failure | Test? | Handled? | Silent? |
|---|---|---|---|---|
| faithfulness_eval | over-blocks valid interpretation | **NO (F7)** | no | **silent → critical gap** |
| evaluate_run import | NameError at 4.4 | no | no | loud (crash) — but blocks progress |
| sanitize-before-judge | injection reaches judge unsanitized | **NO (F5)** | partial | silent → security gap |
| regen loop | infinite spend | yes (4.6) | yes (cap) | loud |

## Parallelization
Mostly **sequential** — the eval core is one tightly-coupled module graph. Two independent lanes only: **Lane A** Phase 2 security (sanitizer/safe_prompt/policy_gate) and **Lane B** Phase 1 schemas+gold can proceed in parallel before Phase 4 joins them. Everything Phase 4+ is one lane.

## Verdict
**DONE_WITH_CONCERNS.** The plan is well-structured and honest about scope, but the **centerpiece eval is keyword-deep, not entailment-deep (F1)**, it has a **forward-dependency bug (F2)**, and it has **no specificity/over-block test (F7)** — three issues that, unaddressed, would let the wow look rigorous while being gameable. Fix F1/F2/F3/F5/F7 before build. Carry to reconcile + grill-me.
