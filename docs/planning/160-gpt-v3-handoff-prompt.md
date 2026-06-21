# v3 Adversarial Handoff → ChatGPT (fix the grill findings, return Spec v3)

Paste the code fence into ChatGPT 5.5 Pro (same chat that produced Spec v2).

```
ROLE
You are the lead architect of "Guwen Reactor." Your Build-Ready Spec v2 went through an
adversarial grill by a senior product data scientist + principal engineer. v2 is strong and
accepted — KEEP its good parts (walking skeleton, clean copyright via original-Chinese-only,
planted-drift climax, cut-list, 5/6 concept coverage). This is round 2: fix the SURVIVING soft
spots, ESPECIALLY the evaluation harness (the project's entire differentiator). For each finding:
fix it concretely in the spec, or defend it with reasoning (steelman — if the reviewer is wrong,
say why). Then output "Guwen Reactor — Build-Ready Spec v3."

GRILL FINDINGS TO RESOLVE

BLOCKER — evaluation credibility (must be bulletproof; it's the whole bet):
G1. Faithfulness precision rests on (a) the BuilderAgent self-reporting source_fact_ids and
    (b) an LLM contradiction judge — and the planted demo drift ("Hua Xin keeps the gold") is
    PRE-LISTED in forbidden_claims, i.e. a near-hardcoded gotcha. A hallucinating agent can also
    emit a plausible-but-wrong fact_id, and SUBTLE hallucinations (invented motivation/emotion,
    plausible unsourced detail) can cite a valid ID and survive the judge. FIX: (1) the demo must
    also catch a drift that is NOT in forbidden_claims (prove generality); (2) calibrate the
    contradiction judge against human labels with the same rigor as the clarity judge (agreement
    >=0.8 + position-bias check); (3) add an adversarial subtle-drift test (added motivation /
    emotion / unsourced detail), not just the obvious forbidden one.
G2. The baseline comparison may be rigged: faithfulness P/R is defined via source_fact_ids, which
    the naive baseline structurally cannot produce, so it auto-fails on scaffolding rather than on
    learner value ("measuring against my own scaffolding"). FIX: make the fair baseline ALSO be
    prompted to cite source facts (apples-to-apples), OR judge faithfulness on the PROSE directly
    (claim-vs-source entailment) independent of fact-ID presence. Lead with the fair baseline.
G3. Recall is non-discriminating: it is 1.00 in BOTH the clean and the drift runs (per the demo),
    so it measures nothing. FIX: either demote recall to a coverage sanity-check (not a headline
    result) and strengthen precision, or add a recall test that can actually fail (omit a required
    beat). Do not present a constant as a result.

CONCERN — feasibility & sequencing:
G4. The non-negotiable wow (eval) is scheduled Day 9, AFTER MCP (D4), ADK two-agent (D5), skills
    (D6) — risky for a vibe-coder whose ADK/MCP debugging can slip and crush the differentiator.
    Also an internal inconsistency: build-order calls faithfulness P0 but the day-plan puts it
    Day 9. FIX: resequence so the eval harness is runnable as PURE PYTHON via CLI by ~Day 5
    (canon gold + faithfulness + planted drift + approval gate), THEN wrap ADK/MCP around the
    working core. Reconcile P0 vs Day-9.
G5. The >=3-concept gate has zero margin: the cut-list allows cutting BOTH ADK and MCP, leaving
    exactly 3 concepts. FIX: lock at least ONE of {ADK two-agent, MCP server} as non-cuttable
    (recommend MCP — a small stdio server is more contained for a solo builder).
G6. Cross-cultural clarity depends on recruiting 2-3 human raters by Day 11 (external dependency
    that often slips). FIX: add a concrete recruitment plan (who, channel) + a pre-written
    10-pair labeling sheet so it's a 30-minute ask; treat 2 raters as the plan, 3 as upside.

CONCERN — recognition vs eval trade-off:
G7. The demo source "Guan Ning Cuts the Mat" is eval-clean but a 3-sentence, English-obscure
    anecdote — it undersells the "broad recognition + visualization wow" the builder prioritized.
    FIX: decide explicitly — keep Guan Ning (and the small scenes) for the eval gold set, but make
    the 5-min VIDEO demo a more iconic scene (e.g. 三顾茅庐 / 大闹天宫 / a 聊斋 ghost tale) for
    visual+emotional pull; or consciously justify staying with the small scene and lean the wow on
    the "scorecard catches a hallucination" mechanism. State the decision + rationale.

NIT — cheap upside:
G8 (UPGRADED — build tooling is now a first-class requirement, not a nit). The capstone IS about
    vibe coding / agentic engineering, so BUILD Guwen Reactor ITSELF via agentic tools and make
    that part of the story:
    - Use **Antigravity** (Google's agentic IDE) as the PRIMARY build environment; deploy and use
      the **Antigravity CLI** as much as possible. Antigravity is a named course concept → capture
      it during the build and show ~20-40s in the video for concept credit.
    - Use **Claude Code + Codex** as the coding agents driving implementation from `specs/`
      (spec-driven: agents build from product_spec.md / eval_plan.yaml / schemas — this is the SDD
      concept in action).
    - Meta-narrative for writeup + video: "this agent was built via agentic engineering"
      (Antigravity + spec-driven + coding agents) — a living demonstration of the course's thesis.
    - DISCIPLINE: tools are the HOW, not the WHAT. Do not let a tool-tour eat eval time; the
      deliverable is still the narrow MVP. Specify exact Antigravity CLI commands ONLY if verified
      against official Antigravity docs; flag any uncertain command as "verify vs docs" — do not
      invent CLI syntax.
G9. Make the cached-demo the PRIMARY public judge link (deterministic, no Gemini key / rate-limit
    risk during judging); live Streamlit becomes the optional bonus, not the judged path.

REQUIRED OUTPUT — "Guwen Reactor — Build-Ready Spec v3":
- Start with a "v3 changes" section: one line per G1–G9 (fixed / defended + how).
- Keep v2's 10-section structure. Rewrite Section 3 (Evaluation) so faithfulness is robust
  (calibrated contradiction judge + subtle non-forbidden drift test + apples-to-apples baseline +
  recall that can fail). Update Section 4 (build order) + Section 10 (day-by-day) for the eval-first
  resequencing and the locked MCP. Update Section 6 (demo) for the G7 scene decision. Update
  Section 8 (concepts) for Antigravity. Update Section 5/9 for cached-demo-as-primary.
- Add a new Section 11 "Build & Deploy Tooling" (per G8): Antigravity as the primary agentic IDE
  + Antigravity CLI usage/deploy (commands verified vs official docs, else marked "verify vs
  docs"); Claude Code + Codex as the coding agents building from specs/; the "built via agentic
  engineering" meta-narrative; how each tool appears in the 5-min video. Keep it HOW-not-WHAT —
  no scope creep into the shipped product.
RULES: keep v2's strengths; do NOT re-expand scope; every eval claim must be measured AND
calibrated; steelman where the reviewer is wrong. Output the spec only.
```
