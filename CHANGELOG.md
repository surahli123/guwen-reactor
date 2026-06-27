# Changelog

All notable changes to Guwen Reactor. Format: [Keep a Changelog](https://keepachangelog.com); dates are ISO (YYYY-MM-DD).

## [Unreleased]

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
