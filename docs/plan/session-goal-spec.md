# Session Goal Spec — Finish the Guwen-Reactor Prototype (Tier 3)

> **Status:** APPROVED (execute-with-edits) — reconciled per the 2026-06-28 adversarial review (`reviews/2026-06-28-goal-spec-adversarial.md`, 0 blockers). This is the *locked spec* the goal-forge
> pattern requires **before** any autonomous run (the human control point).
> Source: [`self-authored-parallel-goal-pattern`] + `decisions-locked.md` (D1–D4, Contracts A–J).
> Date authored: 2026-06-28. Branch: `feat/phase-0-scaffold`.

---

## 0. 一句话(给 owner)

把"古文 → 英文改编"端到端跑通,让一个**确定性闸门**自动**放行干净改编、拦掉植入的幻觉**,
用 CLODE 跑通后渲染成一个**不需要密钥就能打开的静态演示页**,最后用**真实 Gemini 输出**测一组数字。
这一会话做完离线全部 + 你授权后的实测数字 = 完整原型(Tier 3)。

**Plain-language的"完成"长这样:**
- `demo_clean` 跑 → **导出成功**(带防伪 manifest + AIGC 标签)
- `demo_drift` 跑 → **被拦下**,6 种植入幻觉一个不漏
- 额外硬骨头:**编造事件 + 引用一个真实但错位的 fact id** → 也被「结构对齐检查」拦下(review #4)
- 打开 `docs/demo/index.html` → 不用任何 key 就能看到整条链路
- `pytest evals/` → 全绿(现有 42 + 每个新模块的新测试)
- 一组**真实 Gemini 基线数字**写进 `docs/measured_results.md`(你授权后我跑)

---

## 1. End-to-end Goal (the self-authored `/goal` objective)

> Drive the guwen-reactor prototype to a **demoable, source-grounded plot-fidelity** state:
> a pure-Python eval core that deterministically audits structured claims, blocks every
> planted drift type, passes a clean adaptation, exports a manifest-bound bundle behind a
> human-approval gate, renders a no-API-key static canvas, and reports measured baseline
> numbers on real Gemini output — **all green, all committed, this session.**

**Standard:** not "code exists" — every module ships test-first (TDD), the full `pytest evals/`
stays green after each step, and the two end-to-end DoD commands behave exactly as specified.

**Claim scope (review #4):** the deterministic gate proves **structural** source-grounding — valid +
*beat-aligned* citations, blacklist, structural audit — **not** semantic entailment, which stays advisory
(D1). **Disclosed residual:** a fabricated sentence citing a *correct-beat* id is not caught deterministically;
reported in `docs/measured_results.md`.

---

## 2. Definition of Done (the machine-verifiable `/goal` Stop-hook condition)

The session may stop **only** when ALL of these hold (this is the literal DoD gate):

| # | Check | Command / evidence | Pass = |
|---|---|---|---|
| D1 | Clean run exports | `python -m app.cli run runs/demo_clean --approve` | exit 0 + manifest written (sha256 + AIGC label, manifest-bound) |
| D2 | Drift run blocked | `python -m app.cli run runs/demo_drift` (dir **materialized + committed** by S6) | DoD first asserts `runs/demo_drift/` **exists on disk**, then **non-zero / BLOCKED** with `missing[]` listing the gate failures |
| D3 | All 6 drift types caught | `pytest evals/test_drift_injection.py -v` | 6/6 → BLOCKED (contradiction, unsupported-detail, motive-spoof, omission, citation-spoof, judge-injection) |
| D4 | Over-block guard | `pytest evals/test_specificity.py -v` | valid *hedged* interpretation does NOT block export (Contract G) |
| D5 | No-key canvas | **automated:** grep rendered `docs/demo/index.html` for external `http(s)`/`src`/CDN/`fetch` refs (assert none); headless-load with network blocked | renders from committed artifacts, **zero** network/API calls |
| D6 | Full suite green | `pytest evals/ -q` | 42 existing + all new tests pass, 0 fail |
| D7 | Measured numbers | `docs/measured_results.md` | B1 baseline **ran + logged numerator/denominator**, and the **pre-registered deviation rule applied if out-of-band** — **NOT** gated on the fraction landing in `[0.30,0.40]` (no broken ruler); single-annotator limit disclosed *(gated on Line-A auth)* |
| D8 | Valid-but-wrong-id blocked | `pytest evals/test_structural_audit.py -v` | hostile fixture: a claim citing a **valid id from the wrong beat** → BLOCKED via the structural beat↔fact-id alignment check (Contract B rule 5) |

**The gate itself** is defined once in `specs/eval_plan.yaml` (Contract F) — `export_requires_met()`
in `app/policy_gate.py` loads it. **Stage-aware status (review #2):** `evaluate_run` sets
`export_status = BLOCKED` iff a **content** gate fails (zero_count + coverage + `safety_pass` +
`workflow_integrity_pass` + `source_policy_valid` + `source_sanitized`); a content-clean-but-unapproved run
is `READY_FOR_APPROVAL`. The YAML `export_gate` (incl. `human_approved` + `aigc_label_manifest_bound`) is the
**final** requirement enforced only at export (S10). *"No new gate constants"* = no duplicate of the list,
**not** a ban on stage-aware status — and the executor must **NOT** delete the approval `bool_gates` to green a test.

---

## 3. Decomposition — waves, sub-goals, per-sub-goal DoD

Dependency reality: a **serial spine** `4a.1 → 4a.4 → 4b.5`; most 4b modules wire *into*
`evaluate_run`, so they are built sequentially against it, not in naive parallel. Parallelism is
used only where files are genuinely disjoint (noted ‖).

Each sub-goal is TDD: **write the failing test first → implement → green → full suite green.**
Every sub-goal carries its named Contract + test file from `implementation-plan.md`.

### Wave 0 — Fixtures (offline; unblocks everything)
- **S0 · Task 3.1** — hand-write `runs/demo_clean/{adaptation.yaml,structured_claims.yaml}` (Contract A: `beat_id`, `source_fact_ids`, `assertion_type`, `hedging`, `artifact_path`). Also stub `guwen_core/adaptation_gen.py` interface (the live generator call stays `[CONTRACT]`, unused by the eval core).
  - **DoD:** fixtures validate against `StructuredClaim`; clean run is all `assertion_type=action/visual`, `hedging=asserted`, valid covering fact-ids.

### Wave 1 — ⭐ Labeling core (Phase 4a, NON-CUTTABLE) — **CHECKPOINT 1 after this wave**
- **S1 · Task 4a.1** — `guwen_core/claim_validator.py` (structure + fact-id validity; `sanitize()` on `claim_text`). Test `evals/test_claim_validator.py`.
- **S2 · Task 4a.2** — `guwen_core/structural_audit.py` — the heart (Contract B): injection → invalid-id → forbidden-delta → unhedged-motive → **unsupported-action (incl. the structural beat↔fact-id alignment check — review #4: cited ids must belong to the claim's declared beat; an irrelevant-but-valid id does NOT boost coverage)** → hedged-valid. Test `evals/test_structural_audit.py` **incl. the valid-but-wrong-beat hostile fixture (D8)**. *(depends on S1)*
- **S3 · Task 4a.3** ‖ — `guwen_core/coverage.py` — beat coverage from **validated** fact-ids only (Contract C). Test `evals/test_coverage.py`. *(depends on S1; runs ‖ with S2)*
- **S4 · Task 4a.4** — `evals/run_eval_suite.py` `evaluate_run()` (Contract E) — orchestrates validate→audit→coverage→safety-stub→integrity-stub→gate. **Defined before any drift test.** *(integration point; depends on S1–S3)*
- **S5 · Task 4a.5** — `evals/test_specificity.py` (Contract G over-block guard).
  - **Wave DoD:** `pytest evals/` green; clean fixture passes the gate; a tampered fixture fails it.

### Wave 2 — ⭐ Drift + safety + regen + export + CLI + trace (Phase 4b, NON-CUTTABLE) — **CHECKPOINT 2 after this wave**
- **S6 · Task 4b.1** — `guwen_core/drift_injector.py` + `evals/test_drift_injection.py` (6 mutations → all BLOCKED). **Also materialize + commit a durable `runs/demo_drift/` (review #1, both models agreed)** via `inject runs/demo_clean runs/demo_drift subtle_motivation_spoof` — D2 consumes the committed dir, not an ephemeral `tmp_path`. *(depends on S4)*
- **S7 · Task 4b.2** ‖ — `guwen_core/safety_eval.py` (structural deny-list; semantic LLM is `[CONTRACT]`/advisory). Wired into `evaluate_run`.
- **S8 · Task 4b.3** — `guwen_core/regen_loop.py` (`max_total_attempts=3`, fail-closed, stub-injectable). Test `evals/test_regen_loop_blocks_then_passes.py`.
- **S9 · Task 4b.6** ‖ — `guwen_core/{trace.py,workflow_integrity.py}` (OTel-named JSONL trace + `check_order()`). Wired into `evaluate_run`. **trace.py emits exactly `eval_plan.yaml workflow_integrity.required_events`; add a test asserting emitter-vocabulary == that set (review #6).**
- **S10 · Task 4b.4** — `app/approval.py` + `guwen_core/export_bundle.py` (approval diff; manifest sha256 + AIGC; export raises unless gate-passed AND approved).
- **S11 · Task 4b.5** — `app/cli.py` (typer) — **the e2e DoD** (D1+D2 above). *(integration point; depends on S6–S10)*
  - **Wave DoD:** D1, D2, D3, D4, D6 all hold.

### Wave 3 — Canvas + measured numbers (Phase 5)
- **S12 · Task 5.2** `[FULL-CODE]` — `app/render_canvas.py` + `docs/demo/index.html` from committed artifacts, no key (D5).
- **S13 · Task 5.1** `[CONTRACT]` — fair same-template baseline B1 on real Gemini (pre-registered band). **← Line A: needs `GEMINI_API_KEY` (free AI Studio key) via google-genai Developer-API mode — no gcloud/Vertex.**
- **S14 · Task 5.3** — `docs/measured_results.md` with real fractions + disclosed single-annotator limit (D7). *(depends on S13)*
  - **Wave DoD:** D5 holds; D7 holds *iff* Line-A auth completed, else S13/S14 stop as a credential blocker with everything else done.

### Housekeeping (fold in, no extra wave)
- Update `CHANGELOG.md` (Phase 2 currently undocumented). Fix the `coverage_gate` key-name note from the Explore map if any new code reads the plan pseudocode instead of the YAML.

---

## 4. Orchestration, checkpoints, execution mechanism

- **Driver:** native `/goal` Stop-hook set to the DoD (§2). It keeps this session driving until DoD holds.
- **Builders:** each sub-goal dispatched to a focused `oh-my-claudecode:executor` (sonnet, TDD, caveman-ultra output). Disjoint sub-goals (‖) run as parallel `Agent()` calls; spine sub-goals run sequentially against the integration files.
- **Verification lane (separate pass):** after each wave I run `pytest evals/` myself and report actual pass/fail; a `verifier`/`code-reviewer` pass reviews the eval core before we trust it (no self-approval in the build context).
- **Two owner checkpoints** (your "visible stages"): **CP1** after Wave 1 (eval core — the heart), **CP2** after Wave 2 (e2e CLI green). I pause, show evidence, you steer. Between checkpoints I run inside the fence.

---

## 5. Stop conditions (the only reasons to halt early)

1. **Missing credential** — Line A: if `gcloud`/ADC isn't ready when I reach S13, I stop *there* with Waves 0–3-canvas complete (everything except live numbers).
2. **Destructive ambiguity** — any irreversible action not covered by this spec.
3. **Conflicting requirements** — code vs `decisions-locked.md` disagreement (e.g. the `coverage_gate` key mismatch) → surface, don't guess.
4. **Circuit breaker** — 3 failed attempts on the same sub-goal → STOP, diagnose, show you, wait.

---

## 6. Line-A handoff (your one action — now lightweight)

Model access for the live baseline (S13) needs **only a free Google AI Studio API key** —
**no gcloud, no GCP project, no billing, no Vertex/ADC.** The plan already allows a *"direct call"*
path (`implementation-plan.md:11`); this picks the lightweight branch of it. (Vertex/ADC and the
ADK route are the heavier paths — ADK stays P2/deferred per `decisions-locked.md`. The Kaggle
"Day 5: Cloud Run / Agent Runtime" paragraph is *deployment*, a third unrelated thing we are not doing.)

Your action, when convenient, any time before I reach S13:
1. Get a free key at <https://aistudio.google.com/apikey>.
2. Make it available to the session (presence only — never paste the value into a tracked file):
   ```
   export GEMINI_API_KEY=...      # confirm GEMINI_API_KEY vs GOOGLE_API_KEY at S13 (see G_GEMINI)
   ```
   I'll call it via the `google-genai` SDK in **Developer-API mode** (`genai.Client()` with the key),
   **not** `vertexai=True`.

Notes:
- **Eval core needs none of this** — Phases 4a/4b (the wow) are offline-fixture-first. Only S13/S14 use the key.
- **`G_GEMINI` still applies:** the exact call signature is the one unverified gate. Per *"don't invent API
  syntax,"* I confirm it against current `google-genai` docs (context7 / `document-specialist`) **before**
  coding S13 — not now. Update `docs/build_log.md:24` to reflect the AI-Studio route once verified.
- **Free-tier terms:** AI Studio free tier has rate limits (fine for a 3-scene baseline) and may use prompts
  to improve Google products — acceptable here (public-domain Chinese + our own prompts, no sensitive data).

Until the key is set, S13/S14 wait; nothing else blocks.

---

## 7. Explicitly OUT of scope this session (Line B / P2)

Human gold sign-off (`independent_check_notes.md`), Phase 6 MCP, Phase 7 skills, Phase 8 ADK,
Phase 9 video + public ship. These need your action or are P2 upside — separate session.

---

## 8. Reconciliations from the 2026-06-28 adversarial review

Verdict: **execute-with-edits, 0 blockers.** Applied to this spec + binding contracts *before* the run
(full critique: `reviews/2026-06-28-goal-spec-adversarial.md`):

1. **demo_drift durable producer** (OMC + Codex agreed — highest trust) → S6 materializes+commits it; D2 asserts the dir.
2. **Export gate stage-aware** (content vs approval) → §2 note; executor must NOT delete approval `bool_gates`.
3. **D7 no outcome-gating** → §2 D7 rewritten + `eval_plan.yaml` adjustment_rule dead-zone (0.40–0.50) closed.
4. **Valid-but-wrong-id structural check** → `decisions-locked.md` Contract B rule 5 (beat-membership) + S2 + D8 hostile test; within-beat semantic residual disclosed (§1).
5. **D5 automated no-network check** → §2 D5.
6. **workflow_integrity vocabulary** (stale `claims_extracted` from pre-D1 design) → `eval_plan.yaml required_events` fixed + S9 conformance test.

Lower-priority (noted, not gating): homoglyph-evasion of the forbidden match — optional later hardening.
