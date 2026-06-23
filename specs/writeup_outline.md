# Writeup Outline — Guwen Reactor

Target: ≤ 2,500 words.
Track: Agents for Good.
Living file — fill sections as the build lands.

---

## 1. Title and one-line pitch (~120 words)

**Guwen Reactor: A Source-Grounded Agentic Engine for Classroom-Trustworthy
Cross-Cultural Story Adaptation**

One-line pitch: turns public-domain Classical Chinese scenes into educator-friendly
English story cards, cultural decoders, teaching packs, and storyboards, while
measuring plot fidelity and blocking hallucinated claims before export.

---

## 2. Problem and users (~250 words)

- Primary user: English-speaking educators. Learners are beneficiaries.
- Problem: cross-cultural teaching needs accuracy, context, and trust — not only
  translation.
- Accountable user: the educator, who must stake their classroom reputation on the
  output.
- Why existing tools fall short: no source grounding, no hallucination detection,
  no human approval artifact.

---

## 3. Why agents are necessary (~300 words)

One-shot ChatGPT is insufficient because:
- No source guard (no check that English translation was not ingested)
- No canon gold (no ground-truth fact set anchored to Chinese source chunks)
- No claim-vs-source eval (no structural audit of what was invented)
- No safety gate (no check for added content not in source)
- No approval artifact (no diff the educator signs before export)

The multi-component harness — guard → gold → structured claims → audit →
regen loop → approval → export — is what makes the output trustworthy, not the model.

---

## 4. Architecture (~350 words)

- Pure-Python core first (eval-first walking skeleton)
- Local stdio MCP server (`guwen_mcp`, 4 tools)
- Agent skills folder (3–5 skills, trigger-tested)
- Optional ADK BuilderAgent + CriticAgent (separate trust boundary: Critic cannot
  edit what it grades)
- Cached static HTML run canvas as primary judged link (no API key required)
- File-reference handoff contract: paths + SHA-256, never full blobs

Architecture diagram path: `docs/architecture.md`

---

## 5. Evaluation harness (~550 words — centerpiece)

Locked decisions shape every claim here (D1 structural audit, D3 plot-only hard gate).

- **Structured claims (D1=A):** generator emits `{beat_id, claim_text,
  source_fact_ids, assertion_type, hedging, artifact_path}`. Gate audits structure,
  not keyword heuristics.
- **Hard gate (plot only, D3=C):** `unsupported_critical_claims == 0`,
  `contradicted_claims == 0`, `unsupported_motivation_claims == 0`, coverage ≥ 0.85.
- **Interpretive layer (advisory only):** `why_it_matters` and `modern_analogy`
  scored against `interpretive_rubric.yaml`; reported in `eval_report.interpretive_advisory`;
  never in `export_requires`.
- **Precision with denominator:**
  > ILLUSTRATIVE — replace with measured run output: 42/45 supported factual claims
- **Drift suite (D1–D6):** obvious contradiction, non-forbidden unsupported detail,
  subtle invented motive, coverage omission, citation spoof, judge-prompt injection.
- **Specificity test (Contract G):** valid hedged interpretation on a clean run must
  NOT block export — proves the gate does not over-block.
- **Baseline B1:** same-template source-citing baseline scored by same `evaluate_run`;
  expected fail band 30–40% (pre-registered, decided before seeing results).
- **LLM contradiction judge:** advisory only (no calibration study possible under 10
  days); structural audit is the hard gate.
- **`evaluate_run` defined first (Contract E):** drift suite and CLI import it;
  no forward dependency.

---

## 6. Security (~250 words)

- Source-text injection: NFKC + zero-width strip before ingestion.
- Generated-content injection (fix F5 / Contract H): `sanitize(claim_text)` applied
  to generated output BEFORE `build_judge_prompt`.
- Fenced judge prompt: `<UNTRUSTED_CLAIM>` / `<UNTRUSTED_GOLD_FACT>` blocks.
- `PROMPT_INJECTION_ATTEMPT` detector: phrase deny-list, first gate step, blocks export.
- Path confinement: writes only to `runs/<validated_run_id>/` and `docs/demo/`.
- Denial-of-Wallet: max 3 total attempts; fail-closed to human; cost logged.
- AIGC manifest binding: SHA-256 + label presence checked on every artifact.

---

## 7. Demo (~250 words)

Two-beat video:
- Recognition beat (三顧茅廬 preview) — format illustration, not the measured scene.
- Trust beat (管寧割席) — the measured proof: subtle drift → BLOCKED → targeted regen
  → READY_FOR_APPROVAL → educator approves → export.

Primary judged link: `docs/demo/index.html` (GitHub Pages, no API key).

---

## 8. Project journey (~250 words)

- v1 adversarial review: scope cut, eval-first order enforced, cached demo made
  primary, educator wedge clarified.
- v3 deep review: keyword gate → structural audit (D1); LLM judge demoted to advisory
  (D3=C); injection now gates export (fix C2); fact-id validity added (fix C3);
  generated-content sanitization added (fix F5 / Contract H); specificity test added
  (Contract G).
- Build-first discipline: no MCP/ADK before the pure-Python eval core is green.

---

## 9. Course concepts (~200 words)

| Concept | Evidence |
|---|---|
| MCP server | `guwen_mcp` stdio, 4 tools |
| Agent skills | `.agent/skills/*/SKILL.md`, trigger tests |
| Security | source guard, sanitizer, safe prompts, safety eval, policy gate, HITL |
| Deployability | GitHub Pages cached demo, no API key |
| Evaluation | structural audit + drift suite + baseline |
| ADK (target) | BuilderAgent + CriticAgent path-handoff |

---

## 10. Limitations and next work (~180 words)

- Gold set small (1–3 measured scenes); single-annotator with one independent check.
- Human rater pool limited; clarity eval advisory if < 2 raters.
- No image generation (text storyboard only in V1).
- No commercial creator workflow.
- LLM judge advisory only; calibration study deferred to V2.
- V2 verticals: museums, language-learning platforms, diaspora education.

---

## 11. Links (~50 words)

- GitHub repo: [PLACEHOLDER]
- Cached demo: [PLACEHOLDER — `docs/demo/index.html` via GitHub Pages]
- Video: [PLACEHOLDER]
- Cover image: `docs/cover_image.png`
