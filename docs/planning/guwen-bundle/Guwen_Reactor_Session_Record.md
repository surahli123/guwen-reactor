# Guwen Reactor — Session Record and Handoff

## Session purpose

The user is preparing a Kaggle AI Agents: Intensive — Vibe Coding capstone project. The initial idea was to build an agent that can turn Chinese classical/古文 fiction the user has read into comics, short videos, or at least reaction/roast-style scripts. Through discussion and adversarial review, the project was narrowed into a buildable solo capstone: **Guwen Reactor**, a source-grounded cross-cultural adaptation agent for English-speaking learners and educators.

## Key course/capstone constraints captured in the session

- Track selected: **Agents for Good**.
- Primary build audience: English-speaking learners and educators who do not know Classical Chinese.
- Capstone deliverables: public GitHub repo, up to 5-minute YouTube demo, up to 2,500-word writeup, cover image, and project link.
- Hard gate: demonstrate at least three of the course concepts. The final spec targets five: ADK multi-agent, MCP server, security features, deployability, and agent skills.
- Solo builder constraint: approximately 17 days, prompt-driven/vibe-coding skill level, not a strong manual debugger.

## Research and material reviewed

### Course whitepapers uploaded by the user

1. Day 1 — The New SDLC With Vibe Coding.
2. Day 2 — Agent Tools & Interoperability.
3. Day 3 — Agent Skills.
4. Day 4 — Vibe Coding Agent Security and Evaluation.
5. Day 5 — Spec-Driven Production Grade Development in the Age of Vibe Coding.

Important interpretation from the materials:

- Day 1 supports the framing that an agent is not just a model; the model needs a harness with instructions, tools, memory, orchestration, guardrails, and observability.
- Day 2 supports the choice to use a small local MCP server for tool interoperability and to keep full A2UI as V2 rather than a V1 dependency.
- Day 3 supports using skills as narrow procedural modules instead of creating a large swarm of sub-agents.
- Day 4 supports making evaluation and security the project’s differentiator: security proves the agent stayed inside the boundary; evaluation proves the output is worth shipping.
- Day 5 supports spec-driven development, BDD-style behavior specs, policy gates, human-in-the-loop, and context hygiene.

## Major product pivots during the session

### Pivot 1 — From “novel to comic/video” to “cross-cultural story accessibility”

Original idea:

```text
Chinese classical novel → comic / short video / reaction-roast content
```

Final positioning:

```text
Public-domain Classical Chinese story
→ English-friendly story card
→ cultural decoder
→ text storyboard and prompts
→ measured faithfulness evaluation
→ human approval
→ export
```

Reason: Kaggle audience is mostly English-speaking, and the capstone should demonstrate real agent design rather than only image/video generation.

### Pivot 2 — From Freestyle/creative tool to Agents for Good

Final track: **Agents for Good**.

Rationale: The project supports education, cultural accessibility, and the arts. The creative/creator workflow remains a V2 vision, not the V1 build.

### Pivot 3 — From multi-agent swarm to walking skeleton

Initial draft had too many layers: six skills, many MCP tool groups, A2UI, AgBOM, Vibe Diff, many artifacts, six-stage eval, and nine-step canonical flow.

Final V1 build:

- two ADK agents: BuilderAgent and CriticAgent;
- five V1 skills;
- one local MCP server;
- four core artifacts;
- one static HTML run canvas;
- one demo climax.

### Pivot 4 — From “generated images” to “text storyboard + visual prompts”

V1 does not generate images. It produces text storyboards and image/video prompts only.

Reason: cross-panel character consistency is a known hard problem, and solving it is not necessary to prove the capstone’s core agentic-engineering value.

## Locked V1 project definition

### Project name

**Guwen Reactor**

### Subtitle

**A Spec-Driven Agentic Workflow for Making Classical Chinese Stories Understandable, Visual, and Remixable**

### One-line pitch

Guwen Reactor reads a public-domain Classical Chinese story, builds source-grounded canon memory, generates English learner-facing artifacts, and proves adaptation fidelity with measured evaluation and human approval before export.

### Primary user

English-speaking learners and educators.

### V1 source text

Demo source: **管寧割席 / Guan Ning Cuts the Mat**, from *Shishuo Xinyu* / *世說新語*.

Important copyright rule:

- Ingest original Chinese only.
- Do not ingest existing English translations.
- Generate original English explanations from the public-domain Chinese source.

## Final V1 architecture

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

### V1 skills

- source-license-guard;
- classical-interpretation;
- cultural-localization;
- storyboard-generation;
- adaptation-evaluation.

The reaction-script skill was moved to V2 because V1 focuses on learner comprehension, not creator entertainment.

### Local MCP server

Name: `guwen_mcp`.

Tools:

- `get_source`;
- `check_source_policy`;
- `write_artifact`;
- `validate_artifact_schema`;
- `record_trace`;
- `run_eval_suite`;
- `render_run_canvas`.

### Core artifacts

- `story_spec.yaml`;
- `canon_memory.yaml`;
- `adaptation.yaml`;
- `eval_report.yaml`;
- `trace.jsonl`;
- `approval_diff.md`;
- `run_canvas.html`;
- `export_bundle.zip`.

## Evaluation design

The evaluation harness is the showpiece.

### Faithfulness

Measured as precision/recall against a manually constructed canon-memory gold set.

- Precision = supported generated claims / total generated claims.
- Recall = required gold plot beats covered / total required gold plot beats.
- Export threshold: precision >= 0.90, recall >= 0.85, unsupported critical claims = 0, forbidden claims = 0.

### Cross-cultural clarity

Measured with pairwise comparison between Guwen Reactor output and baseline output.

- Target: 10 pairwise comparisons.
- Minimum: 6 comparisons.
- Human raters: 3 target, 2 minimum.
- Report raw agreement and Cohen/Fleiss kappa.
- LLM judge can only be trusted if calibrated against human majority with >=80% agreement.

### Baseline

Naive one-shot prompt:

```text
Translate the following Classical Chinese passage into plain English.
Explain the story for an English-speaking audience.
Create an 8-panel storyboard.
Do not invent details.

[ORIGINAL CHINESE]
```

Baseline must fail often enough to prove the eval is discriminative, with a target failure rate of 30–40%. If the baseline is too weak or too strong, the writeup must disclose and adjust.

### Demo climax

The five-minute video proves the evaluation harness by showing this sequence:

```text
clean run
→ plant false claim: “Hua Xin keeps the gold”
→ faithfulness eval catches contradiction
→ export blocked
→ regenerate failed panel
→ eval passes
→ human approves
→ export bundle created
```

## Final MVP cut-list

Cut in order if behind:

1. slideshow export;
2. SRT export;
3. reaction-script entertainment mode;
4. human clarity set size;
5. gold set size;
6. Streamlit deployment;
7. MCP wrapper;
8. ADK two-agent split.

Never cut:

- source guard;
- canon memory;
- faithfulness eval;
- planted drift demo;
- human approval gate;
- public repo docs.

## Build-ready deliverables created in this chat

- `Guwen_Reactor_Build_Ready_Spec_v2.md` — final build-ready spec.
- `Guwen_Reactor_Session_Record.md` — this session record and handoff.
- `guwen_reactor_cover_image.png` — cover/pitch asset.
- `guwen_reactor_pitch_concept.png` — concept flow diagram.
- `guwen_reactor_architecture_design.png` — V1 architecture diagram.
- `guwen_reactor_eval_climax.png` — evaluation demo climax diagram.
- `guwen_reactor_ui_wireframe.png` — minimal English-first run canvas mockup.
- `Guwen_Reactor_Image_Gen_Prompt_Pack.md` — prompts for image-enabled generation tools.
- `Guwen_Reactor_Capstone_Asset_Bundle.zip` — packaged artifacts.

## Next coding step for the user

Use the build spec as the source of truth. Start with P0 only:

```text
source file + metadata
canon_gold.yaml
schemas
faithfulness eval
planted drift block
human approval gate
```

Do not start with UI polish, image generation, A2UI, slideshow, or creator workflow.
