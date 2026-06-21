# Guwen Reactor

A **source-grounded cross-cultural adaptation agent**: it takes public-domain
Classical Chinese (古文 *gǔwén*) — ingesting the **original Chinese only** and
generating its own English — and produces an English **story card + cultural
decoder + text storyboard**, behind a **measured, deterministic faithfulness
gate** that catches a planted hallucination and refuses to export until a human
approves.

> **Kaggle "AI Agents: Intensive — Vibe Coding" capstone.**
> Track: **Agents for Good**. Deadline: **2026-07-06**.

## Status

🟡 **Planning complete — build not started.**
The plan stage passed its gate on 2026-06-20 (see
[`docs/planning/210-v3-acceptance-and-plan-gate-decision.md`](docs/planning/210-v3-acceptance-and-plan-gate-decision.md)).
No application code exists yet; the build begins on the owner's explicit "go".

## The wow

A faithfulness gate that is **measured, not asserted**: precision reported as a
fraction with a denominator over ~30–40 claims, a deterministic hard gate
(`unsupported_critical_claims == 0` + required-beat coverage + forbidden-claim
match + safety + human approval), and a **planted-drift demo** that proves the
gate catches both a forbidden hallucination and a subtle invented one.

## Where to start reading

| File | What it is |
|---|---|
| [`docs/planning/200-guwen-FINAL-execution-handbook.md`](docs/planning/200-guwen-FINAL-execution-handbook.md) | **THE binding plan** — 10-day scope, day-by-day schedule, cut-list, absolute floor |
| [`docs/planning/210-v3-acceptance-and-plan-gate-decision.md`](docs/planning/210-v3-acceptance-and-plan-gate-decision.md) | Plan-gate decision + the P0-vs-V2 reconciliation |
| [`docs/planning/guwen-v3/`](docs/planning/guwen-v3/) | Adopted **technical reference** (eval / architecture / security mechanisms) |
| [`docs/planning/README.md`](docs/planning/README.md) | Index of the full planning archive |

## Concepts demonstrated (need ≥3 → targeting 5)

MCP server · Agent skills · Security (gate / sanitize / DoW cap / HITL) ·
**Evaluation** (the showpiece) · Deployability (cached static canvas + public repo).
Upside 6th: Antigravity (shown in the video).

## Copyright posture

Ingests **original Chinese public-domain text only** and generates its own
English. No copyrighted translations are stored or reproduced. The primary
judged artifact is a **cached static run snapshot + this public repo** — no live
API key sits in the judged path.

## Build tooling

Built via agentic engineering: **Antigravity** (primary agentic IDE/CLI) +
**Claude Code** + **Codex**, working from `specs/` (created during the build).
