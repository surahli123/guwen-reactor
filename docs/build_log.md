# Build Log — Guwen Reactor

Living log of build steps, tools, decisions, and verification evidence.
Plan: `docs/plan/implementation-plan.md`. Decisions: `docs/plan/decisions-locked.md`.

## Day 0.5 / Phase 0 — Verify-before-build + scaffold

### Task 0.2 — Environment + skeleton ✓ VERIFIED
- **Python 3.14.4** (Homebrew). ⚠️ 3.14 is bleeding-edge — for maximum wheel
  compatibility, reproducers/judges should use **Python 3.11–3.13**
  (`pyproject.toml` sets `requires-python = ">=3.11"`).
- venv at `.venv/` (gitignored). Install: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.
- Pinned (frozen) versions: `pydantic==2.13.4`, `pyyaml==6.0.3`, `pytest==8.4.2`,
  `jinja2==3.1.6`, `typer==0.26.7`, `rich==13.9.4`.
- Smoke test `evals/test_env.py` → **PASS** (1 passed). Runtime print:
  `USING: python=3.14.4, pydantic=2.13.4, pyyaml=6.0.3`.

### Task 0.1 — Verify external tooling & auth — OPEN (owner actions)
The pure-Python eval core builds **offline-fixture-first**, so none of these
block the critical path to the wow. Resolve before any **live** Gemini/MCP/ADK run:

| Item | Verify-gate | Status | Action |
|---|---|---|---|
| Gemini/ADK access + ADC auth | — | ⛔ not done | `gcloud` is NOT installed. Install Google Cloud SDK, then `gcloud auth application-default login`; confirm one model completion. |
| Gemini call signature | `G_GEMINI` | ⛔ pending | confirm exact API after ADC auth |
| MCP stdio round-trip | `G_MCP` | ⛔ pending | after env + a hello MCP server; record the SDK + transport API actually used |
| Antigravity CLI syntax | `G_ANTIGRAVITY` | ⛔ TO VERIFY | confirm install/run/deploy commands vs **official Antigravity docs** before any README command. Do NOT hand-write unverified syntax. |

**Owner to run** (interactive — cannot be automated from here):
```bash
brew install --cask google-cloud-sdk      # if gcloud absent
gcloud auth application-default login
```

### Open plan decisions still to pick (Phase 1)
Iconic video scene (三顧茅廬 default) · independent gold checker (person vs scholarly summary) · the 2 extra eval micro-scenes.

### Next: Task 0.3 — seed `specs/` (product_spec, eval_plan w/ the single canonical gate, threat_model, behavior.feature, demo_script, writeup_outline) + `AGENTS.md` + `docs/capstone_writeup.md`.

## Phase 2 — Security hardening: venv CVE cleanup (2026-06-27)

**CVEs before:** 1 (pytest 8.4.2 / CVE-2025-71176)
**CVEs after:** 0

**Action taken:** Upgraded `pytest==8.4.2` → `pytest==9.0.3` (minimum patched version per pip-audit fix recommendation). No removal needed — all other packages were clean.

**Import-path audit:** Grep of `guwen_core/`, `app/`, `evals/` confirmed pytest is a test-runner direct dep only (not imported in production code). No urllib3/requests/starlette/tornado present in project venv pre-audit; those appeared transiently as pip-audit's own transitive deps and were removed after audit completed.

**Packages removed:** None from project venv (pip-audit's 21 transitive additions were uninstalled post-audit, restoring clean 19-package state).

**requirements.txt change:** `pytest==8.4.2` → `pytest==9.0.3`.

**Verification:** `pytest evals/ -q` → 42 passed in 0.38s (Python 3.14.4, pytest-9.0.3). Rollback snapshot: `/private/tmp/claude-501/-Users-surahli/7dd5375f-ddf7-468e-a98e-eb386946d188/scratchpad/venv-freeze-before.txt`.
