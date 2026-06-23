# Product Spec — Guwen Reactor (V1)

## 1. Problem

Most English-speaking learners cannot directly access Classical Chinese stories. The
barrier is not only language — it includes historical context, idioms, social values,
genre conventions, and trust.

**Narrowed V1 product problem:**

> Educators need classroom-trustworthy adaptations of unfamiliar classical texts.
> They are accountable for accuracy, so they need visible source grounding,
> hallucination detection, and a human approval gate before using AI-generated
> material with learners.

## 2. Primary User

**English-speaking educators, teaching assistants, and curriculum builders.**

Learners are the beneficiaries, not the primary build user. A learner who cannot
read the source cannot personally verify fidelity. An educator can use the source-gold
and evaluation report to decide whether output is safe for classroom use.

Product wedge:
```
"I can use this in class without being embarrassed by a hallucination."
```

## 3. V1 Output Promise

Given a public-domain Classical Chinese scene, Guwen Reactor creates:

1. English story card
2. Cultural decoder
3. Small teaching pack
4. 8 text storyboard panels
5. Source-grounded evaluation report
6. Human approval diff
7. Cached HTML run canvas
8. Local export bundle

## 4. Positioning

**Not translation. Not video generation. Not reaction-video tooling.**

Guwen Reactor is a **source-grounded educational adaptation engine**:

```
Original Chinese source
→ source / copyright guard
→ canon gold / source memory
→ educator-friendly story card
→ cultural decoder
→ teaching pack
→ text storyboard
→ measured fidelity + safety evaluation
→ human approval
→ cached export
```

The differentiator is the harness around the model: specs, tools, memory, guardrails,
tests/evals, observability, deployment, and human judgment.

## 5. Narrowed Claim (D3=C — LOCKED)

**Primary eval claim:** *Source-grounded PLOT fidelity for classroom-safe adaptation.*

- **Hard gate covers:** storyboard plot claims only (action, motive/emotion via
  structural assertion_type + hedging field).
- **Advisory only (never export-blocking):** interpretive fields (`why_it_matters`,
  `modern_analogy`). The interpretive rubric runs and is reported in
  `eval_report.interpretive_advisory`. It never appears in `export_requires`.
- `interpretive_eval.py` is P2, first on the cut-list.

This means:
- We claim "source-grounded PLOT fidelity" — we can defend this with deterministic
  structural audit.
- We do NOT claim the full adaptation is "interpretively correct" — the rubric is
  a diagnostic signal, not a gate.

## 6. Copyright Posture

V1 ingests **only original public-domain Classical Chinese** and generates its own
English. It does not ingest, copy, paraphrase from, or compare against existing English
translations.

Approval wording (exact — do not paraphrase):
```
No existing English translation was provided to the generator.
```

Source guard blocks if:
- `english_translation_ingested == true`
- `source_mode` is not `public_domain_original`
- `source_license_unclear == true`

Required export label:
```
AI-assisted educational adaptation based on public-domain original Chinese text.
```

## 7. V1 vs V2 Boundary

V1 proves the engine on one measured scene (管寧割席 / Guan Ning Cuts the Mat),
plus one optional iconic recognition preview (三顧茅廬 — preview only, not measured).

V2 verticals include museums, language-learning platforms, diaspora education, and
creator workflows. V1 does not claim to build those.

The reusable engine is:
```
schemas + source guard + faithfulness gate + safety gate + HITL + cached run canvas
```
Only `canon_gold` and cultural-localization references are culture-specific.

## 8. Concept-Coverage Map (all 5 required; keep all)

| Concept | V1 evidence | Cuttable? |
|---|---|---|
| MCP server | Local stdio `guwen_mcp` with 4 tools | No |
| Agent skills | `.agent/skills/*/SKILL.md`, trigger tests | No (min 3) |
| Security | source guard, sanitizer, safe prompts, safety eval, policy gate, HITL, path confinement | No |
| Deployability | cached GitHub Pages demo, public repo, no API key required | No |
| Evaluation | pure-Python structural audit + drift suite + baseline | No |
| ADK multi-agent | BuilderAgent + CriticAgent wrapper | Target; cuttable if core at risk |

## 9. Eval Calibration Baseline

Before running B1, the expected fail band (30–40%) and the pre-registered adjustment
rule are committed to `specs/eval_plan.yaml`. See that file for the authoritative gate
definition (Contract F — single source of truth, never duplicated here).

> ILLUSTRATIVE example only — replace with measured run output:
> baseline fail rate = 35%, agent fail rate = 5%

## 10. V1 Definition of Done (abbreviated)

- `unsupported_critical_claims == 0` on demo scene
- Subtle motivation drift (D3) blocked deterministically
- Citation spoof (D5) blocked
- Injection (D6) fenced and blocked
- Coverage omission (D4) fails required-beat gate
- Human approval required before export
- Manifest-bound AIGC label on every export artifact
- Cached `docs/demo/index.html` opens without API key
- Public repo + public project link
