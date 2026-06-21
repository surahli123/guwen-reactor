# Grill Report — Guwen Reactor Build-Ready Spec v2

Written 2026-06-20. Adversarial grill of GPT's `Guwen_Reactor_Build_Ready_Spec_v2.md`.
Spec v2 is genuinely strong and build-ready (accepted C1–C10, walking skeleton, measured eval,
clean copyright, 17-day plan with cut triggers). This report finds the soft spots that SURVIVE
v2 — the things that will actually bite during the build or under a judge's close look. Severity:
BLOCKER (fix before claiming the eval-wow) / CONCERN (will hurt if ignored) / NIT (cheap upside).

## What's genuinely strong (no change needed)
- Copyright solution: ingest original Chinese only, generate own English — clean, defensible.
- Planted-drift demo climax: block → regenerate → pass → approve → export. Great 5-min proof.
- Cut-list discipline + hard-no-cut floor (source guard, canon, faithfulness, drift, approval).
- Concept coverage: 5 of 6 (ADK, MCP, security, deployability, skills).

## BLOCKER — eval credibility (the differentiator must be bulletproof)

### G1 — Faithfulness precision rests on self-citation + a soft judge; the demo drift is a softball
Precision = supported_generated_claims / total. "Supported" depends on (a) the BuilderAgent
self-reporting `source_fact_ids` per panel, and (b) an LLM **contradiction judge** (the spec's
own "judge-based" part). The planted drift ("Hua Xin keeps the gold") is **pre-listed in
forbidden_claims** → an obvious, almost-hardcoded catch. Two gaps:
- A hallucinating agent can also emit a **plausible-but-wrong `fact_id`**; if the ID exists,
  the claim counts as "supported" unless the contradiction judge catches it.
- **Subtle** hallucinations (invented motivation/emotion, plausible unsourced detail) likely
  cite a valid ID AND survive the contradiction judge.
**Fix:** (1) demo must also catch a drift NOT in `forbidden_claims` (prove generality, not a
gotcha). (2) Calibrate the contradiction judge against human labels (same rigor as the clarity
judge: agreement ≥0.8, position-bias check). (3) Add an adversarial subtle-drift test (added
motivation/emotion) to the eval suite, not just the obvious forbidden one.

### G2 — Baseline comparison may be rigged ("broken ruler measuring my own scaffolding")
Faithfulness P/R is defined via `source_fact_ids`, which the naive baseline structurally cannot
produce → baseline auto-fails on the citation scaffolding, not on actual learner value. That is
the exact anti-pattern the user cares about (don't grade against your own scaffolding).
**Fix:** the fair baseline must ALSO be prompted to cite source facts (apples-to-apples), OR
faithfulness must be judged on the PROSE directly (claim-vs-source entailment) independent of
fact-ID presence. Report both the rigged and fair baselines if useful, but lead with the fair one.

### G3 — Recall is non-discriminating (does no work)
Recall = required_gold_beats_covered / total. It is **1.00 in BOTH the clean and the drift runs**
(per the demo). A metric that never varies isn't measuring quality — the eval effectively rests
on precision alone → single-metric fragility.
**Fix:** either drop recall as a headline (keep as coverage sanity check) and strengthen
precision (G1), or add a recall test that can actually fail (e.g., omit a required beat) so
recall earns its place. Don't present a constant as a result.

## CONCERN — build feasibility & sequencing

### G4 — The non-negotiable wow (eval) is sequenced LAST; ADK/MCP debugging will squeeze it
Day-plan puts faithfulness eval at **Day 9**, after MCP (D4), ADK two-agent (D5), skills (D6).
For a vibe-coder ("not a strong manual debugger"), ADK + stdio MCP + trace wiring can eat
multiple days. If they slip, the differentiator gets crushed. Also an internal inconsistency:
build-order calls faithfulness **P0**, day-plan schedules it Day 9.
**Fix:** build the eval harness FIRST as pure Python (it's the user's wheelhouse) — canon gold +
faithfulness + planted drift + approval gate runnable via CLI by ~Day 5. THEN wrap ADK/MCP
around a working, already-impressive core. De-risk the wow before the infra.

### G5 — The ≥3-concept gate has zero margin if both ADK and MCP slip
Cut-list permits cutting BOTH ADK and MCP (items 7–8). That leaves skills + security +
deployability = exactly 3. No buffer; one more slip = below gate.
**Fix:** lock at least ONE of {ADK two-agent, MCP server} as non-cuttable. Recommend MCP (a
small stdio server is more contained for a solo builder than multi-agent orchestration).

### G6 — Cross-cultural clarity depends on recruiting 2–3 human raters by Day 11 (external dependency)
If it slips to advisory, the eval-wow leans entirely on faithfulness (which has G1–G3 issues).
**Fix:** line up raters NOW (friends/classmates/Reddit/Prolific); pre-write the 10-pair labeling
sheet so it's a 30-min ask. Treat 2 raters as the real plan, 3 as upside.

## CONCERN — wow vs eval tension

### G7 — The demo source is eval-clean but low-recognition/low-visual-wow
"Guan Ning Cuts the Mat" = a 3-sentence, obscure (to English audiences) anecdote about cutting
a mat. Perfect for a clean small gold set, but it undersells the "broad recognition + visual wow"
the user explicitly prioritized — and it's far from the 《西游》/《聊斋》 drama the user loves.
**Fix (pick one, consciously):** (a) keep Guan Ning for the eval gold but make the VIDEO demo a
more iconic scene (三顾茅庐 / 大闹天宫 / a 聊斋 ghost tale) so the 5-min reel has visual+emotional
pull; or (b) accept the small-scene trade-off and lean the wow entirely on "the scorecard catches
a hallucination" (mechanism wow, not story wow). Don't sleepwalk into the obscure-anecdote demo.

## NIT — cheap upside
- **G8:** Antigravity is dismissed ("not core gate"). It's a named course concept — actually
  building in Antigravity and showing 20s of it in the video = a near-free 6th concept.
- **G9:** Make the **cached-demo** the PRIMARY public judge link (deterministic, no Gemini key /
  rate-limit risk during judging); live Streamlit is the optional bonus, not the judged path.

## Bottom line
Spec v2 is buildable today. The grill is not "it won't work" — it's "if you don't fix G1–G3,
your evaluation wow looks rigorous but is shallow on close inspection, and the eval is the one
thing you're betting on." G4–G6 are sequencing/feasibility insurance. G7 is the recognition-vs-
eval trade-off to make on purpose, not by default.
