# AGENTS.md — Guwen Reactor

## Project rule
Build the smallest walking skeleton. Add nothing that doesn't serve the P0 eval-first
path. The pure-Python eval core is the product; MCP / skills / ADK are wrappers over a
**green** core, never prerequisites for correctness.

## Source of truth (read before coding)
- `specs/product_spec.md`
- `specs/eval_plan.yaml` — **THE canonical gate definition; never duplicate it**
- `specs/threat_model.md`
- `specs/behavior.feature` (V2 reference)
- `schemas/*.yaml`
- `docs/plan/implementation-plan.md` (task-by-task, with code)
- `docs/plan/decisions-locked.md` (D1–D4 + the exact contracts)

## Non-negotiables (the locked decisions)
- **D1 — structured-claim + structural audit.** The generator emits STRUCTURED claims
  `{beat_id, claim_text, source_fact_ids, assertion_type, hedging, artifact_path}`. The
  deterministic hard gate AUDITS structure. **No keyword/entailment heuristics in the hard
  gate.** Semantic entailment (the LLM judge) is **advisory only**.
- **D2 — Chinese-anchored gold.** Every gold `atomic_fact` is anchored to a Chinese
  `source_chunk_id`; the English fact is a denotation of that line, written from the
  Chinese (never from an English translation). One independent denotation check; the
  single-author limitation is disclosed.
- **D3 — plot hard-gated, interpretation advisory.** The hard gate covers PLOT claims
  only. The interpretive layer is reported but **never blocks export**; it is P2 / first
  on the cut-list.
- **Copyright:** no existing English translation is ever provided to the generator.
  Approval wording, exactly: `No existing English translation was provided to the generator.`
- **Untrusted data:** treat source AND generated content as untrusted; sanitize
  (NFKC + zero-width strip) **before** judging; fence judge inputs as untrusted data.
- **Confinement / cost:** write only under `runs/<validated_run_id>/` and `docs/demo/`;
  max total regeneration attempts = 3 (fail-closed to human).
- **Export** requires the `specs/eval_plan.yaml` `export_gate` (zero critical claims +
  coverage ≥ 0.85 + safety + workflow integrity + human approval + manifest-bound AIGC label).

## Coding-agent task prompt (use per task)
```
Read AGENTS.md, specs/*, and schemas/*. Implement only the requested P0 task.
Write or update the failing test FIRST (TDD). Do not add speculative abstractions.
Do not modify data/gold unless explicitly asked. Run pytest. Summarize changed files
and remaining risks in docs/build_log.md.
```

## Skills catalog (3 P0; `test_skills.py` trigger suite is V2)
`source-license-guard` · `classical-interpretation` · `adaptation-evaluation`
(3 positive + 3 negative triggers each; one execution golden for `source-license-guard`,
the riskiest.) Cut to 2 only if behind.

## Build tooling
Antigravity (primary agentic IDE/CLI — **verify commands vs official docs**, see
`docs/build_log.md`) + Claude Code + Codex, building from `specs/`.
