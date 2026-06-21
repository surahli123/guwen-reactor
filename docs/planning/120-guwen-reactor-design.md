# Guwen Reactor — Capstone Design Doc (v1)

Status: office-hours output, pending /grill-me + user approval. Plan-only; no code until "go".
Companion: 00 requirements · 100 final-decision · 110 mvp-scope. Reuse GPT's 4 diagrams in the Writeup/video.

## One-liner
A **source-grounded cross-cultural adaptation agent**: it turns a public-domain Classical
Chinese story into English-friendly artifacts (story card, cultural decoder, storyboard) and
**proves its fidelity with a measured evaluation harness** + human approval before export.
Not a translation tool. Not a video wrapper.

## Track & user
- **Track:** Agents for Good (education / cultural accessibility / supporting the arts).
- **Primary user (capstone build):** English-speaking **learners + educators** who want to
  finally UNDERSTAND the classics (the builder is the user; + diaspora adults + curious English
  readers + world-lit teachers). Creator / short-form-script production = the commercial/vision
  segment (see Positioning) → pitched in the Writeup, built in v2.
- **Problem:** Classical Chinese fiction is culturally rich but inaccessible — language, idioms,
  history, unfamiliar values, hard to adapt visually, and trust/copyright risk.

## Differentiator
Source-grounded fidelity + a rigorous, MEASURED evaluation (the builder's DS edge), on
public-domain source (zero IP risk) — versus plain translation (no cultural context) or
one-shot AI comic gen (hallucinates, no eval, copyright-murky).

## Positioning / future-fit (Writeup vision — NOT v1 build scope)
The engine is a **generalizable source-grounded cross-cultural content adaptation workflow**:
Classical Chinese → English is the v1 WEDGE, but the same domain-agnostic chain (source guard →
interpretation → localization → storyboard → eval) generalizes to ANY non-English classical /
cultural text, and commercially to **creators + educators who need source-grounded, culturally
accurate short-form scripts from non-English texts** (ChatGPT VC framing: sell the cross-cultural
adaptation workflow, not "古文"). This is the Writeup's "why agents / future-fit" story.
**Discipline:** pitched, NOT built — the 17-day build stays narrow (one scene, learners/
educators, comprehension artifacts + eval). Creators / short-form / video = v2.

## Architecture (accepted target; reuse GPT diagrams in Writeup)
Orchestrator agent (reads AGENTS.md/specs, routes skills)
→ **Skills layer**: source-license-guard · classical-interpretation · cultural-localization ·
  reaction-script · storyboard · adaptation-evaluation
→ calls tools **through MCP only**
→ **Local MCP server `guwen_mcp`**: source · artifact · schema · eval · export · trace tools
→ **Artifact + trace store**: story_spec.yaml, storyboard.yaml, eval_report.yaml, trace.jsonl,
  (agbom.yaml, vibe_diff.yaml — lightweight)
→ **A2UI run canvas**: Story Card | Source | Storyboard | Eval | Trace + **Human Approval**
→ **Policy + export gate**: Markdown / YAML / (SRT) / HTML / optional slideshow.
Canonical flow: Source Guard → Story Spec → Canon Memory → Cultural Localization →
(Reaction Script) → Storyboard → Eval → Human Approval → Export.

## The evaluation harness (the WOW — must be MEASURED, not illustrative)
- **Ground truth = Canon Memory** (characters/relationships/plot-beats/key-facts extracted from
  the source) → makes a subjective task semi-objective.
- **Metrics:**
  - Faithfulness: every artifact claim/panel maps to Canon Memory; no unsupported events →
    **precision/recall** (entailment-style).
  - Cross-cultural clarity: **LLM-judge calibrated to a small human-labeled set** (report kappa);
    pairwise, not 1-5.
  - Trajectory eval: required MCP calls occurred in the correct order (from trace.jsonl).
  - Deterministic tests: schema valid, source coverage, export validity.
- **Calibration:** baseline = naive one-shot prompt (no source-grounding) must fail **30-40%**
  → proves the agent's lift; no "broken ruler."
- **Trust gate (from WBFA pattern):** export only if faithfulness + clarity pass threshold;
  else emit a "diagnostic: panel N contradicts source on X" report. HITL approves.
- **Demo targets:** Faithfulness ≥4/5, Cross-cultural clarity ≥4/5, Copyright readiness = pass,
  Export requires approval.

## Build discipline (the realism layer — see 110)
**Walking skeleton first:** thinnest end-to-end path through ALL boxes on ONE famous scene
(rec《三顾茅庐》or《大闹天宫》), then deepen. Every box exists (hits all concepts + trace runs
end-to-end), depth added where time allows.
**Fallback cut-list (drop in this order if behind):** image generation → SRT subtitles →
reaction-script → full AgBOM/Vibe-Diff → A2UI protocol (fall back to static HTML) → multi-scene.
**Never cut:** eval harness + one scene + cultural decoder + storyboard.

## Course concepts demonstrated (>=3 gate → 5-6)
ADK multi-agent (orchestrator + skills) · MCP server (`guwen_mcp`) · Agent skills (skills library
/ Agents CLI) · **Evaluation** (showpiece) · Security (policy gate + AIGC label + HITL + no
auto-publish) · Deployability (export bundle / canvas) · Antigravity (shown in the build video).

## Safety / copyright
Public-domain source only (source-license-guard enforces); AIGC label on outputs; HITL approval
before any export; no auto-publish; no API keys in repo.

## Submission mapping (Kaggle, due Jul 6 23:59 PT)
- **Writeup (≤2,500 words):** problem → solution → architecture (GPT diagrams) → the eval story
  (measured numbers) → journey. Select track = Agents for Good.
- **Video (≤5 min, YouTube):** climax = eval scorecard CATCHES a seeded faithfulness drift →
  HITL rejects → regenerate → pass → export. Show architecture + Antigravity build.
- **Public repo (GitHub):** README (problem/solution/architecture/setup/diagrams), runnable on
  public-domain sample, eval harness + gold set, no secrets.
- **Cover image + media gallery** required.

## Risks
1. Over-scope ("More Layers") → walking skeleton + cut-list.
2. Eval becomes vibes → measured metrics + judge calibration + 30-40% baseline (non-negotiable).
3. Storyboard image quality (if image-gen attempted) → keep visual prompts as TEXT for v1; image-gen is first on the cut-list.
4. Solo + vibe-coding level → lean on ADK/Antigravity codegen + spec-first; the builder is architect.

## Open (minor)
Resolved: primary user (build) = English-speaking learners + educators; commercial vision =
cross-cultural adaptation workflow (creators+educators) pitched in Writeup. Remaining: pick the
demo scene (《三顾茅庐》 vs 《大闹天宫》).
