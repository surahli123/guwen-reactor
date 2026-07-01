# Changelog

All notable changes to Guwen Reactor. Format: [Keep a Changelog](https://keepachangelog.com); dates are ISO (YYYY-MM-DD).

## [Unreleased]

### Added — 2026-06-30 — Phase 4b pipeline + Phase 5.2 canvas (offline prototype complete)
- **Phase 4b (Wave 2):** `safety_eval` (deterministic deny-list, wired real into `evaluate_run`), `regen_loop` (`run_with_regen`, fail-closed at 3 attempts), `trace` + `workflow_integrity` (OTel JSONL + IN_ORDER; event-vocabulary conformance-locked to the YAML), `approval` + `export_bundle` (refuses unless content-clean AND human-approved; sha256 + AIGC-label manifest), and **`app/cli.py`** — the non-cuttable e2e: `run <dir> --approve` exports; a drift run is BLOCKED with no manifest.
- **Phase 5.2:** `render_canvas` → self-contained no-key `docs/demo/index.html` (D5: zero external refs, 19 tests).
- **Independent code review of the eval core caught + closed a MAJOR `beat_id=None` gate bypass** before it shipped (a beat-less claim citing a real beat-owned fact now BLOCKS).
- **`pytest evals/` = 131 passed.** Commits `4f8e0a7`, `adc8b4f`, `19784fd`.

### Changed — 2026-06-30 — demo direction reframed (owner review)
- The static demo canvas (storyboard + gate table) was **rejected by the owner** as "just a Chinese→English translation, not demo-ready." The engine (131 tests) is sound and reusable; the *presentation* was throwaway.
- **New demo concept: "看得见的忠实 / Visible Faithfulness"** — an engaging grounded retelling where clicking any line reveals (考据-style) the original Classical Chinese it is grounded in + a ✓-verified stamp, plus a "如果没有闸门" toggle showing what an ungated AI would fabricate. Faithfulness made *visible and tactile*, not a table. "Trustworthy cultural education" is the framing; the gate is the quiet trust layer.
- **Aesthetic target:** 《中国诗词山河卷》 handscroll style (青绿山水 on silk, glowing data-lights, woodblock 册页 panels, seal-red, serif). Its **考据** (provenance) feature maps exactly onto our faithfulness-provenance — same interaction.
- **Tooling:** installed `baoyu-design` (the Claude Design engine, global `~/.claude/skills/`) as the front-end design tool; audited it (Med-Risk score = Playwright/esbuild deps, not malice; core path is offline). `render_canvas` / `index.html` will be **superseded** by the new baoyu-design build.

### Added — 2026-06-28 — Phase 2 (security core) + Phase 3 (fixtures) + Phase 4a (eval core — the wow)
- **Adversarial review of the session goal spec** (4 OMC lenses + independent Codex, refute-verified → execute-with-edits, 0 blockers): 6 reconciliations applied before the build (`reviews/2026-06-28-goal-spec-adversarial.md`). A follow-up independent code review of the eval core then caught + closed a **MAJOR `beat_id=None` gate bypass**.
- **Phase 2 — security core:** `guwen_core/source_sanitizer.py` (NFKC + zero-width strip + sha256), `guwen_core/safe_prompt.py` (fenced judge prompt + `detect_injection`), `app/policy_gate.py` (loads the single canonical gate; injection + fact-id gated). (Built earlier; now recorded.)
- **Phase 3 — fixtures:** `runs/demo_clean/{adaptation,structured_claims}.yaml` (G01, 10 claims, beat-aligned, coverage 1.0) + `guwen_core/adaptation_gen.py` (offline loader; live Gemini stays `[CONTRACT]`/S13). `.gitignore` carve-out so the demo fixtures are committable.
- **Phase 4a — eval core (NON-CUTTABLE; the deterministic faithfulness gate):** `claim_validator.py` (Contract A) · `structural_audit.py` (Contract B, **strengthened rule 5: beat↔fact-id alignment** — blocks fabricated events citing real-but-wrong / undeclared-beat ids) · `coverage.py` (Contract C, plot-claims only) · `evals/run_eval_suite.py::evaluate_run` (Contract E, stage-aware `export_status`) · specificity over-block guard (Contract G).
- **`pytest evals/` = 65 passed.** Clean fixture → `READY_FOR_APPROVAL`; injection / invalid-id / forbidden / unhedged-motive / empty-id / wrong-beat / beat-less-bypass → BLOCKED; valid hedged interpretation → not blocked.

### Added — 2026-06-26 — Phase 1 (schemas + sources + 3-scene chinese-anchored gold)
- **Scene picks** (research + adversarial-labelability workflow, one decision at a time): video=三顧茅廬; 3 measured eval scenes **G01 管寧割席 · G02 詠雪 · G03 道旁苦李**; gold check = route 2+3 + second-reader cross-validation (deferred).
- **Protocols:** `docs/plan/gold-cross-validation-protocol.md` (2-reader blind, percent-agreement + κ small-N caveat) + `docs/plan/annotation-guardrails.md` (通用 + 每場景 + specificity/drift two-way proof).
- **Task 1.1** `guwen_core/schema_validator.py` + `evals/test_schema.py` — `StructuredClaim` (Contract A) + chunk-anchored `AtomicFact` (Contract D) + enums (TDD RED→GREEN).
- **Task 1.2** locked 3 scene `source.zh.txt` + `source_metadata.yaml` (`english_translation_ingested:false`) + `_fixture_unclear_license` (Phase-2 negative fixture).
- **Task 1.3** `data/gold/canon_gold.yaml` (G01 10 facts / G02 9 / G03 9, every fact chunk-anchored) + `data/gold/independent_check_notes.md`. **`pytest evals/` = 7 passed.**
- **Adversarial gold audits** (3-lens workflows) caught real contamination in 3/3 scenes (incl. 2 in the spec's own G01 gold) → fixes applied; single-annotator / no-IAA disclosed, human denotation check pending.

### Added — 2026-06-22 — repo genesis + Phase 0
- Initialized the project repo from the `~/notes/kaggle-vibecoding/` planning trail (`docs/planning/`).
- Implementation plan `docs/plan/implementation-plan.md` (1094 lines) — structured-claim generation + deterministic structural-audit eval core.
- Locked decisions **D1–D4** + contracts spine (`docs/plan/decisions-locked.md`); review-gauntlet trail (`docs/plan/reviews/`: eng-review, independent Codex adversarial, reconciliation).
- **Phase 0:** Python env (3.14.4, pinned deps), `evals/test_env.py` (passing), package skeleton.
- Seed specs: **`specs/eval_plan.yaml`** (the single canonical export gate), `product_spec`, `threat_model`, `behavior.feature`, `demo_script`, `writeup_outline`; `AGENTS.md`; `docs/build_log.md`; `docs/capstone_writeup.md` stub.
- Live decision board `docs/plan/session-map.html`.

### Notes
- Eval core is **offline-fixture-first**; live Gemini/MCP/ADK auth is an owner action, off the critical path.
- Python 3.14 is bleeding-edge — reproducers/judges should use **3.11–3.13** (`requires-python = ">=3.11"`).
