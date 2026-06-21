# FINAL Round-2 Handoff → ChatGPT (grill G1-G9 + deep-review B1-B4 + concerns → Spec v3)

Paste the code fence into ChatGPT 5.5 Pro (the chat that produced Spec v2). Supersedes 160.
Full deep-review detail: 170-deep-plan-review.md.

```
ROLE
You are the lead architect of "Guwen Reactor." Your Build-Ready Spec v2 passed an adversarial
grill AND a 7-lens course-grounded deep review (eval-rigor, architecture, product, security,
delivery, rubric, course-alignment). v2 is strong — KEEP its strengths (walking skeleton, clean
copyright via original-Chinese-only, planted-drift climax, cut-list, the existing
unsupported_critical_claims==0 count gate, write_artifact's sha256, the fully-specified clarity-
judge calibration recipe, the honest C1-C10 history). Produce "Build-Ready Spec v3" that fixes
the findings below.

CRITICAL META-RULE: the #1 finding is OVER-SCOPE. Fix SURGICALLY. Most fixes are reframes,
calibration copy-paste, small files, or sequencing — NOT new subsystems. Do NOT add layers,
agents, or tools to "address" a finding. Keep the walking skeleton. If a fix would expand the
build, move it to V2-pitch and say so. Steelman where the reviewer is wrong.

TIMELINE CONSTRAINT (HARD): assume ~10 WORKING days end-to-end, NOT 17. Re-cut the day-plan to 10
days, eval-FIRST, with a buffer day + a 1.5x-budget circuit-breaker. Under 10 days the eval-wow
must rest on the DETERMINISTIC faithfulness gate (unsupported_critical_claims==0 + required-beat
coverage + forbidden-claim match); DEMOTE the LLM contradiction judge to advisory (skip the
calibration study — too costly for 10 days); NARROW the product claim to "source-grounded plot
fidelity"; CUT the clarity human study (advisory-only). Push to V2-if-time: judge calibration,
clarity study, interpretive-field rubric, BDD/Gherkin, skill-level eval suite, non-Chinese demo
scene, live Streamlit. KEEP (cheap + concept-bearing): threat_model + source sanitize (B2), a
1-line DoW regen cap (S7), AIGC integrity via existing sha256 (S6), a 1-line session-convergence
log (E8), Antigravity shown in video (free 6th concept). Non-negotiable core = deterministic
faithfulness gate + planted-drift block + 1 scene + MCP (locked) + 3 skills + security + cached
static demo + 5-min video.

=== BLOCKERS (fix before build) ===

B1. CALIBRATION ASYMMETRY (extends grill G1). The spec calibrates the ADVISORY clarity judge
    (§3.5: agreement>=0.80 + position-bias check) but the EXPORT-GATING faithfulness/contradiction
    judge (§3.4) gets NO calibration. Course (02 §6) makes calibration non-negotiable for ALL
    judge usage. At n=6, 5/6 vs 4/6 flips pass/fail — that's an anecdote, not calibration. FIX:
    copy the §3.5 recipe onto the contradiction judge (hand-label ~20 (claim, gold-fact) pairs,
    swapped-order + paraphrase stability, require >=0.80-0.85 before it may gate), and add
    `contradiction_judge_calibrated` to export_requires. If you can't hit that n, make the HARD
    gate the DETERMINISTIC checks (valid fact ID + forbidden-claim match + required-beat coverage)
    and DEMOTE the LLM contradiction judge to advisory — the exact pattern you already use for clarity.

B2. SOURCE-TEXT PROMPT INJECTION + EMPTY threat_model.md (new). source.zh.txt is fed verbatim to
    BuilderAgent AND the contradiction judge; the planted-drift demo injects an attacker-controlled
    caption that flows into the judge prompt — an injection ("ignore prior instructions") could
    subvert the gate the whole demo rests on. And threat_model.md is a listed Day-1 deliverable
    (§10) + file-tree entry (§2.3) with ZERO specified content = a submission gap. Course: 01 indirect
    injection / invisible payloads; 05 §7 context hygiene (the 50-hallucinated-emails incident). FIX
    (cheap): (1) write threat_model.md naming "indirect injection via source text" + "judge-prompt
    injection via generated content" with mitigations; (2) strip/normalize zero-width + homoglyph
    chars at ingestion; (3) wrap source + generated content in delimited data-fences with a system
    instruction treating fenced text as untrusted data. Add a 10-second "injection-resistance" demo
    beat — a real differentiator for a security-themed capstone.

B3. RE-SEQUENCE: deterministic-Python core FIRST (extends grill G4). The day-plan builds cuttable
    infra (MCP Day 4, ADK Day 5) BEFORE the non-cuttable gradeable core (faithfulness Day 9), with
    zero env bring-up time and zero buffer — and the spec's OWN §4.2 ranks faithfulness P0 and its
    OWN risk register says "pure Python first, wrap in MCP after tests pass." Course: 04 "start
    simple, scale on boundaries"; "Agent = Model + Harness, most failures are config failures"
    (env bring-up IS work). FIX: Days 2-5 = pure-Python vertical (source → canon_gold → adaptation
    via direct Gemini call → deterministic faithfulness + drift + approval gate, runnable by CLI).
    Days 6-9 = wrap MCP / ADK-critic / skills / trace ONE layer at a time over the green core. Add
    Day 0.5 "harness hello-world" (ADK installed, ADC auth, one Gemini completion, one MCP stdio
    round-trip) BEFORE feature work. Designate Days 13 + 17 as buffer + a 1.5x-budget circuit-breaker.
    This makes every cut-list cut a NO-OP (don't run the wrapper) instead of a destructive refactor.

B4. EVAL STATISTICAL FOUNDATION (mostly new; the wow must survive a DS judge). Four sub-fixes:
    (a) Denominator: aggregate generated claims across all 3-5 gold scenes (~40-60) before computing
        a rate; report precision as a fraction with denominator (11/12) not a rounded float; keep the
        existing `unsupported_critical_claims==0` COUNT as the headline hard gate; precision descriptive.
    (b) Construct validity: the interpretive fields (`why_it_matters`, `modern_analogy` = the
        cross-cultural ADAPTATION value) are UN-gated; you measure the easy half (plot-beat citation)
        and market it as the whole product. Either narrow the product claim to "source-grounded plot
        fidelity," OR add a small gold rubric (2-3 acceptable framings + 2-3 distortions) for the
        interpretive fields.
    (c) Contaminated gold: builder writes canon + prompts + validates = zero independent ground truth
        on an obscure text. Get ONE independent check on the demo-scene gold (Chinese-literate person
        or a published scholarly summary, cross-check plot BEATS not prose), use a DIFFERENT model
        family as Pass-3 critic than the generator, disclose single-annotator gold as a limitation.
    (d) Clarity confound: Pair A (full output) vs Pair B (baseline) differ on FORMAT/RICHNESS, not
        the grounding mechanism. Either give the baseline the SAME template (differ only on grounding),
        OR scope the clarity claim to "the full format is clearer than a plain translation."

=== HIGH-VALUE CONCERNS (fix cheaply; no new subsystems) ===

EVAL: E5 compute baseline-fail on the FAIR metric (prose-vs-source entailment, baseline also asked
to cite) + report failure-MODE breakdown not just the 30-40% band. E7 rename "trajectory_gate" →
"workflow integrity test" AND add a real cheap trajectory metric on the regen loop
(iterations_to_converge, did the corrected panel re-cite the right fact, loop token cost). E8/C11
log session-convergence (regenerate_rounds, converged, cost_to_converge) — the course's "single most
informative eval" (Tip 3), free from your regen loop; frame planted-drift→regen as a labeled-
correction convergence demo. E6 specify panel-claim granularity (one claim per caption + one per
decoder term) + a 10-extraction reproducibility spot-check. E10 move clarity_pairwise_preference_rate
out of per-run trust_gate into a corpus-level summary.

SECURITY: S5 `safety_pass` is a REQUIRED gate with NO evaluator — implement the course two-layer
pattern minimally (structural deny-list + ONE semantic LLM call "does this ADD violence/sexual
content NOT in the source?"; faithful classical violence passes). S7/C10 the regen loop has no
budget cap = Denial-of-Wallet — hard cap (3 → fail-closed to human) + log attempts/cost (same fix
serves DoW + trajectory + convergence). S6 the AIGC label has no integrity binding — embed it in
story-card footer / storyboard header / run_canvas.html + a manifest binding {artifact→sha256→label}
(write_artifact already returns sha256). S1 reword the approval_diff copyright claim from "no
copyrighted translation used" to "no existing English translation was provided to the generator."
S9 confine write paths to runs/<validated_run_id>/, reject path separators.

ARCHITECTURE / COURSE: A4 (highest-ROI de-risk) specify a file-reference handoff contract — Builder
writes runs/<id>/*.yaml and emits PATHS; orchestrator passes paths via ADK session state; Critic
reads from disk; the judge gets ONLY the {claim, gold-fact} pair (course 02 §10 Decouple State / not
context-as-database); add test_handoff_passes_paths_not_blobs. A5 specify the retry/regenerate
contract (max_retries=2; route {failing_claim, gold_fact, eval_reason} back, not the whole artifact;
persistent failure → export stays BLOCKED = a GOOD demo outcome); add test_regenerate_loop_blocks_
then_passes. A1/C2/C3 collapse thin-wrapper MCP tools (record_trace, validate_artifact_schema) to
plain Python; keep ~3-4 real high-level MCP tools (get_source returning {id, char_count, uri} not
raw text; check_source_policy; run_eval_suite; render_run_canvas). A6 emit trace deterministically
from the orchestrator (not a model-visible record_trace the LLM may forget); name events with
OpenTelemetry span types (agent.session/think/tool); use ADK's built-in trajectory eval (IN_ORDER).
A2/R6/C12 give CriticAgent a REAL decision loop (read eval_report → reason which panels failed & why
→ targeted regenerate → re-evaluate) and add one sentence: "Builder/Critic are split because the
evaluator must be a separate trust boundary that cannot edit what it grades." C4 add
specs/behavior.feature (BDD/Gherkin: clean run exports / drift blocks / regen passes / missing-
license blocks / no-approval blocks) and wire trajectory+policy tests to it (SDD is a course pillar).
C6 add evals/test_skills.py (3 pos + 3 neg triggers per skill + 1 execution golden for the 2 riskiest);
report trigger accuracy; DoD = "trace shows >=1 skill loaded on task-match," not file existence; cut
to 3 skills if 5 can't clear trigger tests.

PRODUCT / DEMO: P2 (decision) RE-ANCHOR the primary user to the EDUCATOR — source-grounding protects
the party ACCOUNTABLE for accuracy who can PERCEIVE fidelity; a learner who can't read Chinese can't,
so to them the agentic apparatus looks like overhead vs one-shot ChatGPT. Wedge becomes "classroom-
trustworthy, can't-get-fired-for-a-hallucination." (Keep learner as beneficiary.) P3 then give
educators a near-zero-cost teaching_pack (3 discussion Qs + 1 "gold says vs common misreading") or
drop the word. P1 the demo must SHOW a rendered story card + cultural decoder + 2-3 panels (value
proof) BEFORE the trust proof — open 0:30-1:30 on the rendered run_canvas. P5 two-beat climax:
(1) recognition beat (decoder turns 割席 into a felt modern analogy) THEN (2) trust beat (block a
planted lie) — head then heart. P4 state ENGINE = {schema + source-guard + faithfulness-gate + HITL}
(only canon_gold is culture-specific); optionally run the harness once on a non-Chinese public-domain
micro-scene (Aesop fable, 5-fact gold) to convert "reusable engine" from asserted to demonstrated.
G7/P6 keep Guan Ning for the eval gold but use an ICONIC scene (三顾茅庐 / 大闹天宫 / a 聊斋 tale) for
the VIDEO. P7 fix the "Reactor/Remixable" naming leak from the abandoned reaction-video pivot.

RUBRIC / VIDEO / DELIVERY: R1 the 5-min video must hit ALL FIVE rubric beats (Problem / Why-agents-
unique / Architecture / Demo / The-Build) — currently 2 of 5. R4/G8 build in Antigravity + show
20-30s in "The Build" = the free 6th concept that also fills R1's empty beat. R3 add a writeup
outline + word budget; use the C1-C10/grill/deep-review pivot history as the "project journey"
sub-criterion. R5 promote the required cover image to a tracked Day-17 item (reuse the architecture /
eval-climax diagram). R8 give the Documentation milestone a rubric-mirrored checklist (problem /
solution / architecture+diagram / verified copy-paste setup / results table / no keys). D2 make
docs/capstone_writeup.md a LIVING doc from Day 1 + pre-record demo segments as features land. D5
recruit the 2-3 clarity raters as a Day-1/2 task + pre-written label sheet (collection window Days
8-12; plan to 2, advisory fallback). D6/R7/G9 make the cached static run_canvas.html + public repo
the PRIMARY judged link (build the --cached loader Day 7, use it for ALL demos + the video); live
Streamlit is optional bonus, verified logged-out/no-key.

=== REQUIRED OUTPUT — "Guwen Reactor — Build-Ready Spec v3" ===
- Open with a "v3 changes" table: one row per B1-B4 + each concern group (fixed / defended + how).
- Keep v2's section structure. Most-changed sections: §3 Evaluation (B1, B4, E5-E10), §10 day-plan +
  §4 build-order (B3 resequence + buffers + Day-0.5), new §threat-model summary (B2), §2/§5
  architecture (A1-A6 tool/handoff/trace), §6 demo (P1/P5/P2/G7 + injection beat), §8 concepts
  (Antigravity), §1 user (P2 educator re-anchor). Add Section 11 "Build & Deploy Tooling": Antigravity
  as primary agentic IDE + Antigravity CLI (commands verified vs official docs, else "verify vs docs");
  Claude Code + Codex as the coding agents building from specs/; the "built via agentic engineering"
  meta-narrative; cached link as primary.
RULES: keep v2's strengths; SURGICAL fixes only, NO scope expansion (move ambition to V2-pitch); every
eval claim measured AND calibrated; steelman where the reviewer is wrong. Output the spec only.
```
