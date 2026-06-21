# v3 Acceptance + Plan-Gate Decision

Written 2026-06-20. Decision after a 3-lens OMC subagent review (critic / architect /
security) of GPT's Build-Ready Spec v3 (`guwen-v3/`), against the deep-review findings
(170) and the fix-list (180), under the 10-day constraint (190/200).

## DECISION: PASS THE PLAN STAGE — with a binding reconciliation.
The plan is technically build-ready (all blockers' CONTENT resolved). The only real issue
is scope/timeline discipline: v3 over-answered (a 17-day plan that re-added V2-deferred items
as P0). Resolved by the reconciliation below — all deletions/re-tags, no new work.

## 3-lens verdict
- **architect (eval + architecture):** B1 PASS (calibrated gate + advisory fallback + deterministic hard gate); B4a/b/c PASS (denominator/fraction/count-gate; narrowed claim + rubric; independent gold check + diff-family Pass-3 + disclosed limitation); ARCH PASS (file-ref handoff + test, ~4 real MCP tools, deterministic OTel trace, real Critic loop). Residual: B4d demo leads with an UNMEASURED iconic preview; "42/45"-style precision are illustrative placeholders.
- **security:** 5/6 PASS (B2 injection defense + threat_model; S5 two-layer safety; S7 DoW cap; S6 AIGC sha256 manifest; S1 reworded copyright). S9 PARTIAL (docs/demo/ filename rules unstated). 2 new MEDIUM build-time gaps: sanitize generated content (not only source); define the `PROMPT_INJECTION_ATTEMPT` detector. + pin requirements.txt (S8 nit).
- **critic (plan gate):** technical B1-B4 good (B2/B4 PASS), but SCOPE-CREEP FAIL + 10-DAY-REALISM FAIL — §10 is a 17-day plan; calibration study, interpretive rubric/gate, behavior.feature, test_skills.py re-added as P0/hard-gates vs the handoff's "defer to V2."

## Binding reconciliation (the gate condition)
1. **`200-guwen-FINAL-execution-handbook.md` is the BINDING plan** — scope, 10-day calendar, cut-list, absolute floor.
2. **v3 spec = adopted TECHNICAL reference** — use its mechanisms for eval/architecture/security (they are well-built).
3. **v3 items beyond the 10-day floor → V2-if-time, NOT P0:** judge-calibration study (use deterministic-gate-primary + LLM judge advisory), interpretive rubric/gate (narrow claim to "source-grounded plot fidelity"), `behavior.feature`, `test_skills.py`. Hard gate = deterministic set (`unsupported_critical_claims==0` + required-beat coverage + forbidden-claim match + safety + human approval).
4. **Carry-forward cheap fixes into the build:**
   - Caption the demo iconic-preview "format illustration — not the measured scene" (B4d residual).
   - Mark ALL example metrics (e.g. 42/45, 12/14) `ILLUSTRATIVE — replace with measured run output`.
   - Apply NFKC + zero-width strip to GENERATED content too, before judging (security gap 1).
   - Specify the `PROMPT_INJECTION_ATTEMPT` detector + assert in `test_safe_prompt.py` (security gap 2).
   - Pin exact versions in `requirements.txt`; state `docs/demo/` filename validation (S9).
> Keep from v3 as genuinely good: the deterministic-gate-primary fallback, file-reference handoff, ~4 real MCP tools, deterministic OTel trace, real Critic loop, the full threat_model + safe-prompt fences + DoW cap + AIGC manifest, the eval_plan.yaml structure, the writeup_outline + rater_label_sheet.

## What "go" triggers (build start, eval-first)
D0.5 harness hello-world (ADK + ADC auth + 1 Gemini call + 1 MCP stdio round-trip) → D1 repo +
specs (pull v3's threat_model/eval_plan/AGENTS as starting files) → D2 canon gold + schemas →
D3 adaptation → **D4 deterministic eval core + planted drift + approval (CLI green)** → wrappers
→ video → ship. Verify BEFORE build: Antigravity CLI commands vs official docs; pick the iconic
video scene; line up 1 independent gold check; confirm Gemini/ADK auth.

Status: PLAN STAGE PASSED (conditional reconciliation above). Still no code until owner says "go".
