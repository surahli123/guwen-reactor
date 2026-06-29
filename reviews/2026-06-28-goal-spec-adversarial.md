# Adversarial Review — `docs/plan/session-goal-spec.md` (FINAL)

`VERIFIED_AGAINST: feat/phase-0-scaffold @ bd54fd8 @ 2026-06-28 (PT)`

**Verdict:** **execute-with-edits** — spec is fundamentally sound; **0 surviving BLOCKERs**, 4 CONCERNs
+ 2 SUGGESTIONs, all pre-build wording/wiring inconsistencies. Reconcile them BEFORE the autonomous run.

## Method & coverage
5 parallel reviewers — 4 OMC Claude lenses (`critic`, `architect`, opus DS eval-validity, `security-reviewer`)
+ **independent Codex** — 48 raw findings → refute-by-default verification → opus synthesis.
(First run was rate-limited mid-verify; resumed after the 14:10 PT reset — completed: 7 findings survived,
~14 refuted, post-verify ALL 5 raised "BLOCKERs" downgraded to CONCERN/SUGGESTION.)

## OMC vs Codex (why running both paid off)
- **AGREED (highest trust):** `runs/demo_drift` has no durable producer (OMC `plan-correctness-3` + Codex `codex-7`). Fix first.
- **Codex uniquely:** D7 outcome-gating (broken-ruler) + valid-but-wrong-fact-id gate hole — both eval-validity.
- **OMC uniquely:** export-gate stage confusion + workflow_integrity event-name mismatch + D5 evidence gap — structural seams.
- Net: the families **partition** the spec (healthy coverage, no contradiction).

---

## CONCERNS (4 — must reconcile before the run)

### #1 · `runs/demo_drift` has no durable producer — D2 would crash on a clean checkout  ⭐ AGREED by both families
D2 (`session-goal-spec.md:45`) and the Wave-2 e2e proof (`implementation-plan.md:957-959`) consume
`runs/demo_drift` as a pre-existing dir, but nothing materializes it: Wave-0 commits only `runs/demo_clean`;
S6 injects into ephemeral `tmp_path/'drift'` (`impl-plan:899`) yet S6 prose (line 79) claims it "creates
`runs/demo_drift` at test time." `runs/` is empty → standalone D2 hits FileNotFoundError, which is non-zero
but NOT the specified "BLOCKED + `missing[]`" → **D2 as worded is unsatisfiable.** In the non-cuttable spine.
**Fix:** add a durable step — commit `runs/demo_drift` as a fixture OR run `inject runs/demo_clean
runs/demo_drift subtle_motivation_spoof` before D2; fix S6 line-79 prose; DoD asserts the dir exists.

### #2 · Export gate lumps approval+manifest with content → clean runs return BLOCKED at `evaluate_run`
`eval_plan.yaml` `export_gate.bool_gates` includes `human_approved` + `aigc_label_manifest_bound`
(lines 33-39); `policy_gate.py:115-117` flags any non-True bool_gate as missing → BLOCKED. But approval/manifest
are produced LATER at export (4b.4), so a clean-but-unapproved run is BLOCKED — failing S4 (line 74), D4
(line 47), and Task 4a.4's own `!= BLOCKED` assertion (`impl-plan:841,847`). Enum `READY_FOR_APPROVAL` already
implies stage-aware intent; the spec just never says it. **Real risk:** a careless executor deletes the approval
gates from the YAML to green the test → silently weakens export. (OMC-only; downgraded BLOCKER→CONCERN — TDD self-corrects.)
**Fix:** declare the `evaluate_run`-time gate **content-only** (zero_count + coverage + `safety_pass` +
`workflow_integrity_pass` + `source_policy_valid` + `source_sanitized`); `human_approved` + manifest **default-pass**
at eval, enforced only at export. `export_status = READY_FOR_APPROVAL` iff content gates pass. Clarify "No new
gate constants" = no duplicate list, NOT a ban on stage-aware eval. **Do NOT delete the approval bool_gates.**

### #3 · D7 gates the Stop-hook on the OUTCOME landing in [0.30,0.40] — broken-ruler / outcome-tuning hazard  (Codex)
D7 (`session-goal-spec.md:50`) passes only if measured fractions land in band, but `eval_plan.yaml:74-82`
pre-registers an `adjustment_rule` for out-of-band ("never tune after seeing which way the number moved").
The DoD table is the literal `/goal` Stop-hook and is NOT loaded from YAML → D7's wording is operative and
**contradicts the pre-registered methodology** — it stalls the session or incentivizes tuning the harness until
the number complies (the exact failure the owner's eval-calibration rule forbids). Dead zone: pass band
[0.30,0.40] but adjustment only fires <30% / >50% → 0.40–0.50 undefined.
**Fix:** D7 passes on (a) real B1 logged WITH denominator + (b) pre-registered deviation-handling applied if
out-of-band. **Never gate on the outcome being in-band.** Close the 0.40–0.50 dead zone in the YAML rule.

### #4 · Deterministic gate trusts valid-but-WRONG fact citations — gameable + untested  (Codex; corroborates the eval-validity lens)
`evaluate_claims` B.5 (`impl-plan:764-766`) flags UNSUPPORTED only when `source_fact_ids` is **empty**;
`validate_claims` (647-655) only flags ids **absent** from gold. So an action/visual claim citing a **real-but-
irrelevant** id passes everything → `else`→SUPPORTED (770-772) **and its irrelevant id boosts beat coverage.**
The drift suite tests non-existent ids (`citation_spoof`) and empty ids (`unsupported_detail`) but **never
valid-but-wrong-id.** `decisions-locked.md:32` says ids must "cover it" but impl reduced "cover" → "non-empty."
This is the structure-not-meaning gap: the gate proves citation *form*, not citation *relevance*.
**Note:** full semantic entailment is D1-locked as advisory-only — so the fix must be **structural, not semantic.**
**Fix:** (a) tighten the headline claim → "structural source-grounding + valid-id citation; semantic entailment
advisory"; (b) add a **structural beat↔fact-id alignment check** (cited ids must belong to the claim's declared
beat) — deterministic, respects D1; (c) add a **hostile fixture** with a valid-but-wrong id; (d) stop the
irrelevant-id coverage boost; (e) reconcile `decisions-locked.md:32` "cover it" = structural beat-membership.
**Residual (disclose):** within-beat fabrication with a correct-beat id remains advisory-only (semantic).

## SUGGESTIONS (2 — cheap hardening)
- **#5 · D5 "zero network/API calls" asserted, not verified.** Evidence is "manually open the HTML," which can't
  prove absence of CDN/font/fetch refs. **Fix:** grep rendered HTML for external `http(s)`/`src`/CDN/fetch (assert none)
  and/or headless-load with network blocked and assert it renders.
- **#6 · `workflow_integrity` required_events ≠ emitted span names.** `eval_plan.yaml:96-98`
  `[claims_extracted, eval_completed]` vs pipeline spans `[claims_validated, structural_audit, coverage, safety]`
  (`impl-plan:946`). `check_order` is bound to the YAML → a mismatch makes `workflow_integrity_pass=False` on the
  CLEAN run → breaks D1 the first CLI run. **Fix:** reconcile YAML required_events to the actual emitted vocabulary
  + a unit test asserting `emitter vocab == yaml required_events`.

## Lower-priority (noted, not in the action set)
- Homoglyph evasion of the forbidden match (`security-safety-4`): Cyrillic-homoglyph forbidden claim + valid id
  evades B.3 (NFKC doesn't fold confusables); sanitizer detects (`homoglyph_suspected`) but gate doesn't consume it.
  Bounded materiality (needs a deliberate adversary; doesn't affect measured numbers; partly disclosed). Optional
  cheap win: wire `homoglyph_suspected` into a bool gate.

---

## Recommended edits (ordered) & where they land
| # | Edit | Lands in | Touches locked contract? |
|---|---|---|---|
| 1 | demo_drift durable producer + S6 prose + D2 asserts dir | spec §3/§2, `implementation-plan.md` | impl prose only |
| 2 | export gate content-only at eval; approval/manifest default-pass | spec §2/§3 note | clarifies, no change |
| 3 | D7 rewrite (no outcome-gating) + close 0.40–0.50 dead zone | spec §2, `eval_plan.yaml` | **yes — pre-registered rule** |
| 4 | structural beat↔fact-id check + hostile test + reword "cover" | spec, `implementation-plan.md` Contract B, `decisions-locked.md:32` | **yes — adds scope + locked wording** |
| 5 | D5 automated no-network check | spec §2 | no |
| 6 | reconcile workflow_integrity required_events + test | `eval_plan.yaml`, spec | canonical YAML |

**Owner sign-off needed for #4 (scope add + locked-decision wording) and #3 (pre-registered rule).**
Edits #1, #2, #5, #6 are pure reconciliations.

---

## APPLIED — 2026-06-28 (owner approved #4 = add structural check)
All 6 edits landed across `session-goal-spec.md` (§0/§1/§2 D2·D5·D7·D8/§3 S2·S6·S9/§8), `decisions-locked.md`
(Contract B rule 5 → structural beat-membership), `eval_plan.yaml` (adjustment_rule dead-zone closed;
required_events D1-consistent vocabulary), and `implementation-plan.md` (pipeline-order line aligned to the
canonical YAML vocabulary). Homoglyph item deferred as optional hardening. Spec status → APPROVED (execute-with-edits).
Next: Wave 0.
