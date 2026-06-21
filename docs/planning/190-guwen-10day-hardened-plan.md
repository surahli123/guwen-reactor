# Guwen Reactor — Hardened 10-Day Plan (brutal cut)

Written 2026-06-20. The builder may have only ~10 WORKING days end-to-end, not 17. This re-cuts
the deep-reviewed Spec v2 to a 10-day reality. Principle: keep ONLY the non-negotiable core
(eval-wow + one scene + end-to-end + demoable); everything else → writeup-vision. Plan-only.

## What 10 days forces (vs the 17-day plan)
- Eval-wow rests on the **deterministic faithfulness gate**, NOT a calibrated LLM judge.
  Demote the contradiction judge to ADVISORY (B1's cheap path) — no calibration study (costs
  ~1-2 days we don't have). HARD gate = `unsupported_critical_claims==0` + required-beat
  coverage + forbidden-claim match. These are objective and reproducible → still a real wow.
- Narrow the product claim to **"source-grounded plot fidelity"** (B4b) — do NOT build the
  interpretive-field gold rubric. The decoder/analogy ship but are not gated (disclosed).
- **Cut the clarity human study** (or advisory-only). Removes rater recruitment + Day-11 +
  the kappa work. Faithfulness alone carries the eval-wow.
- 3 gold scenes (1 demo + 2 eval), not 5. 3 skills, not 5.

## Non-negotiable core (must ship)
source-guard → canon_memory (gold, 1 independent check on demo scene) → adaptation (story card
+ cultural decoder + text storyboard) → DETERMINISTIC faithfulness gate (count + coverage +
forbidden) → planted-drift block (incl. one NON-forbidden subtle drift) → regenerate (max 2,
DoW cap) → human approval → export (MD/YAML + static HTML canvas). Wrapped in a small MCP
server (LOCKED, ~3 real tools) + 3 skills. trace.jsonl (deterministic, OTel-named). 1-page
threat_model.md + source-text sanitize/data-fence (B2). Public repo + cached static link + 5-min
video. = concepts: MCP + skills + security + evaluation + deployability (5; ADK multi-agent is
upside).

## Cut beyond the 17-day cut-list (→ V2 / writeup-vision)
LLM-judge calibration; clarity human study; interpretive-field gold rubric; 5th/4th gold scene;
4th/5th skill; BDD/Gherkin behavior.feature; skill-level eval suite; non-Chinese micro-scene
demo; live Streamlit deploy; full A2UI; image generation; AgBOM/Vibe-Diff-MFA; reaction-script.
KEEP (cheap + concept-bearing): threat_model + sanitize (B2); DoW cap on regen (1 line, S7);
AIGC integrity binding via existing sha256 (S6); session-convergence log (regen_rounds — 1 line,
E8); Antigravity shown in video (free 6th concept, G8/R4).

## 10 working-day schedule (eval-first; B3)
| Day | Milestone | Definition of done | If it slips |
|---|---|---|---|
| 0.5 | Harness hello-world | ADK installed, ADC auth, 1 Gemini completion, 1 MCP stdio round-trip | fix env BEFORE any feature work |
| 1 | Repo + specs + scene + gold-1 | repo; product_spec + eval_plan + 1-page threat_model committed; demo scene (iconic) + 3 gold scenes chosen; demo-scene canon gold drafted | if env still broken, pure-Python only, MCP later |
| 2 | Canon gold + schemas | 3-scene canon_gold (demo scene independently checked) + pydantic schemas; `pytest test_schema` green | drop to 2 eval scenes |
| 3 | Adaptation (pure Python) | source-guard + sanitize/data-fence; direct-Gemini story card + cultural decoder + text storyboard for the demo scene | decoder/analogy are ungated (disclosed) |
| 4 | **Eval core (the wow)** | deterministic faithfulness gate + planted-drift (1 forbidden + 1 subtle non-forbidden) BLOCKS export; regenerate (max 2, DoW cap); human approval gate; **CLI end-to-end green** | NON-CUTTABLE — buffer Day 10 absorbs slip |
| 5 | Measured numbers + trace | fair baseline (baseline also cites) on ~30-40 aggregated claims; report fractions + count gate headline; trace.jsonl (OTel-named); cached run snapshot + `--cached` flag | clarity stays cut/advisory |
| 6 | Wrap MCP + 3 skills | ~3 real MCP tools over the green core; 3 SKILL.md with triggers; trace shows >=1 skill load on match | MCP LOCKED; skills cut to 2 if needed |
| 7 | ADK split (upside) + canvas | Builder/Critic split with a real critic decision loop IF green, else Critic=Python module (note "conceptual split"); static run_canvas.html renders source→output→eval→trace | ADK split is the cuttable one (concepts already =5) |
| 8 | Video + cover | <=5-min video: recognition beat (decoder) → trust beat (drift blocked→regen→pass→approve→export) → Antigravity 20s → 5 rubric beats; cover image from a diagram | use `--cached` run for the video |
| 9 | Writeup + README + ship | writeup <=2500w (living doc; uses the C1-C10/grill/review journey); README rubric-checklist; repo public; cached static link verified logged-out | freeze code; bugfix only |
| 10 | BUFFER + submit | submit early PT; no risky last-hour changes | absorbs any earlier slip |

Circuit-breaker: if any day's milestone exceeds 1.5x its budget, stop, trigger the cut-list, do
not push into buffer twice.

## Absolute floor (if Days 6+ collapse)
The Day-4 pure-Python CLI core (source→canon→adaptation→deterministic faithfulness→drift-block→
approval→export) + public repo + a video of the CLI. Still demonstrates evaluation + security +
deployability (+ skills if any landed) = >=3 concepts, and the eval-wow is intact. Everything
above Day 4 is upside layered on a shippable core.

## What stays the wow at 10 days
"A reproducible source-fidelity gate that catches a planted hallucination and refuses to export
until a human approves" — objective, demoable in 90 seconds, and exactly the builder's eval edge.
No fragile human study or uncalibrated judge in the critical path.
