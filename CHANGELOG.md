# Changelog

All notable changes to Guwen Reactor. Format: [Keep a Changelog](https://keepachangelog.com); dates are ISO (YYYY-MM-DD).

## [Unreleased]

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
