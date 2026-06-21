# Planning archive

This directory is the **research → product handoff**: the full decision and
design trail for Guwen Reactor, copied verbatim from the original lab notebook
at `~/notes/kaggle-vibecoding/` (originals preserved there). It is documentation,
not code.

## Binding entry points (read these first)

1. **[`200-guwen-FINAL-execution-handbook.md`](200-guwen-FINAL-execution-handbook.md)** — the single source of truth for scope, the 10-day schedule, the cut-list, and the absolute floor.
2. **[`210-v3-acceptance-and-plan-gate-decision.md`](210-v3-acceptance-and-plan-gate-decision.md)** — the plan-gate PASS decision and the binding reconciliation (what is P0 vs V2-if-time).
3. **[`guwen-v3/`](guwen-v3/)** — the adopted *technical reference* spec (eval plan, threat model, AGENTS, behavior spec, rater sheet, writeup outline). Mechanisms only; scope is governed by `200`.

## Map of the trail (by number)

| Range | Phase |
|---|---|
| `00`–`05` | Course material (capstone rubric + the 5 whitepapers) |
| `10`–`90` | Demand research → idea slate → idea selection (Guwen Reactor chosen) |
| `100`–`120` | Final idea decision → MVP scope → design |
| `140`–`180` | GPT adversarial handoffs + grill + deep review |
| `190`–`210` | 10-day hardened plan → final execution handbook → plan-gate decision |
| `guwen-bundle/` | v2 spec bundle (superseded by v3) |
| `guwen-v3/` | v3 build-ready technical reference (adopted) |
| `research/` | Raw demand-research scouts (idea-validation phase; kept for the trail) |

## Status

Plan stage **passed** (2026-06-20). No application code yet — the build begins
on the owner's explicit "go". The implementation plan (turning `200` into
executable tasks) is the next step.
