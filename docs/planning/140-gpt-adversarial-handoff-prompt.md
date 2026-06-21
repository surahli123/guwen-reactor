# Adversarial Handoff Prompt → ChatGPT (challenge the Guwen Reactor spec, get a build-ready doc back)

Paste everything in the code fence below into ChatGPT 5.5 Pro.

```
ROLE
You are the lead architect of "Guwen Reactor." You are receiving an adversarial design
review from a skeptical principal engineer + senior product data scientist. For EACH
challenge: either defend it with concrete reasoning (steelman — if the reviewer is wrong,
say so and why) or revise the design. Then output a single BUILD-READY design spec doc.
Be concrete: name tools, files, schemas, metrics, thresholds. No hand-waving, no hype.

CONTEXT (self-contained)
- Event: Kaggle "AI Agents: Intensive — Vibe Coding" capstone. Due 2026-07-06 23:59 PT.
- Builder: SOLO, ~17 days, prompt-driven / "vibe-coding" skill level (NOT a strong manual
  debugger; acts as architect, leans on AI codegen + Antigravity/ADK).
- Scoring: Pitch 30 (core concept/value 10, 5-min YouTube video 10, writeup 10) +
  Implementation 70 (technical impl 50 + documentation 20). HARD GATE: demonstrate >=3 of
  {ADK multi-agent, MCP server, Antigravity, security features, deployability,
  agent skills / Agents CLI}. Deliverables: public GitHub repo + <=5-min YouTube video +
  <=2,500-word writeup + cover image.
- Project (LOCKED): "Guwen Reactor" — a SOURCE-GROUNDED cross-cultural adaptation agent that
  turns a PUBLIC-DOMAIN Classical Chinese story into English-friendly artifacts (story card,
  cultural decoder, storyboard) and PROVES fidelity with a MEASURED evaluation harness +
  human approval before export. Track: Agents for Good. Primary BUILD user = English-speaking
  learners + educators. Commercial VISION (writeup only) = a generalizable cross-cultural
  content-adaptation workflow. Differentiator: "not translation, not video-gen."
- Your spec under review: orchestrator agent + 6 skills (source-license-guard,
  classical-interpretation, cultural-localization, reaction-script, storyboard,
  adaptation-evaluation) → local MCP server `guwen_mcp` (source/artifact/schema/eval/export/
  trace tools) → artifact+trace store (story_spec.yaml, storyboard.yaml, eval_report.yaml,
  trace.jsonl, agbom.yaml, vibe_diff.yaml) → A2UI run canvas + human approval → policy/export
  gate (Markdown/YAML/SRT/HTML/optional slideshow). 6-stage eval: deterministic tests →
  policy & safety → LLM-as-judge → trajectory eval → human review (Vibe Diff) → export.

ADVERSARIAL CHALLENGES — address each explicitly:
C1. OVER-SCOPE / "MORE LAYERS." 6 skills + 6 MCP tool groups + A2UI + AgBOM + Vibe-Diff +
    7 output artifacts + a 6-stage eval + a 9-step canonical flow is the exact "stack more
    layers" anti-pattern the course livestream warned against — for a SOLO 17-day vibe-coder.
    Defend the scope, OR cut to a WALKING-SKELETON MVP: the thinnest end-to-end path through
    the core boxes on ONE scene, then deepen. Give an explicit BUILD ORDER and a prioritized
    FALLBACK CUT-LIST (what to drop first if behind schedule).
C2. EVAL MUST BE MEASURED, NOT ILLUSTRATIVE. The builder's entire differentiator is RIGOROUS
    evaluation; a radar of "target scores" is vibes. For EACH eval metric specify: the exact
    ground truth, how it is computed, and whether it is objective or judge-based.
    Specifically: (a) faithfulness as precision/recall against an extracted "canon memory"
    (characters/relationships/plot-beats/facts); (b) cross-cultural clarity via LLM-judge
    CALIBRATED to a small human-labeled set (report agreement/kappa; pairwise not 1-5);
    (c) a BASELINE (naive one-shot prompt, no source-grounding) that must fail 30-40% to prove
    lift and avoid a "broken ruler." How big is the gold set, who labels it, how is it built
    in days?
C3. BUILD-VS-PITCH COHERENCE. The capstone BUILDS the learner/comprehension vertical; do not
    pitch a commercial vision (creators / short-form scripts) the demo does not evidence.
    Re-anchor the vision on the reusable ENGINE/workflow (which the build proves), with
    creators as an explicit "next vertical," not a bait-and-switch.
C4. A2UI FEASIBILITY. Full A2UI protocol is emerging/advanced. Is it necessary for v1, or does
    a static self-contained HTML "run canvas" suffice? Specify the minimal viable UI and what,
    if anything, A2UI buys that justifies the risk.
C5. IMAGE-GEN / CHARACTER-CONSISTENCY TRAP. Cross-panel character consistency is the exact
    unsolved problem funded startups ($5M, $1.5M) still fail. Does v1 GENERATE images or keep
    visual prompts as TEXT? Justify; if images, how do you avoid the consistency wall in 17 days?
C6. DEMO CLIMAX. Specify the SINGLE 5-minute-video moment that proves the eval works (e.g.,
    the scorecard catches a planted faithfulness drift → HITL rejects → regenerate → pass →
    export). Give the exact demo script/path.
C7. COPYRIGHT PRECISION. The Chinese SOURCE may be public-domain, but most English
    TRANSLATIONS are copyrighted. Does the agent ingest the ORIGINAL Chinese and produce its
    OWN English (clean), or reuse an existing English translation (IP risk)? State the exact
    source text + edition/licensing, and how source-license-guard enforces it.
C8. CONCRETE STACK + GROUND-TRUTH. Name the exact stack (ADK? Python? which models? local MCP
    impl?) and show HOW the canon-memory gold set for ONE scene is constructed and validated
    in days.
C9. SKILLS TRIAGE. Of the 6 skills, which are ESSENTIAL to the walking skeleton vs deferrable?
    Map each to v1-build / v2-pitch.
C10. REALISTIC 17-DAY PLAN. A day-by-day with milestones, a "definition of done" per milestone,
    and where the cut-list triggers. Be honest about what a solo vibe-coder can actually ship.

REQUIRED OUTPUT — a single "Guwen Reactor — Build-Ready Spec v2" with these sections:
1. Problem & primary user (build) + positioning/vision (engine, not 古文).
2. Architecture: per component, mark V1-BUILD vs V2-PITCH (walking skeleton vs shown-in-writeup).
3. Evaluation harness: measured metrics, ground-truth construction, calibration, baseline,
   thresholds, trust gate. (This is the showpiece — most detail here.)
4. MVP build order (walking skeleton) + prioritized fallback cut-list.
5. Tech stack + canon-memory gold-set construction recipe.
6. Demo path (the 5-min climax) + how it maps to the rubric.
7. Copyright/source plan (exact text + licensing).
8. Concept-coverage map (which of the >=3 required concepts, where demonstrated: code vs video).
9. Risk register (top 5) + mitigations.
10. 17-day day-by-day with definition-of-done.

RULES: steelman where the reviewer is wrong (push back, don't capitulate). Keep the BUILD
narrow and put ambition in the writeup vision. Any claim the demo cannot show = cut or move to
vision. Prefer the course's "start simple, single orchestrator + a few skills, DAG handoff"
guidance over a big swarm. Output the spec doc only.
```
