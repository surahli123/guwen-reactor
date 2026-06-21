# Deep Multi-Lens Plan Review — Guwen Reactor Build-Ready Spec v2

Written 2026-06-20. Synthesis of 7 adversarially-verified review lenses (eval rigor,
agent architecture, product/wedge, security/copyright, delivery feasibility, Kaggle
rubric, course-material alignment). Each lens was independently adversarially verified
against the actual spec; this synthesis keeps only CONFIRMED findings (dropping anything
the verifier marked "wrong", and noting "overstated" briefly), de-dups across lenses
**and** against the prior grill (`150-grill-spec-v2.md`, G1–G9), and cross-checks course
alignment against course notes `01`–`05` + synthesis `10`.

Severity legend: **BLOCKER** = fix before claiming the eval-wow / before build. **CONCERN**
= will cost points or eat the calendar. **NIT** = cheap upside.

> One framing note that recurs below: the *prior grill (G1)* already flagged "calibrate
> the contradiction judge." Three independent lenses (E4, S3, C1) re-derived the SAME gap
> but added a NEW dimension the grill missed — the **asymmetry**: the spec gives the
> *advisory* clarity judge a full calibration protocol and gives the *export-gating*
> faithfulness judge nothing. That asymmetry is the genuinely new, build-blocking insight.

---

## VERDICT

**NOT build-ready as-is — but close.** The spec is a strong, honest v2 (walking skeleton,
measured eval, clean copyright, cut-list discipline — see Strongest Parts). It is blocked
on four things that all undermine the ONE thing the project bets on (the eval-as-wow) or
that risk the calendar a solo weak-debugger cannot recover from:

1. **The gating faithfulness judge is uncalibrated while the advisory clarity judge is
   fully calibrated** (the asymmetry — E4/S3/C1). The export gate rests on the one judge
   the spec never validates.
2. **Indirect prompt injection from the source text is absent from the threat model, and
   `threat_model.md` is a listed Day-1 deliverable with zero specified content** (S2/C7).
   For a security-themed capstone this is both a real attack surface (a planted caption
   could carry "IGNORE PRIOR INSTRUCTIONS" into the gating judge) and a missing submission
   artifact.
3. **The day-plan builds cuttable infra (MCP Day 4, ADK Day 5) BEFORE the non-cuttable,
   gradeable value core (faithfulness Day 9), with zero environment bring-up time and zero
   buffer days** (D1/D3/D9 — and the spec's own §4.2 says faithfulness is P0). This inverts
   the risk so the differentiator is finished last by the person least able to debug it.
4. **The eval's statistical foundation is too thin to be the wow it's sold as** — single
   planted data point, no stated denominator, no extraction-reproducibility, and a clarity
   comparison confounded by output richness (E1/E2/E3/E9 + R/C cross-confirms).

Everything else is CONCERN/NIT and can be absorbed during the build. Fix the four blockers
(all cheap relative to their payoff) and this is build-ready. The recommended re-sequence
(deterministic-Python core first, harness wrapped around it) simultaneously de-risks 3 and
makes the cut-list cuts no-ops instead of destructive refactors (D7).

---

## RANKED MUST-FIX BEFORE BUILD

Ordered by (build-blocking risk × cheapness of fix). The structured object carries the
machine-readable version; this is the human-readable ranking with rationale.

### 1. Calibrate the GATING faithfulness/contradiction judge (or demote it) — BLOCKER
- **Lenses:** E4, S3, C1 (triple-confirmed). **New vs grill:** EXTENDS G1.
- **Course basis:** 02-paper2 §6 LLM-as-judge non-negotiables ("swap positions to
  eliminate ordering bias; calibrate against human ratings until ~90% agreement"); 10
  "pairwise comparison (not 1-5)". The spec already implements this protocol for the
  *clarity* judge (§3.5: `agreement_with_human_majority_min: 0.80`, `position_bias_check`)
  but the export-gating contradiction judge (§3.4) gets none of it.
- **The new insight (beyond G1):** it's not just "add calibration" — it's that the spec
  *calibrates the wrong judge*. The advisory judge is calibrated; the gating judge is the
  uncalibrated one. At the small n the spec uses, 5/6 vs 4/6 flips pass/fail — calibration
  at n=6 is an anecdote, not a calibration.
- **Fix:** Copy the §3.5 calibration recipe onto the contradiction judge: hand-label ~20
  (claim, gold-fact) pairs, run swapped-order + paraphrase stability, require ≥0.80–0.85
  before it may gate. If you can't hit that n, make the HARD gate the *deterministic* checks
  (valid fact ID, forbidden-claim string match, required-beat coverage) and demote the LLM
  contradiction judge to advisory — the exact pattern the spec already uses for clarity. Add
  `contradiction_judge_calibrated` to `export_requires`.

### 2. Write `threat_model.md` + add source-text prompt-injection defense — BLOCKER
- **Lenses:** S2 (blocker), C7 (concern). **New vs grill:** NEW (no grill item covered
  injection or the missing threat-model artifact).
- **Course basis:** 01 Red Team (poisoned context / indirect prompt injection), Invisible
  Payloads (zero-width / homoglyphs); 05 §7 Context Hygiene (the 50-hallucinated-emails
  incident: "AI fills gaps with whatever strings exist in its context"). The spec lists
  `threat_model.md` as a Day-1 DoD (§10) AND a file-tree entry (§2.3) but never specifies
  its contents.
- **Why blocker:** (a) `threat_model.md` is a stated deliverable with no content = a literal
  submission gap; (b) `source.zh.txt` is fed verbatim to BuilderAgent AND the contradiction
  judge (§3.4/§5.2 `get_source` returns raw `source_text`), and the planted-drift demo
  itself injects an attacker-controlled caption (§6.2) that flows into the judge prompt — so
  an injection in a caption could subvert the very gate the demo rests on.
- **Fix:** (1) Actually write `threat_model.md` (name "indirect prompt injection via source
  text" and "judge-prompt injection via generated content" as threats + mitigations). (2)
  Strip/normalize zero-width + homoglyph chars at ingestion. (3) Wrap source + generated
  content in delimited data fences with a system instruction treating fenced text as
  untrusted data. An "injection-resistance" demo beat is a genuine differentiator for a
  security-themed capstone — turn the gap into a points-winner.

### 3. Re-sequence: deterministic-Python core FIRST, harness wrapped around it — BLOCKER
- **Lenses:** D1, D3, D7, D9 (delivery) + A7 (architecture) + G4 (grill). **New vs grill:**
  EXTENDS G4 — the grill flagged "eval sequenced last"; the lenses add (a) zero
  environment bring-up time (D1), (b) cuts become destructive refactors when infra is
  wired first (D7), (c) zero buffer days (D9).
- **Course basis:** 04 "start simple, scale on boundaries" + walking-skeleton; 04 "Agent =
  Model + Harness; most agent failures are configuration failures" (harness/env bring-up IS
  the work, not a free precondition); METR 19%-slower-with-AI stat. The spec's OWN §4.2 ranks
  faithfulness P0 and ADK/MCP P1, and its OWN risk register prescribes "keep tools pure
  Python first, wrap in MCP after tests pass" — but the day-plan contradicts both.
- **Fix:** Days 2–5 build the pure-Python vertical (source → canon_gold → adaptation via
  direct Gemini call → deterministic faithfulness + drift + approval gate, runnable by CLI).
  Then Days 6–9 wrap MCP / ADK-critic / skills / trace one layer at a time over a green,
  already-impressive core. Add an explicit **Day 0.5 harness hello-world** (ADK installed,
  ADC auth, one Gemini completion, one MCP stdio round-trip) BEFORE feature work, and
  designate Days 13 + 17 as buffer. This makes every cut-list cut a no-op (don't run the
  wrapper) instead of a refactor (D7), and gives a slip on non-cuttable Day-9 work somewhere
  to go (D9).

### 4. Fix the eval's statistical foundation (the wow must survive a DS judge) — BLOCKER
- **Lenses:** E1, E2, E3, E9 (+ E5/E6 narrower). **New vs grill:** mostly NEW (grill G1–G3
  hit judge-softness, rigged baseline, non-discriminating recall; these add denominator,
  construct validity, contamination, and clarity-confound).
- **Course basis:** 01 "golden regression set" + discriminative thresholds; 01 dimension 1
  "Intent Satisfaction is the hardest, most important"; 10 "set the bar at the eval, not the
  demo"; CLAUDE.md eval-calibration baseline rule (presumes a denominator big enough to
  estimate a rate).
- **Four sub-fixes:**
  - **E1 (denominator/quanta, overstated→real):** state `total_generated_claims` per run;
    aggregate claims across all 3–5 gold scenes (~40–60 claims) before computing a rate so
    it's stable to ±1 claim; report precision as a fraction with denominator (11/12), not a
    rounded float; make the HEADLINE hard gate the count metric `unsupported_critical_claims
    == 0` (which the spec already has — §3.4) and keep precision descriptive. *(Verifier
    note: "mathematically un-hittable" was overstated — 10/11 rounds above 0.90 — and the
    count gate already exists; the denominator/quanta problem is the real, retained core.)*
  - **E2 (construct validity):** `why_it_matters` + `modern_analogy` (the cross-cultural
    ADAPTATION value) are un-gated; the eval rigorously measures the EASY half (plot-beat
    citation) and markets it as covering the whole product. Either narrow the product claim
    to "source-grounded plot fidelity" OR add a small gold rubric (2–3 acceptable framings +
    2–3 distortions) for the interpretive fields. *(Verifier: cultural_decoder key-terms ARE
    partially gated via source_fact_ids — the gap is the interpretive fields, not the whole
    decoder.)*
  - **E3 (contaminated gold):** builder writes the canon, the prompts, AND validates — zero
    independent ground truth on an obscure text. Get ONE independent check on the demo-scene
    gold (Chinese-literate friend / classical-Chinese teacher / cross-check plot beats — not
    prose — against a published scholarly summary), use a DIFFERENT model family as Pass-3
    critic than the generator, and disclose single-annotator gold as a known limitation.
  - **E9 (clarity confound):** Pair A (full Guwen output: story card + decoder + analogy +
    storyboard) vs Pair B (baseline: translate + explain + panels) differ on
    FORMAT/RICHNESS, not the source-grounding mechanism. Either give the baseline the SAME
    template (differ only on grounding) OR scope the clarity claim to "the full format is
    clearer than a plain translation" (honest format claim) and keep faithfulness as the
    mechanism evidence.

---

## PER-LENS CONFIRMED FINDINGS (de-duped)

### Lens 1 — Evaluation rigor & measurement validity
- **E1** (BLOCKER, overstated→retained): denominator/quanta problem on faithfulness gate;
  count-gate already exists. → must-fix #4.
- **E2** (BLOCKER): construct-validity gap — gates plot-citation, markets it as cultural
  adaptation. → #4. *NEW vs grill.*
- **E3** (BLOCKER): contaminated/self-labeled gold, no independent check on the hard part. →
  #4. *NEW.*
- **E4** (CONCERN): contradiction judge uncalibrated while clarity judge is — the asymmetry.
  → #1. (Verifier: this is the same gap as S3/C1.)
- **E5** (CONCERN): 30–40% baseline-fail band is trivially satisfied by the scaffolding
  artifact (baseline can't emit fact-IDs → auto-fails for the wrong reason); 40–50% gap in
  escape-hatch logic. Compute baseline fail on the FAIR metric (prose-vs-source entailment),
  pre-register "substantive failure," report the failure-mode breakdown instead of the band.
  (Compounds grill G2.)
- **E6** (CONCERN, overstated→narrowed): extraction reproducibility — storyboard panels
  already carry structured `source_fact_ids` (read-not-infer), so the gap is narrower: panel
  claim *granularity* is unspecified and no reproducibility spot-check exists. Fix granularity
  (one claim per panel caption + one per decoder key-term) + spot-check 10 extractions.
- **E7** (CONCERN): "trajectory_gate" is a fixed-order workflow assertion mislabeled as a
  trajectory eval — it can't catch redundant loops / wrong-tool / DoW / self-repair-vs-mask.
  Rename it "workflow integrity test" + add a real cheap trajectory metric on the regen loop
  (iterations_to_converge, did corrected panel re-cite the right fact, loop token cost). *NEW.*
- **E8** (CONCERN): no session-convergence / cost-to-converge metric despite the product
  BEING an iterative regen loop and the course naming this "the single most informative eval"
  (01 Tip 3, with sample code). Log `regenerate_rounds`, `converged`, `cost_to_converge`. *NEW.*
- **E9** (BLOCKER): clarity comparison confounds richness vs mechanism. → #4. *NEW.*
- **E10** (NIT): `clarity_pairwise_preference_rate` (a corpus-level calibration stat) leaks
  into the per-run `trust_gate.metrics`; move it to a corpus-level summary. *NEW.*

### Lens 2 — Agent architecture & engineering
- **A1** (CONCERN, overstated→down from blocker): `get_source` returns full `source_text`,
  `record_trace` + `validate_artifact_schema` are model-visible thin wrappers. (Verifier:
  `write_artifact` already returns {path, sha256}; `check_source_policy`/`run_eval_suite` are
  already high-level — so it's "3 plumbing + 4 real," not "7 wrappers.") Make `get_source`
  return {id, char_count, uri}; demote record_trace/validate to plain Python.
- **A2** (CONCERN, overstated→down from blocker): CriticAgent mixes deterministic checks with
  the one LLM-only job. Move deterministic checks (schema, precision/recall arithmetic,
  trajectory order, forbidden-claim string match) to `PolicyGate.py`; let CriticAgent do only
  the semantic contradiction check → genuine heterogeneous-model adversarial split (Flash
  builds, Pro critiques), which 02 §5 names a VALID multi-agent boundary.
- **A3** (CONCERN): 5 flat SKILL.md files, no progressive-disclosure wiring, no
  scripts/references/assets subdirs. Register via ADK `SkillToolset` so disclosure is real +
  trace-visible; add a `references/` entry per skill; write 3 pos + 3 neg triggers; drop to 3
  skills if 5 can't clear trigger tests.
- **A4** (CONCERN): inter-agent state handoff mechanism is unspecified (default = re-feed YAML
  into next prompt = context-as-database anti-pattern, 02 §10). Specify a file-reference
  contract: Builder writes `runs/<id>/*.yaml`, emits paths; orchestrator passes paths via ADK
  session state; Critic reads from disk; LLM-judge gets only the claim+gold-fact pair. Add
  `test_handoff_passes_paths_not_blobs`. (Highest-ROI de-risk for a weak debugger.)
- **A5** (CONCERN): no retry/regenerate contract (max retries, what context the regen gets,
  persistent-failure behavior) — yet the demo climax depends on it. Specify max_retries=2,
  route {failing_claim, gold_fact, eval_reason} (not the whole artifact) back; on persistent
  failure export stays BLOCKED (a GOOD demo outcome — "the gate held"). Add
  `test_regenerate_loop_blocks_then_passes`.
- **A6** (CONCERN): trace is emitted via a model-visible `record_trace` MCP tool the LLM must
  remember to call → missing events when it forgets. Emit trace deterministically from the
  orchestrator after each step; use ADK native tracing if a one-flag enable exists; call it
  "OpenTelemetry-style trace" in the writeup. (Verifier: "10 OpenTelemetry" cite is from the
  synthesis doc, not a primary paper; 04 §6 observability is the primary anchor.)
- **A7** (CONCERN): plan stacks 3 integration boundaries before any working vertical slice. →
  folded into must-fix #3.
- **A8** (NIT): `render_run_canvas` (and arguably `run_eval_suite`) behind MCP for zero
  interop benefit — pad the tool count. Report 3–4 well-justified MCP tools, not 7.

### Lens 3 — Product value & wedge
- **P1** (BLOCKER): the demo spends 2:00–5:00 on faithfulness plumbing and only flashes field
  NAMES at 1:00–2:00 — the judge never SEES a rendered story card / cultural decoder, i.e.
  never experiences what a learner reads. Re-budget: open 0:30–1:30 with the rendered
  run_canvas (story card + decoder + 2–3 panels read aloud) — value proof BEFORE trust proof.
  *(Verifier: course_basis partly misapplies Eval Tip 2, which is about screenshot-eval of web
  UIs; the rubric "wow factor" basis is independently sufficient.)*
- **P2** (BLOCKER): the "source-grounded" wedge protects the EVALUATOR, not the learner — a
  learner who can't read Chinese can't perceive faithfulness, so the agentic apparatus is
  invisible overhead vs a one-shot ChatGPT prompt (and the spec's own ≥30% baseline-pass means
  the naive baseline passes most of the time). Re-anchor primary user to the EDUCATOR
  (accountable for accuracy, can perceive fidelity) → wedge becomes "classroom-trustworthy,
  can't-get-fired-for-a-hallucination." This also rescues P3. *(Verifier: the New-SDLC "80%
  problem" cite is a loose analogy; rubric basis is the valid anchor.)*
- **P3** (CONCERN): educators are named co-primary (§1.2) but have zero artifact/workflow/demo
  beat — cutting the word "educators" changes nothing in the build. Add a near-zero-cost
  `teaching_pack` block (3 discussion Qs + 1 "gold says vs common misreading") OR delete
  "educators" and own learner-only.
- **P4** (CONCERN): "reusable engine for any source culture" (§1.4) is asserted but every V1
  component is single-culture hand-built (Chinese gold/forbidden_claims/name maps). State
  explicitly that ENGINE = {schema + source-guard + faithfulness-gate + HITL} and only
  canon_gold is culture-specific; optionally run the harness once on a non-Chinese
  public-domain micro-scene (Aesop fable, 5-fact gold) to convert asserted → demonstrated.
- **P5** (CONCERN): the demo's emotional peak is a BLOCKED-export banner — compliance/QA wow,
  cold for an Agents-for-Good arts/literature project. Two-beat climax: (1) recognition beat
  (decoder turns 割席 into a felt modern analogy), THEN (2) trust beat (watch it block a
  planted lie). Head + heart, in that order.
- **P6** (CONCERN, overstated on novelty → = grill G7): low-recognition Guan Ning demo hides
  the value from a cold judge who never knew the story. *Verifier: this is G7 with new
  "value-lens" language but the SAME fix (keep Guan Ning for gold, use an iconic scene for the
  video). Not new beyond grill — counted as a re-confirm of G7, not a new finding.*
- **P7** (NIT): "Remixable" subtitle + the name "Reactor" leak the abandoned reaction-video
  pivot (in `Guwen_Reactor_Session_Record.md`); the spec's §6.2 demo title already says
  "faithful." Fix the Session Record subtitle so the writeup/submission doesn't inherit the
  incoherence.

### Lens 4 — Security, safety & copyright
- **S1** (CONCERN, overstated→down from blocker): output-side copyright claim. `approval_diff.md`
  says "No copyrighted English translation used" — a claim the system can't prove (it only knows
  none was *ingested*). Minimum fix = reword to "No existing English translation was provided to
  the generator." (n-gram/LCS overlap guard is optional for a 45-word public-domain text.)
  *(Verifier: the 05 Zero-Trust quote was repurposed — it's about prompt injection, not
  copyright.)*
- **S2** (BLOCKER): source-text indirect prompt injection absent from threat model;
  `threat_model.md` unspecified. → must-fix #2.
- **S3** (CONCERN): gating contradiction judge uncalibrated vs calibrated advisory clarity
  judge. → #1 (same as E4/C1).
- **S4** (CONCERN): HITL approval is a single "Approve" button + self-authored "all-clear"
  banner = confirmation-fatigue / rubber-stamp pattern the course names (01 Vibe Diff). The
  spec already says "V1 uses plain-English approval diff" (§2.2) but §6.2 shows a banner. Make
  `approval_diff.md` list each exported claim + its cited fact ID; frame as "plain-text Vibe
  Diff (MFA deferred to V2)."
- **S5** (CONCERN): `safety_pass` is a required export gate (§3.8) with NO defined evaluator /
  threshold / implementation — undefined required gate = theater or undefined behavior.
  Implement the course two-layer pattern at min scale: structural deny-list + one semantic LLM
  call ("does this ADD violence/sexual content NOT in the source?"); document false-positive
  handling (faithful-to-source classical violence passes).
- **S6** (CONCERN): AIGC label is a plain YAML field with no integrity binding and isn't
  embedded in the human-facing artifacts. `write_artifact` already returns sha256 — use it:
  embed the label in story-card footer / storyboard header / run_canvas.html + a manifest
  binding {artifact → sha256 → label}. Frame as "risk-stratified attestation (lite)."
- **S7** (CONCERN): regen loop has no max-attempts / token ceiling / iteration logging =
  Denial-of-Wallet exposure the course names first-class. Add a hard cap (3 → fail closed to
  human), log attempts + cost-to-converge in the trace. (Same root as E8/C10 — one fix serves
  DoW defense + trajectory eval + session-convergence.) *NEW (DoW angle).*
- **S8** (NIT): no version pinning in requirements.txt = slopsquatting checklist item. Pin
  exact versions + one threat_model.md line. *(= adjacent to grill, counted nit.)*
- **S9** (NIT): `write_artifact`/`render_run_canvas` have no path-confinement spec (no `..`
  rejection) — relevant given S2 source-injection could attempt out-of-tree writes. Confine to
  `runs/<validated_run_id>/`, reject path separators.

### Lens 5 — Solo 17-day delivery feasibility
- **D1** (BLOCKER): zero ADK/Gemini/MCP environment bring-up time; Day 4 assumes a working
  install. → #3 (add Day 0.5 hello-world).
- **D2** (BLOCKER): Days 15–17 = 3 days for the writeup+video tail; 2,500-word writeup first
  authored on submission day. Make `docs/capstone_writeup.md` a living doc from Day 1,
  pre-record demo segments as features land, Day 17 = pure submission/buffer.
  *(Verifier: tail is ~20 pts (writeup 10 + video 10) — README is in the 70% bucket — but the
  risk stands.)*
- **D3** (BLOCKER): cut-list and day-plan disagree on the true minimum; infra built before the
  non-cuttable value core. → #3.
- **D4** (CONCERN): judge calibration (position-bias, ≥0.80 agreement) is folded invisibly into
  Days 9/11 with no recovery day. Schedule an explicit half-day "judge calibration" task with a
  defined exit (≥0.80 or downgrade to report-only + disclosure). Pre-write the position-bias
  harness.
- **D5** (CONCERN): human clarity raters (Day 11) are an async external dependency with no
  recruitment task scheduled. Make "recruit raters + send pre-written label sheet" a Day-1/2
  task; set a collection WINDOW (Days 8–12); plan to 2 raters, 3 as upside, advisory-mode as
  clean fallback. (= grill G6, schedule angle.)
- **D6** (CONCERN): Streamlit deploy (optional per rubric) eats 3 of the last 5 build days.
  Demote live deploy to opt-in; make static run_canvas.html + public GitHub repo the PRIMARY
  judged link; build cached path Day 7. *(Verifier: Day-12 static canvas IS non-optional; only
  Day-14 live deploy is optional — don't conflate.)*
- **D7** (CONCERN): cutting MCP/ADK late is a destructive refactor, not a clean cut, for a weak
  debugger with no test net. → #3 (wrap-around design makes cuts no-ops).
- **D8** (CONCERN): 5 SKILL.md files in one day, DoD measures file EXISTENCE not invocation.
  Redefine Day-6 DoD as "trace.jsonl shows ≥1 skill loaded on task-match during the E2E run";
  cut to 3 well-wired skills if pressed. (= A3 from the delivery angle.)
- **D9** (BLOCKER): zero buffer/slip days; a 2-day spiral on non-cuttable Day-9 has nowhere to
  go. → #3 (Days 13 + 17 as buffer + a 1.5×-budget circuit-breaker rule).
- **D10** (NIT): cached-demo fallback first built Day 14 → untested at video (Day 16) /
  submission (Day 17). Build the cached loader Day 7 (snapshot a known-good run + `--cached`
  flag); use `--cached` for ALL demos + the video. (= grill G9, reliability angle.)

### Lens 6 — Kaggle capstone rubric & scoring
- **R1** (BLOCKER): the 5-min video covers only 2 of the rubric's 5 named beats; "Why agents /
  what's unique" gets ZERO time, "The Build" gets 20s. Re-cut to hit all five (Problem /
  Why-agents-unique / Architecture / Demo / The Build). *NEW.*
- **R2** (CONCERN, overstated→down from blocker): "clever toolset use" — 5 of 7 MCP tools are
  thin wrappers (real ding), but `get_source`+`check_source_policy` are domain-meaningful, and
  the Agents-CLI claim is overstated: the rubric scores the *Agent-skills concept* (provable via
  .agent/skills SKILL.md, which the rubric accepts), not the google-agents-cli tool specifically.
  Add ≥1 genuinely high-level tool (or reframe the eval tool as a goal tool).
- **R3** (CONCERN): the 10-pt Writeup has no plan/word-budget/journey narrative in the spec.
  Add a writeup outline with a word budget; the C1–C10 pivot record IS the "project journey"
  sub-criterion — connect them. *NEW.*
- **R4** (CONCERN): Antigravity (a hard-gate concept, provable in Video at zero code cost) is
  declined. Build inside Antigravity + 20–30s in "The Build" beat → 6th concept + fills R1's
  empty beat. *(Verifier: gate is already safe at 5 concepts — real value is the video beat +
  6th concept, not gate insurance.)* (= grill G8, with R1 synergy.)
- **R5** (CONCERN): cover image is REQUIRED but treated as a side asset with no quality bar /
  creation milestone. Promote to a tracked Day-17 gating item (reuse the architecture /
  eval-climax diagram as source). *NEW.*
- **R6** (CONCERN): "central agent use" (10 pts) is undermined by cut-list item 8 (cut the
  two-agent split without breaking the product) + mostly-deterministic real work. Give CriticAgent
  a real decision loop (read eval_report → reason which panels failed & why → targeted regenerate
  → re-evaluate); narrate the check-and-balance as the innovation. (= A2/C12 from rubric angle.)
- **R7** (CONCERN): public project link defaults to a live Streamlit/HF Space (live key + rate
  limits during judging). Invert: cached/static run_canvas = PRIMARY link, live = optional bonus;
  verify logged-out, no-key on Day 14 + Day 17. *(Verifier: a broken live link + working public
  repo still satisfies the rubric fallback — risk is impression, not invalidity.)* (= grill G9.)
- **R8** (NIT, but 20 pts): Documentation Day-15 milestone is one line with no element checklist.
  Mirror the rubric verbatim (problem / solution / architecture-with-diagram / verified
  copy-paste setup / results table / no keys). *NEW.*

### Lens 7 — Course-material alignment
- **C1** (BLOCKER): gating contradiction judge has no pairwise/calibration spec while the
  clarity judge does. → #1 (same as E4/S3).
- **C2** (CONCERN, overstated→down from blocker): thin-wrapper MCP tools (write_artifact /
  record_trace / validate_artifact_schema). Collapse to in-process Python; keep get_source /
  check_source_policy / run_eval_suite / render_run_canvas as the MCP surface. (= A1.)
- **C3** (CONCERN): MCP tools pass raw full-text through context (get_source full source_text;
  write_artifact full yaml_text) vs URIs/pointers (02 §10 "Decouple State"). Return
  {id, char_count, snippet}/path; pass run_id + paths between agents. (= A4.)
- **C4** (CONCERN): zero BDD/Gherkin behavior specs despite a specs/ folder — SDD paper makes
  Gherkin the centerpiece and graders "likely reward a BDD spec that genuinely drives behavior."
  Add `specs/behavior.feature` (clean run exports / planted drift blocks / regen then passes /
  missing-license blocks / no-approval blocks) and wire the trajectory + policy tests to it. *NEW.*
- **C5** (CONCERN): PolicyGate is purely STRUCTURAL; the course policy server is TWO layers
  (structural + semantic LLM referee), and the safety checks are inherently semantic but
  unenforced. Add a semantic gate reusing the judge model. (= S5.) *NEW.*
- **C6** (CONCERN): 5 skills ship with NO skill-level eval (trigger accuracy, pos/neg triggers,
  pass^k) — course: "a skill without a test is a hope"; SkillsBench 19% perform WORSE than no
  skill. Add `evals/test_skills.py` (3 pos + 3 neg per skill + one execution golden for the 2
  riskiest); report trigger accuracy; frame as EDD. (= A3/D8.) *NEW.*
- **C7** (CONCERN): no context-hygiene/prompt-sanitization layer (the 50-email incident). →
  #2 (same root as S2). *NEW.*
- **C8** (CONCERN): Antigravity dismissed but is a free concept demonstrable in Video. (= R4/G8.)
- **C9** (CONCERN): bespoke trajectory checking ignores the course's named primitives —
  OpenTelemetry span taxonomy (agent.session/think/tool) AND ADK's built-in eval trajectory
  modes (EXACT/IN_ORDER/ANY_ORDER). Name events with OTel span types; use IN_ORDER (export is an
  action-allowed sequence) or map the custom check to IN_ORDER semantics in docs. *NEW.*
- **C10** (CONCERN): regen loop has no budget cap / DoW defense. (= S7/E8.) *NEW (DoW).*
- **C11** (CONCERN): single-run output eval ignores session-convergence (Tip 3) + mining user
  corrections as labeled failure data (Tip 4); the regen loop IS a convergence/correction event.
  Record {regenerations_to_pass, cost_to_converge, blocked_then_recovered}; frame planted-drift
  block→regen as a labeled-correction convergence demo. (= E8.) *NEW.*
- **C12** (NIT): the Builder/Critic split is correct but unanchored to the course's boundary
  criterion → vulnerable to a "redundant stacked agents" read. Add one sentence: "Builder/Critic
  are split because the evaluator must be a separate trust boundary that cannot edit what it
  grades." (= A2/R6 framing.) *NEW.*

---

## COURSE-ALIGNMENT GAPS (course-taught/rewarded things the spec VIOLATES or MISSES)

1. **LLM-as-judge calibration applied to the wrong judge.** Course (02 §6): swap-position +
   calibrate-to-human is non-negotiable for ALL judge usage. Spec calibrates the advisory
   clarity judge and leaves the EXPORT-GATING faithfulness judge uncalibrated. (E4/S3/C1.)
2. **No pairwise framing on the gating judge.** Course rewards pairwise/entailment over absolute
   classification; the contradiction judge is a single-output binary classifier. (C1.)
3. **Session-convergence eval missing** — the course's named "single most informative eval"
   (Tip 3) with sample code, ignored despite the product being an iterative loop. (E8/C11.)
4. **User-corrections-as-labeled-failure-data (Tip 4) missing** — the regen loop generates this
   for free and the spec discards it. (C11.)
5. **Trajectory eval is a workflow assertion, not a trajectory eval** — violates the CONCEPT
   (tolerate ordering variance, detect loops/self-repair/DoW) while using the WORD. Also ignores
   OTel span taxonomy + ADK's built-in trajectory modes. (E7/A6/C9.)
6. **No BDD/Gherkin behavior spec** despite SDD being a course pillar + "graders likely reward a
   BDD spec that drives behavior." (C4.)
7. **One-layer policy server** — course policy server is structural + semantic; safety checks are
   semantic but unenforced. (S5/C5.)
8. **No skill-level evaluation** — "a skill without a test is a hope"; SkillsBench 19%
   worse-than-no-skill; DoD measures file existence not invocation/trigger accuracy. (C6/D8/A3.)
9. **No Denial-of-Wallet defense** on an LLM-in-a-loop — a named first-class agentic threat. (S7/C10.)
10. **No source-text sanitization / indirect-injection defense** — the course's flagship
    cautionary tale (50 hallucinated emails / poisoned context). (S2/C7.)
11. **Context-as-database / full-text-through-context** instead of URIs/pointers (02 §10 Decouple
    State). (C3/A4.)
12. **Thin-wrapper tools** instead of high-level-goal tools (10 anti-pattern). (C2/A1/R2.)
13. **"Start simple, scale on boundaries" violated by sequencing** — 3 integration boundaries
    stacked before a working slice; spec's own P0/P1 + risk register contradicted. (A7/D1/D3.)
14. **Antigravity (a hard-gate concept) declined** despite zero-cost video demonstrability. (R4/C8/G8.)
15. **Video misses 3 of 5 rubric-named beats** (Why-agents-unique, Architecture, The Build). (R1.)

---

## NEW FINDINGS BEYOND THE PRIOR GRILL (G1–G9)

Genuinely new (the grill did not cover these):
- **The calibration ASYMMETRY** — grill G1 said "calibrate the contradiction judge"; the new
  insight is the spec calibrates the *advisory* judge and leaves the *gating* one uncalibrated
  (E4/S3/C1).
- **Construct validity** — eval gates plot-citation, markets it as cultural adaptation; the
  interpretive fields (`why_it_matters`, `modern_analogy`) are un-gated (E2).
- **Contaminated/self-labeled gold with no independent check on the hard part** (E3).
- **Clarity comparison confound** — Pair A vs B differ on richness, not the mechanism (E9).
- **Per-run vs corpus-level metric category error** in trust_gate (E10).
- **Indirect prompt injection from source text + unspecified `threat_model.md`** (S2/C7).
- **`safety_pass` is a required gate with no evaluator** + one-layer policy server (S5/C5).
- **AIGC label has no integrity binding / isn't embedded in artifacts** (S6).
- **Denial-of-Wallet on the regen loop** (S7/C10).
- **Session-convergence + correction-mining evals missing** (E8/C11).
- **Trajectory "eval" is a workflow test; OTel + ADK trajectory primitives ignored** (E7/A6/C9).
- **No BDD/Gherkin spec** despite SDD pillar (C4).
- **No skill-level eval** despite the skills-as-hard-gate claim (C6).
- **Inter-agent state-handoff mechanism + retry/regenerate contract unspecified** (A4/A5).
- **Context-as-database (full-text through context)** (C3).
- **No environment bring-up time; cuts become destructive refactors; zero buffer days** (D1/D7/D9).
- **Video misses 3 of 5 rubric beats; writeup/cover-image/README have no plan or quality bar**
  (R1/R3/R5/R8).
- **Demo never shows the rendered artifact (value proof); BLOCKED-banner is a cold climax;
  wedge protects evaluator not learner; educators are decorative** (P1/P5/P2/P3).

Re-confirms of the grill (NOT new — counted as confirmations):
- G7 (low-recognition demo source) ≈ P6. G6 (rater dependency) ≈ D5. G8 (Antigravity) ≈ R4/C8.
- G9 (cached link primary) ≈ R7/D10. G2 (rigged baseline) compounded by E5. G4 (eval sequenced
  last) extended by D1/D3/D7/D9. G1 (judge calibration) extended by the asymmetry (E4/S3/C1).

---

## STRONGEST PARTS (no change needed)

- **Copyright solution** — ingest original Chinese only, generate own English. Clean and
  defensible; output-side claim wording is the only tweak (S1).
- **Planted-drift demo climax** — block → regenerate → pass → approve → export is a genuinely
  good 5-min proof spine (just needs a recognition beat first, P1/P5, and a non-forbidden drift
  to prove generality, G1).
- **Cut-list discipline + hard-no-cut floor** (source guard, canon, faithfulness, drift,
  approval) — the right instinct; just needs the wrap-around sequencing so cuts are no-ops (D7).
- **Concept coverage at 5 of 6** with ≥3 hard-gate satisfied comfortably (Antigravity is the
  free 6th).
- **`unsupported_critical_claims == 0` count gate already exists** alongside precision — the
  landable hard gate E1's fix asks for is already half-built.
- **`write_artifact` already returns sha256** — the integrity primitive S6 needs is already there.
- **The clarity judge's calibration protocol is fully specified** — it's the exact recipe to copy
  onto the gating judge (#1).
- **The spec's own §4.2 (P0/P1) + risk register already prescribe the right sequencing** — the
  fix is to make the day-plan obey the spec it already wrote.
- **Honest C1–C10 revision history** — doubles as the writeup's "project journey" sub-criterion
  (R3) for free.
