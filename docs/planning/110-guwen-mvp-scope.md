# Guwen Reactor — MVP Scope Cut (solo, 17 days)

Written 2026-06-20. Office-hours premise-challenge of GPT's full spec (4 diagrams).
GPT's spec is an excellent ARCHITECTURE + writeup story (hits 5-6 course concepts) but is
over-scoped as a 17-day solo BUILD — the "More Layers" anti-pattern the course warns about.
Rule: **the diagram is the writeup; the build is a thin vertical slice of it.**

## Principle
Build ONE end-to-end vertical slice DEEP; stub the breadth; show the full architecture in
the writeup (reuse GPT's 4 diagrams). The evaluation harness is the showpiece and must
produce MEASURED numbers (not the illustrative radar).

## IN (the demo spine — build deep)
- **Source**: 1 public-domain classic, 1 famous scene (rec: 三国演义《三顾茅庐》 or 西游记《大闹天宫》 — plot-driven, iconic, globally recognizable). 2-3 scenes only if time allows.
- **Core agent chain** (orchestrator + skills, DAG handoff):
  1. **Source Guard** — public-domain check + load source text (light).
  2. **Canon Memory** — extract characters / relationships / plot-beats / key-facts = the "story bible" = the EVAL GROUND TRUTH. (Core — this is what makes the eval objective.)
  3. **Cultural Decoder** — English explanation + idiom/historical/values context. (Core — the "access" value prop.)
  4. **Storyboard** — panel beats + per-panel description + visual prompts as TEXT. (Core — the visual wow.)
  5. **Evaluation harness** — THE WOW:
     - Faithfulness: every claim/panel maps to Canon Memory; no unsupported events → precision/recall (NLI/entailment-style).
     - Cross-cultural clarity: LLM-judge **calibrated to a small human-labeled set** (report kappa).
     - Trajectory eval: required MCP calls happened in the correct order (from trace.jsonl).
     - Deterministic tests: schema valid, source coverage, export validity.
     - Baseline = naive one-shot prompt (no source-grounding) → must fail 30-40% (proves lift; no broken ruler).
  6. **Policy gate + HITL approval** — public-domain check, AIGC label, no auto-publish (light but present = security concept).
  7. **Export** — Markdown + YAML + a simple self-contained **HTML storyboard/scorecard canvas** (NOT full A2UI protocol).
- **Implementation**: ADK skills + a small **local MCP server** (`source.get_text`, `artifact.write`, `schema.validate`, `eval.run`, `trace.log`) → hits MCP + agent-skills concepts. **trace.jsonl** (OpenTelemetry-style) feeds trajectory eval.
- **Hero artifacts (pick 2)**: Cultural Decoder + Storyboard, with the **Eval Report** as the showpiece overlay.

## OUT / STUB (shown in writeup architecture, NOT built for v1)
- Full **A2UI protocol** → replace with a simple HTML canvas.
- **Reaction script, subtitles (SRT), image generation** from visual prompts → visual prompts stay TEXT; no image-gen; reaction/subtitles = v2.
- **AgBOM, Vibe-Diff, full observability store** → lightweight/illustrative; keep only trace.jsonl + approval_record.
- **Multi-story scale** → one scene first.
- The illustrative **radar chart** → keep for the writeup, but the real deliverable is MEASURED eval numbers.

## Concepts hit (>=3 gate) — easily 5
ADK multi-agent (orchestrator + skills) · MCP server (local, 5 tools) · Agent skills (skills library / Agents CLI) · Evaluation (the showpiece) · Security (policy gate + AIGC label + HITL) · Deployability (export bundle). Antigravity shown in the build video.

## Primary user (v1)
**Learner / heritage-seeker** (e.g., the user themselves + Chinese-diaspora adults + curious
English readers) who wants to finally UNDERSTAND the classics. Educator = secondary (same
artifacts). Creator (reaction/video production) = v2. This keeps the eval clean
(faithfulness + clarity) and the "access" problem sharp.

## 5-min video climax
《三顾茅庐》 → agent runs the chain → eval scorecard CATCHES a seeded faithfulness drift
(a panel inventing an event not in the source) → HITL rejects → regenerate → pass → export.
"The scorecard catches the hallucination" = the wow + proves the eval is real.

## Reuse
GPT's 4 diagrams (Why / System Design / Eval Gate / Capability radar) → drop straight into
the Writeup + video as the architecture story.
