# Guwen Reactor — Build-Ready Spec v2

## 0. Adversarial Review Decisions

**C1 — Over-scope:** reviewer is right. V1 is cut to a walking skeleton: one source scene, one end-to-end run, two ADK agents, five essential skills, one local MCP server, four core artifacts, one static HTML run canvas, and one evaluation climax. Full A2UI, AgBOM, Vibe-Diff MFA, generated images, multi-story support, and commercial creator workflow move to V2.

**C2 — Eval must be measured:** accepted. V1’s showpiece is a measured eval harness with a manually built canon-memory gold set, precision/recall faithfulness, baseline comparison, pairwise clarity labels, and a planted-drift demo.

**C3 — Build-vs-pitch coherence:** accepted. V1 builds the learner/educator comprehension vertical only. Creator/short-form adaptation is V2 vision.

**C4 — A2UI feasibility:** full A2UI is cut from V1. V1 ships a static self-contained HTML run canvas. A2UI is V2.

**C5 — Image-gen trap:** V1 does not generate images. It produces text storyboards and visual prompts only.

**C6 — Demo climax:** the 5-minute video proves evaluation by planting a false story drift, blocking export, regenerating, passing, then approving export.

**C7 — Copyright precision:** V1 ingests original Classical Chinese only and generates its own English. No existing English translations are ingested.

**C8 — Concrete stack:** V1 uses Python, Google ADK, a local stdio MCP server, YAML/Pydantic schemas, pytest, Streamlit, and a cached-demo deploy path.

**C9 — Skills triage:** source guard, classical interpretation, cultural localization, storyboard, and evaluation are V1. Reaction-script as entertainment is V2.

**C10 — 17-day realism:** day-by-day plan below has cut triggers. Anything not demo-visible by Day 13 is cut.

---

## 1. Problem, Primary User, Positioning, and Vision

### 1.1 Primary build problem

Most English-speaking learners cannot directly access Classical Chinese stories because the barrier is not just language. They also lack historical context, idioms, social values, and genre conventions.

**Guwen Reactor V1** solves one narrow problem:

> Given one public-domain Classical Chinese scene, produce an English-friendly learning artifact that explains what happened, why it matters culturally, and how it could be visualized — while proving the adaptation is faithful to source facts.

### 1.2 Primary V1 user

**English-speaking learners and educators** who want a short, reliable, culturally explained version of a Classical Chinese story for classroom, self-study, or cultural discovery.

V1 is not built for influencers, comic studios, or automated content farms.

### 1.3 Positioning

**Not translation. Not video generation.**

Guwen Reactor is a **source-grounded cross-cultural adaptation engine**:

```text
Original Chinese source
→ source/copyright guard
→ canon memory
→ plain-English story card
→ cultural decoder
→ 8-panel text storyboard
→ measured fidelity + clarity evaluation
→ human approval
→ export
```

### 1.4 Vision, without bait-and-switch

The commercial/long-term vision is **not “古文 only.”** It is a reusable engine for cross-cultural adaptation:

```text
unfamiliar source culture/language
→ grounded story understanding
→ audience-specific cultural localization
→ adaptive learning/creative artifacts
→ fidelity evaluation
```

V2 verticals can include creators, museums, language learning, diaspora education, and short-form cultural explainers. V1 proves the engine on one public-domain Classical Chinese scene.

---

## 2. Architecture: V1-BUILD vs V2-PITCH

### 2.1 V1 architecture

```text
Streamlit UI / CLI
    ↓
ADK Root Orchestrator
    ├── BuilderAgent
    │     uses V1 skills + guwen_mcp tools
    └── CriticAgent
          read-only evaluator + trust gate recommendation
    ↓
PolicyGate.py
    ↓
Human Approval
    ↓
Export Bundle
```

### 2.2 Components

| Component | V1-BUILD | V2-PITCH | Decision |
|---|---:|---:|---|
| ADK Root Orchestrator | Yes | Expandable | Minimal ADK runtime controlling run state |
| BuilderAgent | Yes | Yes | Generates structured artifacts |
| CriticAgent | Yes | Yes | Justified check-and-balance agent |
| 10-agent swarm | No | No | Explicitly rejected |
| `.agent/skills/` library | Yes | Yes | Five V1 skills only |
| Local MCP server `guwen_mcp` | Yes | Yes | One server, seven tools |
| Full A2UI protocol | No | Yes | Too risky for 17 days |
| Static HTML run canvas | Yes | Yes | Minimal visual proof |
| AgBOM | No | Yes | V2 only |
| Vibe Diff with MFA | No | Yes | V1 uses plain-English approval diff |
| Image generation | No | Optional V2 | Text prompts only |
| Slideshow video | Optional | Yes | Cut first if behind |
| Multi-story corpus | No | Yes | V1 evaluates 3–5 short scenes but demos one |
| Creator/short-form workflow | No | Yes | Vision only |

### 2.3 V1 file tree

```text
guwen-reactor/
  README.md
  AGENTS.md
  requirements.txt

  specs/
    product_spec.md
    eval_plan.yaml
    threat_model.md
    demo_script.md

  app/
    streamlit_app.py
    adk_app.py
    policy_gate.py
    approval.py

  agents/
    builder_agent.py
    critic_agent.py

  .agent/
    skills/
      source-license-guard/
        SKILL.md
      classical-interpretation/
        SKILL.md
      cultural-localization/
        SKILL.md
      storyboard-generation/
        SKILL.md
      adaptation-evaluation/
        SKILL.md

  guwen_mcp/
    server.py
    tools.py

  schemas/
    story_spec.schema.yaml
    canon_memory.schema.yaml
    adaptation.schema.yaml
    eval_report.schema.yaml
    trace_event.schema.yaml

  data/
    sources/
      guan_ning_cuts_mat/
        source.zh.txt
        source_metadata.yaml
    gold/
      canon_gold.yaml
      clarity_pairs.yaml
      human_labels.csv

  runs/
    demo_run/
      story_spec.yaml
      canon_memory.yaml
      adaptation.yaml
      eval_report.yaml
      trace.jsonl
      approval_diff.md
      run_canvas.html
      export_bundle.zip

  evals/
    test_schema.py
    test_policy_gate.py
    test_faithfulness.py
    test_trajectory.py
    run_baseline.py
    run_eval_suite.py

  docs/
    architecture.md
    measured_results.md
    capstone_writeup.md
```

---

## 3. Evaluation Harness

This is the showpiece. Security answers whether the agent stayed inside boundaries; evaluation answers whether the output is worth shipping.

### 3.1 Core artifacts under evaluation

V1 evaluates four artifacts:

```text
story_spec.yaml
canon_memory.yaml
adaptation.yaml
eval_report.yaml
```

`adaptation.yaml` contains:

```yaml
story_card:
  title_en: string
  one_sentence_hook: string
  plain_english_summary: string
  why_it_matters: string
  modern_analogy: string

cultural_decoder:
  key_terms:
    - term_zh: string
      explanation_en: string
      source_fact_ids: [string]

storyboard:
  panels:
    - panel_id: P01
      visual_description: string
      caption_en: string
      source_fact_ids: [string]
      plot_beat_ids: [string]
      character_ids: [string]

export:
  aigc_label: "AI-assisted educational adaptation draft"
```

### 3.2 Canon-memory gold set

#### Gold set size

V1 target:

```text
5 short public-domain scenes
1 demo scene
4 eval-only scenes
```

Fallback if behind:

```text
3 scenes minimum
1 demo scene
2 eval-only scenes
```

#### Who labels it

Primary labeler: builder.

Validation:

```text
Pass 1: builder labels source facts manually.
Pass 2: builder re-checks after 24 hours against original Chinese.
Pass 3: LLM critique asks: “Which gold facts are unsupported by the Chinese?”
Pass 4: builder accepts/rejects critique manually.
```

Cross-cultural clarity labels require English-speaking humans:

```text
Target: 3 English-speaking human raters
Minimum: 2 raters
No Chinese knowledge required
Task: pairwise choose which output is clearer for an English learner
```

If fewer than 2 human raters are available by Day 11, clarity becomes an advisory metric only, and the writeup must disclose this limitation.

### 3.3 Gold canon schema

`data/gold/canon_gold.yaml`

```yaml
scenes:
  - scene_id: G01
    title_en: "Guan Ning Cuts the Mat"
    source_id: "shishuo_xinyu_de_xing_guan_ning"
    required_characters:
      - id: C_GUAN_NING
        canonical_names: ["Guan Ning", "管宁", "管寧"]
        role: "principled scholar"
      - id: C_HUA_XIN
        canonical_names: ["Hua Xin", "华歆", "華歆"]
        role: "friend/classmate"
    relationships:
      - id: R01
        subject: C_GUAN_NING
        relation: "studies_with"
        object: C_HUA_XIN
    plot_beats:
      - id: B01
        required: true
        text: "Guan Ning and Hua Xin are gardening together."
      - id: B02
        required: true
        text: "They see a piece of gold in the ground."
      - id: B03
        required: true
        text: "Guan Ning treats the gold like debris."
      - id: B04
        required: true
        text: "Hua Xin picks up the gold and throws it away."
      - id: B05
        required: true
        text: "A prestigious carriage passes while they study."
      - id: B06
        required: true
        text: "Guan Ning keeps reading."
      - id: B07
        required: true
        text: "Hua Xin stops reading to look."
      - id: B08
        required: true
        text: "Guan Ning cuts the mat and ends the friendship."
    forbidden_claims:
      - "Hua Xin keeps the gold."
      - "Guan Ning attacks Hua Xin."
      - "The two reconcile in the scene."
      - "A romantic relationship exists."
```

### 3.4 Faithfulness metric

The spec requires faithfulness as precision/recall against canon memory.

#### Ground truth

Manual canon memory:

```text
characters
relationships
plot_beats
atomic facts
forbidden claims
```

#### Generated fact extraction

The system requires every storyboard panel and cultural claim to include `source_fact_ids` or `plot_beat_ids`.

Then the evaluator creates:

```yaml
generated_claims:
  - claim_id: GC01
    text: "Hua Xin picks up the gold and throws it away."
    cited_fact_ids: [B04]
    artifact_location: "storyboard.P03.caption_en"
```

#### Computation

```text
Supported generated claims =
  generated claims whose cited fact IDs exist
  AND whose claim does not contradict the gold fact
  AND whose claim is not in forbidden_claims

Faithfulness Precision =
  supported_generated_claims / total_generated_claims

Faithfulness Recall =
  required_gold_plot_beats_covered / total_required_gold_plot_beats
```

#### Objective or judge-based?

Hybrid:

```text
Objective:
- valid fact IDs
- required plot beat coverage
- schema checks
- forbidden-claim string/semantic flags

Judge-based:
- semantic contradiction check between generated claim and gold fact
```

#### Thresholds

```yaml
faithfulness_gate:
  precision_min: 0.90
  recall_min: 0.85
  unsupported_critical_claims_max: 0
  forbidden_claims_max: 0
```

Export is blocked if any critical unsupported claim appears.

### 3.5 Cross-cultural clarity metric

#### Goal

Measure whether an English-speaking learner understands the story without knowing Chinese.

#### Human-labeled calibration set

```text
10 pairwise comparisons target
6 pairwise comparisons minimum
Each pair:
  A = Guwen Reactor output
  B = baseline one-shot output
Raters:
  3 English-speaking humans target
  2 minimum
Labels:
  A clearer / B clearer / Tie
```

#### Agreement

```text
If 3 raters:
  report Fleiss' kappa
If 2 raters:
  report Cohen's kappa
Also report raw agreement
```

Threshold:

```yaml
human_label_quality:
  raw_agreement_min: 0.70
  kappa_target_min: 0.55
```

If kappa is below 0.55, the writeup reports disagreement and does not overclaim clarity.

#### LLM judge calibration

The LLM judge receives pairwise outputs with randomized A/B order.

```text
LLM clarity agreement =
  LLM pairwise choice matches human majority / total labeled pairs
```

Threshold:

```yaml
llm_clarity_judge:
  agreement_with_human_majority_min: 0.80
  position_bias_check: "run swapped A/B order; choices must be stable >=80%"
```

If the LLM clarity judge fails calibration, it becomes report-only and does not gate export.

### 3.6 Baseline

#### Baseline prompt

`evals/baseline_prompt.txt`

```text
Translate the following Classical Chinese passage into plain English.
Explain the story for an English-speaking audience.
Create an 8-panel storyboard.
Do not invent details.

[ORIGINAL CHINESE]
```

No canon memory. No source fact IDs. No staged evaluation. No policy gate. No regenerate loop.

#### Baseline failure criteria

A baseline output fails if any of these occur:

```text
faithfulness_precision < 0.90
faithfulness_recall < 0.80
unsupported_critical_claims > 0
forbidden_claims > 0
cross-cultural clarity loses to V1 by human majority
```

#### Required discriminative band

```yaml
baseline_expected_failure_rate:
  target_min: 0.30
  target_max: 0.40
```

If baseline failure is below 30%, the metric is not discriminative enough; the writeup must say so. If baseline failure is above 50%, add a stronger one-shot baseline with explicit “cite source facts” instruction to avoid comparing against a strawman.

### 3.7 Trajectory evaluation

`trace.jsonl` logs each step:

```json
{"step":1,"event":"source_loaded","tool":"get_source","agent":"BuilderAgent"}
{"step":2,"event":"license_checked","tool":"check_source_policy","agent":"BuilderAgent"}
{"step":3,"event":"canon_built","artifact":"canon_memory.yaml","agent":"BuilderAgent"}
{"step":4,"event":"adaptation_built","artifact":"adaptation.yaml","agent":"BuilderAgent"}
{"step":5,"event":"eval_run","artifact":"eval_report.yaml","agent":"CriticAgent"}
{"step":6,"event":"approval_requested","artifact":"approval_diff.md","agent":"PolicyGate"}
{"step":7,"event":"export_allowed","artifact":"export_bundle.zip","agent":"PolicyGate"}
```

Required order:

```text
source_loaded
→ license_checked
→ canon_built
→ adaptation_built
→ eval_run
→ approval_requested
→ export_allowed
```

Threshold:

```yaml
trajectory_gate:
  required_events_present: true
  license_before_generation: true
  eval_before_approval: true
  approval_before_export: true
```

### 3.8 Policy and safety gate

Objective checks:

```yaml
policy_gate:
  allowed_source_modes:
    - public_domain_original
    - user_owned
    - authorized_excerpt
  blocked_source_modes:
    - copyrighted_modern_full_text
    - existing_english_translation_unknown_license
    - unclear_source
  export_requires:
    - schema_valid
    - license_pass
    - faithfulness_pass
    - safety_pass
    - human_approved
    - aigc_label_present
```

Safety checks are intentionally narrow for V1:

```text
No explicit/gory adaptation.
No sexualized framing.
No hate/harassment.
No instructions for wrongdoing.
No publishing action; export is local files only.
```

### 3.9 Trust gate summary

`eval_report.yaml`

```yaml
trust_gate:
  export_status: "BLOCKED" | "APPROVED"
  reasons:
    - code: "FAITHFULNESS_PRECISION_LOW"
      severity: "critical"
      detail: "Precision 0.78 < 0.90"
  metrics:
    faithfulness_precision: 0.78
    faithfulness_recall: 1.00
    unsupported_critical_claims: 1
    clarity_pairwise_preference_rate: 0.70
    schema_valid: true
    trajectory_valid: true
    license_valid: true
    human_approved: false
```

---

## 4. MVP Build Order and Fallback Cut-List

### 4.1 Walking skeleton build order

Build one thin path first:

```text
1. Source file loads.
2. Source license guard passes.
3. BuilderAgent creates canon_memory.yaml.
4. BuilderAgent creates adaptation.yaml.
5. CriticAgent runs deterministic + faithfulness eval.
6. PolicyGate blocks or allows export.
7. Human approves.
8. HTML run canvas renders.
9. Export bundle downloads.
```

### 4.2 Prioritized build order

| Priority | Build item | Definition of done |
|---:|---|---|
| P0 | Source + gold canon | One scene has source metadata and canon gold |
| P0 | Schemas | `pytest evals/test_schema.py` passes |
| P0 | Faithfulness eval | Planted drift is blocked |
| P0 | Human approval gate | Export impossible without approval |
| P1 | ADK two-agent workflow | Builder and Critic produce separate trace events |
| P1 | MCP server | Tools list and run through stdio |
| P1 | Static HTML run canvas | Opens locally and shows source → output → eval |
| P2 | Baseline comparison | Baseline run and measured failure rate |
| P2 | Human clarity calibration | 6–10 pairwise labels |
| P3 | SRT export | Optional |
| P3 | Slideshow | Optional |
| P3 | Reaction-video script | V2/optional |

### 4.3 Prioritized fallback cut-list

Cut in this order if behind:

1. Slideshow export — keep HTML storyboard.
2. SRT export — keep captions in `adaptation.yaml`.
3. Reaction-script entertainment mode — keep learner story card and storyboard.
4. Human clarity set size — reduce from 10 pairs to 6 pairs.
5. Gold set size — reduce from 5 scenes to 3 scenes.
6. Streamlit deploy — replace with GitHub Pages static run canvas plus local CLI.
7. MCP wrapper — last-resort cut only if ADK + skills + security + deployability remain demonstrable.
8. ADK two-agent split — last-resort cut only if MCP + skills + security + deployability remain demonstrable.

Hard no-cut items:

```text
source guard
canon memory
faithfulness eval
planted drift demo
human approval gate
public repo docs
```

---

## 5. Tech Stack and Gold-Set Construction

### 5.1 Runtime stack

```yaml
language:
  python: "3.11+"

agent_runtime:
  google_adk: "primary orchestration framework"
  agents:
    - BuilderAgent
    - CriticAgent

tool_protocol:
  mcp_python_sdk: "local stdio MCP server"
  server_name: "guwen_mcp"

ui:
  streamlit: "interactive local/deployed UI"
  static_html: "self-contained run canvas fallback"

schemas:
  pydantic: "Python validation"
  yaml: "human-readable artifacts"
  jsonschema_or_pydantic: "CI validation"

eval:
  pytest: "deterministic tests"
  llm_as_judge: "faithfulness contradiction + clarity pairwise"
  pandas_optional: "metrics table generation"

models:
  generation_model: "Gemini Flash-class model through ADK"
  judge_model: "Gemini Pro-class model through ADK"
  fallback_mode: "cached demo artifacts if API unavailable"

deployment:
  primary: "Hugging Face Space or Streamlit Community Cloud"
  fallback: "GitHub Pages static HTML + local CLI"
```

### 5.2 MCP tools

`guwen_mcp/server.py`

```yaml
tools:
  - name: get_source
    input: {source_id: string}
    output: {source_text: string, metadata: object}

  - name: check_source_policy
    input: {source_id: string}
    output: {allowed: boolean, source_mode: string, reasons: list}

  - name: write_artifact
    input: {run_id: string, artifact_type: string, yaml_text: string}
    output: {path: string, sha256: string}

  - name: validate_artifact_schema
    input: {artifact_type: string, path: string}
    output: {valid: boolean, errors: list}

  - name: record_trace
    input: {run_id: string, event: object}
    output: {ok: boolean}

  - name: run_eval_suite
    input: {run_id: string, suite: string}
    output: {eval_report_path: string, passed: boolean}

  - name: render_run_canvas
    input: {run_id: string}
    output: {html_path: string}
```

MCP is local stdio only. No credentials. No remote write tools.

### 5.3 Skills triage

| Skill | V1-BUILD | V2-PITCH | Notes |
|---|---:|---:|---|
| `source-license-guard` | Yes | Yes | Essential |
| `classical-interpretation` | Yes | Yes | Essential |
| `cultural-localization` | Yes | Yes | Essential |
| `reaction-script` | No | Yes | Cut from V1 core; optional narration only |
| `storyboard-generation` | Yes | Yes | Essential |
| `adaptation-evaluation` | Yes | Yes | Essential |

V1 uses five skills, not six. The reaction-script skill becomes V2 because the build user is learner/educator, not creator.

### 5.4 Canon-memory gold construction recipe

```text
Step 1: Select 5 public-domain micro-scenes from Shishuo Xinyu.
Step 2: Store each original Chinese scene in data/sources/<scene_id>/source.zh.txt.
Step 3: Create source_metadata.yaml with title, author, source URL, license mode, and no-translation-ingested flag.
Step 4: Manually label characters, relationships, plot beats, atomic facts, and forbidden claims.
Step 5: Run LLM critique against original Chinese: “Find unsupported or missing gold facts.”
Step 6: Builder manually accepts/rejects critique.
Step 7: Lock gold file before running baseline and V1 comparison.
```

Minimum gold size:

```yaml
minimum_gold:
  scenes: 3
  plot_beats_per_scene: 5
  atomic_facts_per_scene: 8
  forbidden_claims_per_scene: 3
```

Target gold size:

```yaml
target_gold:
  scenes: 5
  plot_beats_per_scene: 6-10
  atomic_facts_per_scene: 10-15
  forbidden_claims_per_scene: 3-5
```

---

## 6. Demo Path: 5-Minute Climax

### 6.1 Single proof moment

The video climax:

> The scorecard catches a planted faithfulness drift, blocks export, shows the human-readable approval diff, regenerates, passes, and exports.

This proves the project’s differentiator: measured source fidelity.

### 6.2 Exact demo run

#### 0:00–0:30 — Problem

Show title:

```text
Guwen Reactor
Making Classical Chinese stories understandable, visual, and faithful for English-speaking learners.
```

Narration:

```text
Most English-speaking learners cannot read Classical Chinese.
The hard part is not only translation. It is source fidelity, cultural context, and trust.
```

#### 0:30–1:00 — Architecture

Show diagram:

```text
Source Guard → Canon Memory → Cultural Localization → Storyboard → Evaluation → Human Approval → Export
```

Mention two agents:

```text
BuilderAgent creates artifacts.
CriticAgent evaluates them before export.
```

#### 1:00–2:00 — Clean source run

Input source:

```text
Guan Ning Cuts the Mat
```

Show generated outputs:

```text
story_card.title_en
plain_english_summary
cultural_decoder
8 storyboard panels
```

#### 2:00–3:15 — Planted drift

Toggle:

```bash
python evals/inject_drift.py --run runs/demo_run --drift hua_xin_keeps_gold
```

Injected false panel:

```yaml
panel_id: P03
caption_en: "Hua Xin keeps the gold, proving he values wealth over friendship."
source_fact_ids: [B04]
```

Gold fact says Hua Xin picks it up and throws it away.

Run:

```bash
python evals/run_eval_suite.py --run runs/demo_run
```

Expected result:

```yaml
faithfulness_precision: 0.78
faithfulness_recall: 1.00
unsupported_critical_claims: 1
export_status: BLOCKED
reason: "Generated claim contradicts B04: Hua Xin throws the gold away."
```

#### 3:15–4:00 — Regenerate and pass

Click:

```text
Regenerate failed panels
```

Corrected panel:

```yaml
caption_en: "Hua Xin picks up the gold, then throws it away — but the hesitation matters."
source_fact_ids: [B04]
```

Expected result:

```yaml
faithfulness_precision: 1.00
faithfulness_recall: 1.00
unsupported_critical_claims: 0
export_status: READY_FOR_APPROVAL
```

#### 4:00–4:40 — Human approval

Show `approval_diff.md`:

```text
Original intent:
Explain Guan Ning’s values to English-speaking learners.

Proposed export:
- Story card
- Cultural decoder
- 8-panel storyboard
- AI-assisted educational adaptation label

Risk summary:
No unsupported source claims detected.
No copyrighted English translation used.
No generated images.
```

Click:

```text
Approve export
```

#### 4:40–5:00 — Export and rubric mapping

Show:

```text
export_bundle.zip
run_canvas.html
eval_report.yaml
trace.jsonl
```

Narration:

```text
The demo proves the core engine: source grounding, measured faithfulness, security gate, human approval, and deployable educational artifacts.
```

### 6.3 Rubric mapping

| Rubric area | Demo evidence |
|---|---|
| Core concept/value | English learners can understand inaccessible classical text |
| 5-minute video | Drift blocked → regenerate → approve → export |
| Writeup | Explains Agents for Good and measured eval |
| Technical implementation | ADK agents, MCP tools, skills, eval harness, schemas |
| Documentation | Specs, architecture, eval plan, threat model |
| Hard gate concepts | ADK, MCP, skills, security, deployability |

---

## 7. Copyright and Source Plan

### 7.1 Exact V1 source

Demo source:

```yaml
source_id: shishuo_xinyu_de_xing_guan_ning
title_zh: 管寧割席
title_en: Guan Ning Cuts the Mat
work: 世說新語 / 德行
traditional_author: 劉義慶
source_language: Classical Chinese
source_mode: public_domain_original
english_translation_ingested: false
```

### 7.2 Original Chinese source text

`data/sources/guan_ning_cuts_mat/source.zh.txt`

```text
管寧、華歆共園中鋤菜，見地有片金，管揮鋤與瓦石不異，華捉而擲去之。
又嘗同席讀書，有乘軒冕過門者，寧讀如故，歆廢書出看。
寧割席分坐曰：「子非吾友也。」
```

### 7.3 Licensing rule

V1 does not ingest, copy, paraphrase from, or compare against any existing English translation. The agent produces a new English explanation from the original Chinese source.

### 7.4 Source guard enforcement

`source_metadata.yaml`

```yaml
source_id: shishuo_xinyu_de_xing_guan_ning
allowed: true
source_mode: public_domain_original
author_death_year: 444
english_translation_ingested: false
blocked_derivative_sources:
  - existing_english_translation
  - modern_annotated_translation
  - copyrighted_textbook_translation
allowed_operations:
  - explain_in_own_english
  - summarize
  - produce_storyboard
  - export_educational_adaptation
required_export_label:
  - "AI-assisted educational adaptation based on public-domain original Chinese text."
```

PolicyGate blocks export if:

```text
source_mode != public_domain_original
english_translation_ingested == true
aigc_label missing
human_approved == false
```

---

## 8. Concept-Coverage Map

The capstone hard gate requires at least three concepts. V1 demonstrates five.

| Concept | V1 evidence | Code/video proof |
|---|---|---|
| ADK multi-agent | Root orchestrator + BuilderAgent + CriticAgent | `app/adk_app.py`, trace shows both agents |
| MCP server | Local `guwen_mcp` stdio server | `guwen_mcp/server.py`, tool listing in video |
| Security features | source guard, policy gate, no translation ingestion, approval gate, trace | `app/policy_gate.py`, blocked export demo |
| Deployability | Streamlit/HF Space with cached demo | public project link |
| Agent skills / Agents CLI style | `.agent/skills/*` with narrow SKILL.md files | repo + video walkthrough |
| Antigravity | Build process only, not required | optional devlog; not core gate |

---

## 9. Risk Register

| Risk | Severity | Mitigation |
|---|---:|---|
| Over-scope causes no working demo | High | Walking skeleton first; cut-list enforced on Days 4, 7, 10, 13 |
| Eval becomes illustrative, not measured | High | Manual canon gold, precision/recall, baseline, planted drift, published thresholds |
| Human clarity labels unavailable | Medium | Minimum 2 raters; if unavailable, clarity becomes advisory and writeup discloses limitation |
| ADK/MCP integration slows solo builder | Medium | Keep tools pure Python first; wrap in MCP after tests pass; last-resort direct Python fallback |
| Copyright ambiguity | High | Original Chinese only; no English translations; allowlisted sources; export blocked on unclear source |
| Deployment breaks due API/key limits | Medium | Cached demo mode; static HTML run canvas; local CLI works without hosted model |
| Image generation distracts from evaluation | Medium | No image generation in V1; prompts only |
| Baseline does not fail enough | Medium | Publish actual result; add stronger one-shot baseline if naive baseline is too weak/strong |
| LLM judge disagreement | Medium | Calibrate against human pairwise labels; disable judge as gate if agreement <80% |
| Solo debugging difficulty | High | Pytest-first, small files, schema validation, deterministic eval before agent integration |

---

## 10. 17-Day Plan with Definition of Done

Assume start: **June 20, 2026**. Deadline: **July 6, 2026 23:59 PT**.

| Day | Date | Milestone | Definition of done | Cut trigger |
|---:|---|---|---|---|
| 1 | Jun 20 | Repo + spec lock | Repo created; `specs/product_spec.md`, `eval_plan.yaml`, `threat_model.md` committed | No new features after spec lock |
| 2 | Jun 21 | Source + gold scene | Guan Ning source, metadata, first canon gold file complete | If source uncertain, switch to another public-domain scene immediately |
| 3 | Jun 22 | Schemas + validators | `story_spec`, `canon_memory`, `adaptation`, `eval_report` schemas pass pytest | Drop extra output artifacts |
| 4 | Jun 23 | MCP tools skeleton | `guwen_mcp` lists tools and writes artifacts locally | If MCP broken, build direct Python tools first and wrap later |
| 5 | Jun 24 | ADK two-agent skeleton | BuilderAgent and CriticAgent write trace events | If ADK blocks progress, make CLI workflow and return to ADK Day 8 |
| 6 | Jun 25 | V1 skills | Five `SKILL.md` files with positive/negative triggers | Drop reaction-script skill fully |
| 7 | Jun 26 | First end-to-end generation | Source → canon → adaptation YAML works for one scene | If no E2E run, cut Streamlit until Day 12 |
| 8 | Jun 27 | Deterministic evals | Schema, policy, trajectory tests pass | Drop SRT/slideshow |
| 9 | Jun 28 | Faithfulness eval + planted drift | Injected false claim is blocked with precision/recall report | This is non-cuttable |
| 10 | Jun 29 | Baseline run | Naive baseline evaluated on 3–5 scenes; failure rate computed | If baseline setup slow, use 3 scenes |
| 11 | Jun 30 | Human clarity labels | 6–10 pairwise labels collected; kappa/agreement computed | If labels unavailable, mark clarity advisory |
| 12 | Jul 1 | Run canvas UI | Static `run_canvas.html` renders source, output, eval, trace | Full A2UI permanently cut |
| 13 | Jul 2 | Approval + export gate | Export blocked before approval and allowed after approval | If deploy not started, static HTML becomes primary project link |
| 14 | Jul 3 | Streamlit/cached demo deploy | Public link works or GitHub Pages fallback works | No live-model dependency for demo |
| 15 | Jul 4 | Documentation | README, architecture, eval results, threat model complete | No new code except bug fixes |
| 16 | Jul 5 | Video recording | <=5-minute video recorded with planted-drift climax | If live demo flaky, use cached run with terminal commands |
| 17 | Jul 6 | Final submission | GitHub public, video public/unlisted, writeup <=2,500 words, cover image, project link | Submit by afternoon PT, no last-hour risky changes |

### Final V1 definition of done

```yaml
v1_done:
  one_public_domain_source: true
  original_chinese_only: true
  english_story_card: true
  cultural_decoder: true
  text_storyboard: true
  canon_memory_gold: true
  faithfulness_precision_recall: true
  baseline_comparison: true
  planted_drift_blocked: true
  human_approval_before_export: true
  static_html_run_canvas: true
  public_repo: true
  public_project_link: true
  five_minute_video: true
```

### Final V2 boundary

Anything below is writeup vision only unless V1 finishes early:

```text
full A2UI
image generation
character consistency across generated images
multi-story corpus
creator monetization workflow
short-form video generation
remote A2A agents
AgBOM
cryptographic MFA Vibe Diff
```
