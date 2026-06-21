# Spec-Driven Production Grade Development in the Age of Vibe Coding

**Author:** Lee Boonstra | **Date:** May 2026 | **Course:** Kaggle AI Agents Intensive — Vibe Coding

---

## Core Thesis

> "Vibe coding is not vibe-in-production."

Speed is not the bottleneck anymore — integration, review, and governance are. AI has shifted the bottleneck *downstream* to humans who must verify, test, and integrate AI-generated output. The paper is a playbook for how to cross that gap without burning the team or shipping broken software.

---

## 1. Introduction: The Illusion of Speed

- Coding agents (Antigravity, Gemini CLI) act as **Hybrid Team Members**: LLM as brain, tools as hands.
- Bug-to-code ratio challenge: AI writes code faster, but also generates potential mistakes at an unprecedented rate.
- Key reframe: AI can write *more* comprehensive test coverage than any human in the same timeframe — this is the counter to the bug rate problem.
- **"Vibe coding"** = using AI to rapidly generate code based on high-level intent rather than rigid manual coding.
- In enterprise: called **"Development with Agentic AI."** Unlike standard GenAI (smart autocomplete), Agentic AI uses tools to integrate into the workflow — it can reason, write specs, use a browser, commit code.
- The real problem: if human reviewers are drowning in AI-generated PRs, "the speed of writing becomes irrelevant. The process isn't actually faster; it is simply creating a bigger pile of stuff to be sorted later."

---

## 2. Spec-Driven Development (SDD)

### The Central Shift

- Traditional: Code-First (vague idea → open editor → type until something works).
- New paradigm: **Spec-First**. Most time is now spent writing high-quality specifications.
- Developer role = **technical architect**, not coder.
- **"Code is now disposable."** If the spec is rock-solid, the entire codebase can be regenerated repeatedly (e.g., flip Python to JavaScript in an afternoon).

### A Good Specification

> "A good specification is an **Architectural North Star**. It prevents 'context fragmentation' — the digital equivalent of the game 'telephone,' where the AI starts losing the plot because it's looking at outdated snapshots of files."

A production-grade spec contains:

1. **Full Technical Design** — requirements, database schemas, API specifications ("contracts" allowing different parts to talk to each other). Don't say "make a login page"; break it into pieces.
2. **Visual Aids** — diagrams, specific tools and libraries *with version numbers*.
3. **Background Information** — the "Why" behind the "What." Helps the agent think forward and anticipate steps.
4. **Scenarios** — what good looks like, what's wrong, edge cases.

**Practical tip from author:** Write technical designs in Google Docs, let humans review them (catch logic flaws *before* the AI generates thousands of lines of broken code), then File > Download > Markdown → add to a `specs/` folder.

### Format: Hybrid Markdown + Conditional YAML

Research citation: Ouyang et al. 2026, *SkCC: Portable and Secure Skill Compilation for Cross-Framework LLM Agents* (arxiv.org/abs/2605.03353):

- LLM agents exhibit **up to 40% performance drop** when using generic, unoptimized Markdown files.
- For Gemini: **hybrid Markdown + Conditional YAML** is optimal.
  - Markdown headers: anchor attention.
  - YAML for structured config / data schemas with nesting depth > 3.
- Parsing accuracy for deeply nested configs: **YAML 51.9% > JSON 43.1% > XML 33.8%**.
- SkCC tool auto-compiles a single-source instruction file into optimal target format in < 10ms.

**Tokenization as hard constraint:** Every character, newline, and indentation space consumes token budget. Treat the `/specs` folder as a "lean, compiled instruction set." Eliminate the "reasoning format tax."

### Behavior-Driven Development (BDD)

> "A Behavior-Driven Development (BDD) specification is the ultimate tool for turning vague, ambiguous human ideas into a precise architectural design that an AI agent can build without guessing."

- Uses **Gherkin syntax**: `Scenario / Given / When / Then`.
- Forces LLM to think in terms of **State → Action → Outcome**.
- Completely eliminates vibe coding; keeps the agent on a strict track.

---

## 3. Where Do Instructions Live? (3 Layers)

### Layer 1: Chat Interface
- Short-lived, session-specific.
- Use for high-level orchestration and instant feedback loops.
- Example: `"Review the design in specs/payment_retry.md and generate the failing unit tests defined in Scenario 3."`
- **Do NOT dump a 100-page system design into chat** — exhausts context budget, increases latency, fragments context.

### Layer 2: `specs/` Folder (Task-specific, Version-Controlled)
- Static folder checked into the repository.
- Stores: technical design, BDD scenarios, API contracts, structural YAML schemas.
- Agent dynamically indexes this directory to build and verify code.
- Path example: `./my-app/specs/my_spec.md`

### Layer 3: Agent Skills (Reusable, Feature/Behavior-Focused)
- Structured Markdown files with specialized, trigger-based workflows.
- Must be stored in `.agent` directory to be recognized by Antigravity workspace manager.
- Teach the agent repeatable engineering habits (e.g., auto-maintain `CHANGELOG.md` when code changes).
- Path example: `./my-app/.agent/skills/docs-maintenance/SKILL.md`

### Layer 4: System Prompts (Global, Identity-Focused)
- **Global Profile:** `~/.gemini/GEMINI.md` — defines universal persona, default style, core principles regardless of project.
- **Shared Multi-Tool Config:** `AGENTS.md` (`./my-app/.agents/AGENTS.md`) — prevents instructional fragmentation when team uses multiple AI clients. Cross-tool foundation; local GEMINI.md retains highest priority.
- **Project Spec:** `./my-app/.gemini/GEMINI.md` — project's DNA, CLI agent auto-detects and prioritizes its rules.

---

## 4. Execution Modes: Different Prompts for Different Use Cases

### Mode 1: Project Generation (The Architect)
- Scaffold from scratch.
- **No YOLO Mode:** Agent must propose folder structure and tech stack *first* for confirmation before coding.
- Prompt must include generation of tests, documentation, and logging.
- **Always include version numbers** for every library — prevents agent falling back to stale training data (e.g., suggesting `gemini-1.5-flash` when newer models exist).

### Mode 2: Feature Generation (The Builder)
- Implement features on existing codebase.
- Prompt agent to match existing style (naming patterns, error handling).
- Manually confirm changes when multiple files are being edited.
- See the **"Diff"** (exact lines added/removed) inside the editor.
- Tip: Variable renaming is acceptable but must be a *separate task*, not bundled with a bug fix.

### Mode 3: Bug Fixing (The Forensic Specialist)
- Root cause analysis + surgical repair.
- Shift from **Symptom Prompting** ("The button doesn't work") to **Evidence Prompting** ("Logs showed a 403 error").
- Use versioning on CLI (e.g., `gh` commands for Git) to compare code versions.
- Explain the flow: "Request hits Load Balancer → Auth strips header → Pod fails."
- **Always prompt for a failing unit test or curl command first** to reproduce the bug. Keep this test in the codebase permanently.
- Set strict constraint: agent should only fix the root cause. No unrelated "cleanup."
- E2E testing: Antigravity's built-in browser (isolated Chrome sandbox, no shared logins) can autonomously run localhost, interact with live UI, verify visual fixes in real time.

### Mode 4: Documentation Writing (The Author)
- In SDD, docs are the **source of truth** — if docs and code aren't in sync, AI will hallucinate.
- Specify in agent skills that `README.md` and `CHANGELOG.md` must always be maintained.
- Use **Google Style Docstrings** (Python) or **JSDoc** (TypeScript).

### Mode 5: Data Engineering (The Librarian)
- Use IDE extensions (e.g., Google Cloud Data Extension) to access cloud data directly.
- Prompt agent to always show the specific SQL query or command used to generate output.

---

## 5. MCP: One Integration, Every Framework

> "MCP was created by Anthropic and is now an open standard. People like to call it 'the USB-C for AI tools.'"

- Build one MCP server for a database/API/file system → any MCP-compatible agent can use it without a custom integration.

### Building an MCP Server (~40 lines, Python)

Key pattern from `mcp_server.py`:
- Import `mcp.server.Server`, `mcp.server.stdio.stdio_server`, `mcp.types.Tool, TextContent`.
- Decorate with `@server.list_tools()` and `@server.call_tool()`.
- Input validation: only allow `SELECT` queries for read tools.
- Run via `stdio_server` for local communication.

### Connecting an MCP Client

Key pattern from `mcp_client.py`:
- `StdioServerParameters(command="python", args=["mcp_server.py"])`.
- `async with stdio_client(...) as (read, write)` → `ClientSession` → `session.initialize()`.
- `session.list_tools()` to discover, `session.call_tool(name, args)` to execute.

---

## 6. Team Culture & Process Evolution

### Problems at High Velocity
- **Merge conflicts:** Multiple developers landing on the same file within the hour.
- **Review gridlock:** Massive PR becomes a Russian-doll of sub-PRs; cross-timezone blocking.
- **Context fragmentation:** Agent quotes outdated snapshot → calls a function that no longer exists.

### Code Review Strategies

1. **Bundled Summaries and Risk Assessments:** Every PR includes AI-generated snapshot of what changed, potential breakage points, and risk assessment. Human reviewers focus on architectural impact, not line-by-line.

2. **Reimagined Ownership:** Shift human reviews from style nitpicking (disposable AI code) to ensuring architectural blueprint integrity. Style → automated linters, SKILLS.md stylebooks.

3. **The "Conditional LGTM":** Reviewer approves contingent on all automated tests passing; if tests go green, code merges automatically. Eliminates 12-hour cross-timezone delays.

4. **No-Blame Culture:** Attribute bugs/merge conflicts to broken integration processes, not the individual developer using the agent.

5. **Agent Coding Reviews:** Build a skill that does the code review. Example `code-check.md` skill:
   ```
   gh pr view <PR NUMBER>
   ```
   Reviews for: Critical Vulnerabilities (hardcoded secrets, SQL injection, XSS), Logic & Efficiency (off-by-one errors, infinite loops), Readability, Edge Cases.
   Output: Description → ISSUES: Critical / Warnings / Best Practices / Quick Win — or LGTM.

### Three Tiers of Continuous Code Review

| Tier | Name | Example | Trade-off |
|------|------|---------|-----------|
| 1 | Managed | Gemini Code Assist on GitHub | Generic reviewer; misses domain-specific risks |
| 2 | Hybrid | GitHub Action + Antigravity CLI | Your review criteria; CI runtime; fast to set up |
| 3 | Custom | ADK agent on Agent Engine | Full context memory, multi-PR awareness; you own the runtime |

**Tier selection questions:**
1. How specific is your review criteria? Generic → Tier 1. Team/repo-specific → Tier 2 or 3.
2. Does the agent need to remember things across runs? No → Tier 1 or 2. Yes → Tier 3.
3. What's the worst case? Noisy comment → any tier. Merged regression or leaked secret → Tier 3 + Policy Server.

**Tier 3 at full scale (Graph-Native):** For 100M+ line codebases: knowledge graph (Spanner Graph), vector store, sub-agent pipeline (Search → Story → Impact → Task-breakdown → Coding agents). Moves equivalent refactor from two weeks to a few hours (Siemens case study).

### Sustainability / Approval Fatigue

> "According to Quantum Workplace research reported by CNBC, frequent AI users are **45% more likely to experience high burnout** than non-users."

Mitigations:
- **Digital Quiet Hours:** Approval requests do not bleed into evenings/weekends.
- **Agent Insight Sessions:** Weekly sessions where developers share patterns identified by AI counterparts — turns isolated discoveries into shared organizational knowledge.

---

## 7. Zero-Trust Development: Building the Safety Net

### The Incident That Explains Why This Matters

A simple prompt to create a button triggered a chain reaction: browser agent autonomously clicked the button → connected to a deprecated legacy agent with no email safeguards → **50 colleagues received false emails filled with hallucinated content**.

> "This highlighted **context hallucination risk**: when AI lacks sufficient data, it sometimes fills gaps using whatever strings exist in its context, including sensitive information like hardcoded email addresses or URLs."

Root cause: no human-in-the-loop or policy engine → agent optimized for its goal using whatever it could find. **Guardrails are not optional.**

### Implementing Guardrails

The paradox: agents must be autonomous enough to solve complex problems, but cannot go rogue in an enterprise environment.

> "Hard-coding constraints into a system prompt is brittle, contexts overflow, and agents can be 'convinced' to bypass rules via prompt injection. To build production-grade platforms, external, tamper-proof governance is required."

### Sandboxing

- Execute agent-driven tasks within **ephemeral, low-privilege containers** isolated from primary network and sensitive file systems.
- Creates a "blast radius" — damage confined to a disposable instance, wiped and reset without consequence.
- Antigravity: enable "Terminal Sandboxing" in User Settings.
- Team option: containerize agent workspace with a custom `Dockerfile` (e.g., `.gemini/sandbox.Dockerfile`) starting from official Gemini CLI sandbox image. Set `export GEMINI_SANDBOX=docker`.

### Human-in-the-Loop (HITL)

- Implement **checkpoint gates** for actions meeting a specific risk profile:
  - Deploying code to production
  - Modifying database schemas
  - Initiating financial transactions
- Present agent's sanitized intent to a human supervisor for manual sign-off.
- Ensures final responsibility for architectural integrity remains in human hands.

### AI-Generated Test Coverage

- In high-velocity environments, "test-driven development" becomes real by tasking the machine with writing the tests that validate its own output.
- Force the agent to produce a **failing unit test or reproduction command (curl)** before attempting any fix.
- Embed automated tests in codebase → every rapid iteration backed by verifiable suite of checks.

### Evaluation (vs. Testing)

> "Traditional software tests are insufficient for systems whose output is *generated* rather than *computed*. An agent can pass 100 unit tests on its tools and still fail spectacularly by choosing the wrong tool, paraphrasing a critical answer, or hallucinating a fact."

- **Unit test:** "Did the function return the right value?" — binary.
- **Evaluation:** "Is the agent's behavior at least as good as the baseline?" — scored judgment.
  - 0–5 score from an **LLM-as-judge**
  - **Trajectory check** that tolerates ordering variance in tool calls
  - Gate that fires when quality drops below a configurable margin (not when an assertion flips)
- Tests catch deterministic regressions; **evaluation catches behavioral drift**.

### Policy Server (Two Layers)

**Layer 1 — Structural Gating ("Traffic Lights"):**
- Deterministic rules based on roles and environments.
- Fast, binary checks (e.g., a `viewer` role cannot use `send_email` tool).
- Defined in `policies.yaml`:
  ```yaml
  environments:
    localhost:
      blocked_tools:
        - send_email
  roles:
    viewer:
      allowed_tools:
        - list_files
        - read_file
  ```

**Layer 2 — Semantic Gating ("The Intelligent Referee"):**
- Uses a secondary LLM (Gemini) to inspect *intent and content* of a proposed action against natural language privacy guidelines.
- Addresses: tool is allowed, but the *way* it's used violates a policy.
- Example: admin can use `send_email`, but should not send unmasked PII (plain-text email addresses or API keys). Regex cannot catch every possible PII leak.

**Execution flow (policy_server.py):**
1. **Structural Check:** Is the tool allowed for this role/env? (Check YAML)
2. **Semantic Check:** Are the arguments safe? (Ask Gemini — evaluate if action violates PII policies)
3. **Execution:** Both pass → tool runs. Otherwise → return "Policy Violation" to agent → self-correct or fail gracefully.

> "This creates a safety net that separates execution logic from governance logic — a critical separation of concerns for enterprise software."

### Context Hygiene & Prompt Sanitization

**Context Hallucination Risk:** When agent lacks specific data, it fills gaps using any available strings in its context — potentially leaking hardcoded email addresses or private URLs.

**Solution: Dynamic ContextResolver (`context_resolver.py`)**
- Regex-based translation utility.
- Replaces `[[VARIABLE_NAME]]` placeholder syntax with runtime overrides or environment config.
- Priority chain: (1) override_state dict → (2) os.environ → (3) leave unresolved (prevents silent failures).

**Integration (`tool_policy_engine.py`):**
- Wire ContextResolver into agent's execution pipeline as a validation step.
- Intercept incoming tool calls before they run.
- Resolve all args that are strings: `resolved_args[k] = resolve_context(v)`.
- Translates `[[COMMENTER_EMAIL]]` or `[[DEFAULT_PRESENTATION_ID]]` into authorized test assets safely — no hardcoded PII in test suites or system prompts.

---

## 8. Summary & Where to Start

> "AI has eliminated the code production bottleneck, moving the constraint downstream to humans who must review, test, and integrate that output. This is a shared cognitive load: humans act as architects writing Test Specs, Integration Specs, and MLOps/DevOps blueprints, while the AI handles the heavy lifting writing actual test code, performing integrations, and managing granular operational details."

**The real challenge:** Orchestrating systems that verify, integrate, and deploy work — not producing code.

**Getting started with google-agents-cli:**
```bash
uv google-agents-cli setup
```
Installs 7 skills covering scaffolding, ADK code, evaluation, deployment, publishing, observability.
- `agents-cli scaffold` → spec-driven project generation
- `agents-cli eval run` → AI-generated test coverage gate
- `agents-cli deploy` → sandboxed deployment to Cloud Run or Vertex AI Agent Engine

---

## Key Code Snippets Reference

| File | Purpose |
|------|---------|
| `mcp_server.py` | MCP server exposing SQLite DB as tools (40 lines) |
| `mcp_client.py` | MCP client connecting via stdio, discovering and calling tools |
| `code-check.md` | Agent skill for automated PR code review (security + logic) |
| `policies.yaml` | Deterministic role/environment gating rules |
| `policy_server.py` | Hybrid policy engine — structural + semantic gating |
| `context_resolver.py` | Regex placeholder resolver for context hygiene |
| `tool_policy_engine.py` | Middleware integrating ContextResolver into agent pipeline |

---

## Capstone Design Notes

### What to Build
1. **SDD Spec + BDD Scenarios for your agent** — demonstrate the spec-first workflow, show how Gherkin scenarios drive code generation.
2. **MCP server** wrapping a real data source (SQLite, API, file system) — shows "USB-C for AI tools" in practice.
3. **Tiered code review agent** — even Tier 2 (GitHub Action + agent CLI) demonstrates the continuous reviewer pattern.
4. **Policy Server** — implement structural + semantic gating to protect an agent from going rogue; show the email-incident prevention.
5. **Context Hygiene middleware** — implement the ContextResolver and wire it into an agent pipeline.
6. **Evaluation harness** — LLM-as-judge scoring showing behavioral drift detection (vs. binary unit tests).

### What to Demonstrate
- Spec stored in `specs/` folder drives code generation (not chat prompts alone).
- Gherkin BDD scenarios as executable contracts.
- Sandboxed agent execution with HITL checkpoint gate.
- Policy violation interception before tool execution.
- AI-generated failing test → fix → passing test cycle.
- Graders want to see: separation of governance from execution logic, evidence that guardrails actually intercept bad actions.

### What Graders Likely Reward
- Working MCP server with real tools (not toy).
- Policy Server that actually blocks a disallowed action and returns a meaningful error.
- BDD spec that genuinely drives agent behavior (not just decorative documentation).
- Evaluation metric (LLM-as-judge or trajectory check) comparing agent output to a baseline.
- Demonstrated HITL checkpoint that pauses execution for human approval.
- Knowledge of the three-tier code review spectrum and a working implementation of at least Tier 2.
