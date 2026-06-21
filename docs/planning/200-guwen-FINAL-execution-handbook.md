# Guwen Reactor — FINAL Execution Handbook (single source of truth)

Status: **PLAN-ONLY. Do NOT write code until the owner says "go".** Today 2026-06-20;
deadline 2026-07-06 23:59 PT; assume ~10 working days. Consolidates 00 (rubric), 120
(design), 150 (grill), 170 (deep review), 180 (GPT handoff), 190 (10-day cut). Build from THIS.

## 1. Locked decisions (one screen)
- **Project:** Guwen Reactor — a source-grounded cross-cultural adaptation agent. Track: **Agents for Good**.
- **Primary user:** English-speaking **educators** (accountable for accuracy, can perceive fidelity); learners are the beneficiary. (P2 re-anchor.)
- **Wow:** a **measured, deterministic source-fidelity gate** that catches a planted hallucination and refuses to export until a human approves. Narrowed claim = **"source-grounded plot fidelity"**.
- **Source:** ingest ORIGINAL Chinese only, generate own English (zero IP risk). Eval gold built on small Shishuo Xinyu scenes (incl. 管寧割席); the 5-min **video uses one ICONIC scene** (三顾茅庐 / 大闹天宫 / a 聊斋 tale) for recognition.
- **Positioning (writeup vision, NOT v1 build):** a reusable cross-cultural adaptation ENGINE = {schema + source-guard + faithfulness-gate + HITL}; only canon_gold is culture-specific.
- **Build tooling:** Antigravity (primary agentic IDE + CLI — verify commands vs official docs) + Claude Code + Codex as coding agents building from `specs/`. Meta-narrative: "built via agentic engineering."

## 2. Architecture (v2 + baked surgical fixes)
ADK orchestrator → BuilderAgent (artifacts) + CriticAgent (REAL decision loop: read eval_report → which panels failed & why → targeted regenerate → re-eval; a separate trust boundary that cannot edit what it grades) → deterministic **PolicyGate.py** → **Human approval** → Export bundle.
- **MCP `guwen_mcp` (LOCKED, ~3 real high-level tools):** `get_source` (returns {id, char_count, uri} — NOT raw text), `check_source_policy`, `run_eval_suite`. `render_run_canvas` optional. record_trace/validate → plain Python (not model-visible thin wrappers).
- **Handoff contract (highest-ROI de-risk):** Builder writes `runs/<id>/*.yaml`, emits PATHS; orchestrator passes paths via ADK session state; Critic reads from disk; the judge gets ONLY the {claim, gold-fact} pair (no context-as-database). Test: `test_handoff_passes_paths_not_blobs`.
- **Trace:** emitted deterministically from the orchestrator (not an LLM-called tool); OTel span names (agent.session/think/tool); ADK IN_ORDER trajectory check.
- **Security (cheap, concept-bearing):** `threat_model.md` (names indirect injection via source text + judge-prompt injection); ingestion strips zero-width/homoglyphs + wraps source/generated text in untrusted data-fences; regen **DoW cap** (max 2-3 → fail-closed to human, log cost); `safety_pass` = structural deny-list + ONE semantic LLM call ("adds violence/sexual content NOT in source?"); AIGC label embedded in artifacts + manifest {artifact→sha256→label}; write paths confined to `runs/<id>/`.

## 3. The evaluation harness (the wow) — spec
- **Ground truth = canon_memory gold** (characters/relationships/plot-beats/atomic-facts/forbidden-claims), 3 scenes (1 demo + 2 eval), demo-scene gold **independently checked once** (Chinese-literate person or published scholarly summary; cross-check beats not prose); Pass-3 critic uses a DIFFERENT model family than the generator; single-annotator gold disclosed as a limitation.
- **HARD gate (deterministic):** `unsupported_critical_claims == 0` (headline) + required-beat coverage + forbidden-claim match + valid fact-IDs + schema valid. **LLM contradiction judge = ADVISORY** (no calibration study under 10 days).
- **Metrics (measured, not illustrative):** precision as a fraction with denominator (e.g. 11/12), aggregated across ~30-40 claims over all scenes; recall demoted to a coverage sanity-check (add one omit-a-beat test so it can fail); session-convergence log (regenerate_rounds, converged, cost_to_converge).
- **Planted drift demo:** catch BOTH a forbidden-listed drift AND a subtle non-forbidden one (invented motivation) → proves generality.
- **Baseline (fair):** naive one-shot that is ALSO asked to cite source facts (apples-to-apples), OR judge faithfulness on prose directly; report failure-MODE breakdown + the ~30-40% band; if <30% or >50%, disclose + adjust.

## 4. 10-day schedule (compact; full detail + "if-slips" in 190)
- **D0.5** env hello-world (ADK + ADC auth + 1 Gemini call + 1 MCP stdio round-trip).
- **D1** repo + specs (product_spec, eval_plan, 1-page threat_model, behavior.feature optional) + pick scenes + draft demo-scene gold. Recruit-rater task only if doing clarity (default: skip).
- **D2** 3-scene canon gold (demo independently checked) + pydantic schemas + `pytest test_schema` green.
- **D3** pure-Python adaptation (story card + cultural decoder + text storyboard) via direct Gemini; source-guard + sanitize/data-fence.
- **D4** ⭐ deterministic faithfulness gate + planted drift (forbidden + subtle) blocks export + regenerate (≤2, DoW cap) + human approval; **CLI end-to-end green**. NON-CUTTABLE.
- **D5** fair baseline + measured fractions (count-gate headline) + trace.jsonl (OTel) + cached run snapshot + `--cached`.
- **D6** wrap MCP (~3 tools) + 3 skills (triggers; trace shows skill load) over the green core.
- **D7** ADK Builder/Critic split (real critic loop) IF green, else Critic=Python module (note conceptual split) + static run_canvas.html. **Feature freeze.**
- **D8** record ≤5-min video (5 rubric beats; recognition→trust climax; Antigravity 20s; `--cached` run) + cover image (reuse a diagram).
- **D9** writeup ≤2500w (living doc; uses the C1-C10/grill/review journey) + README (rubric checklist) + repo public + cached static link verified logged-out.
- **D10** BUFFER + submit early. Circuit-breaker: any day >1.5x budget → trigger cut-list, don't double-dip buffer.

## 5. Cut-list (drop in order if behind) & absolute floor
Cut: live Streamlit → slideshow/SRT → 4th/5th scene+skill → ADK two-agent split (Critic→Python) → MCP wrapper (LAST resort). **Never cut:** source guard, canon, deterministic faithfulness, planted-drift, approval gate, public repo + README.
**Absolute floor (Days 6+ collapse):** the D4 pure-Python CLI core + public repo + a CLI video → still hits evaluation + security + deployability (≥3) with the wow intact.

## 6. Concept coverage (need ≥3 → have 5)
MCP server (`guwen_mcp`, code) · Agent skills (`.agent/skills/`, code+video) · Security (gate/sanitize/DoW/HITL, code+video) · **Evaluation** (showpiece, code+video) · Deployability (cached static canvas + repo, video). Upside 6th: Antigravity (video). ADK multi-agent = upside if D7 lands.

## 7. Submission checklist (Kaggle)
- [ ] Kaggle Writeup ≤2,500 words, Track=Agents for Good, title+subtitle (fix "Reactor/Remixable" naming leak).
- [ ] Media gallery + **cover image** (required).
- [ ] YouTube video ≤5 min, public/unlisted, all 5 beats + the eval climax.
- [ ] Public project link = **cached static run_canvas + public GitHub repo** (primary, no key/login); live = optional.
- [ ] README: problem / solution / architecture+diagram / verified copy-paste setup / results table / **NO API keys**.
- [ ] Submit before deadline; no last-hour risky changes.

## 8. Verify BEFORE build (open items)
1. **Antigravity CLI** — confirm actual install/CLI/deploy commands vs official docs (don't hand-write unverified syntax). [I can research this on "go".]
2. Pick the iconic VIDEO scene (三顾茅庐 / 大闹天宫 / 聊斋).
3. Line up ONE independent check for the demo-scene gold.
4. Confirm Gemini/ADK access + ADC auth works (the D0.5 hello-world).

## 9. The GO gate
This is plan-only. On your explicit **"go"**, the build starts at **D0.5 + D1** (env hello-world + repo/specs), eval-first, via Antigravity + Claude Code/Codex from `specs/`. Optional before go: send the updated `180` to GPT for a 10-day Spec v3 and I reconcile it against this handbook.
