# The New SDLC With Vibe Coding: From Ad-Hoc Prompting to Agentic Engineering

**Authors:** Addy Osmani, Shubham Saboo, Sokratis Kartakis
**Course:** Kaggle AI Agents Intensive — Vibe Coding
**Date:** May 2026

---

## Introduction

> "The most profound shift in software engineering isn't a new language, framework, or cloud service. It's the transition from writing code to expressing intent, and trusting intelligent systems to translate that intent into working software."

As of early 2026:
- 85% of professional developers regularly use AI Coding Agents
- 51% use them daily
- ~41% of all new code is AI-generated

**The evolution arc:** Autocomplete → Inline suggestions → Chat-based interfaces → Fully autonomous agents (clone repo, plan, execute, test, PR — no human typing).

---

## 1. Key Definitions

### AI Agent (Quick Refresher)

> "An AI agent is a software system that perceives a goal, plans steps to reach it, takes actions through tools, observes the results, and iterates until the goal is met or it hits a stopping condition."

Five parts of every agent:
1. **Model** — the reasoning engine; reads context, decides next action
2. **Tools** — APIs, code execution, databases, other agents
3. **Memory** — state; short-term session logs + long-term persistent state
4. **Orchestration** — code that runs the loop; assembles context, dispatches tool calls, captures results
5. **Deployment** — hosting, identity, observability, production infrastructure

**The loop:** Get mission → Scan scene → Think → Act → Observe → Iterate

### Vibe Coding

Coined by Andrej Karpathy (February 2025):
> "Fully give in to the vibes, embrace exponentials, and forget that the code even exists."

In practice: describe in natural language → accept AI output → copy errors back to prompt → repeat. Went viral because many developers were already working this way. By 2026 Karpathy introduced "agentic engineering" as the disciplined counterpart.

### Agentic Engineering

The disciplined end of the spectrum: AI acts as a powerful implementation engine within carefully designed systems of constraints, tests, and feedback loops, with humans retaining oversight over architecture, correctness, and quality.

---

## 2. The Spectrum: Vibe Coding to Agentic Engineering

The key differentiator is **not** whether you use AI — it's how much structure, verification, and human judgment surrounds the AI's output.

| Dimension | Vibe Coding | Structured AI-Assisted | Agentic Engineering |
|---|---|---|---|
| Intent specification | Casual natural language prompts | Detailed prompts with examples and constraints | Formal specs, architecture docs, memory files |
| Verification | "Does it seem to work?" | Manual testing, spot-checking | Automated test suites, CI/CD gates, LM judges |
| Codebase understanding | Minimal; developer may not read generated code | Selective review of critical paths | Comprehensive review of architecture; AI handles implementation details |
| Error handling | Copy-paste error messages back to AI | Developer diagnoses root cause, AI implements fix | Agents self-diagnose within defined bounds; humans handle architectural issues |
| Appropriate scope | Prototypes, scripts, personal projects, hackathons | Features within established codebases | Production systems, team-scale development |
| Risk profile | High; acceptable for disposable code | Moderate; human judgment at key checkpoints | Low; systematic verification at every stage |

**Applied Tip:** The right position depends on stakes. A weekend prototype can be pure vibe coding. A production API handling financial transactions demands agentic engineering.

### Verification: Tests vs. Evals (the critical distinction)

> "The single biggest differentiator between the two ends is how outputs get verified."

- **Tests** — verify deterministic parts: function given this input → that output. Checked by code.
- **Evaluations (evals)** — verify non-deterministic parts: did the agent take the right trajectory of steps, choose the right tools, produce a response that meets quality bar? Checked by labeled datasets, scoring rubrics, and LM judges.

> "Without both, the practice is always vibe coding, regardless of how sophisticated the prompts are."

Two eval types:
- **Output evaluation** — checks the final artifact (does the code compile, do tests pass?)
- **Trajectory evaluation** — checks the full sequence of tool calls and intermediate reasoning

> "A fluent output that skipped its verification steps is a more dangerous failure than one with a visible error."

---

## 3. Context Engineering: The Real Skill

> "The quality of AI-generated code depends less on the cleverness of your prompts and more on the quality of the context provided."

> "The shift from 'prompt engineering' to 'context engineering' reflects a deeper truth about working with AI. Models don't need cleverly worded instructions as much as they need the same context that a skilled human developer would need to do good work."

### Six Types of Context

1. **Instructions** — the agent's core role, goals, and operational boundaries
2. **Knowledge** — retrieved documents, architectural diagrams, domain-specific data
3. **Memory** — short-term session logs (what just happened) + long-term persistent state (what the project is)
4. **Examples** — few-shot behavioral demonstrations and codebase reference patterns
5. **Tools** — precise definitions of APIs, scripts, and external services the agent can invoke
6. **Guardrails** — hard constraints, formatting rules, and safety validations

### Static vs. Dynamic Context

**Static context** — always loaded: system instructions, rule files (AGENTS.md, CLAUDE.md, GEMINI.md), global memory, persona definitions. Defines who the agent is and how it behaves. Expensive: every token present in every interaction regardless of relevance.

**Dynamic context** — loaded on demand: skill instructions triggered by task matching, tool results retrieved during execution, documents fetched from RAG pipelines, windowed session history. Efficient: pays token cost only when needed.

> "The design decision of what belongs in static context versus dynamic context is a genuine engineering trade-off. Too much static context wastes tokens and dilutes signals. Too little means the agent forgets critical rules."

### Agent Skills

> "The most powerful pattern for managing dynamic context is Agent Skills: structured, portable packages of procedural knowledge that the agent loads only when the task calls for it."

Progressive disclosure model:
- Agent sees lightweight metadata at startup
- Loads full instructions when a task matches
- Pulls deep reference material only when explicitly needed
- Pays token cost only for the one actively being used

Four problems Agent Skills solve:
1. Context rot from overloaded prompts
2. Absence of procedural memory for LLMs
3. Operational overhead of multi-agent architectures
4. Need for portability across tools and vendors

---

## 4. The New SDLC

### Traditional SDLC Under Pressure

> "AI compresses this cycle dramatically, but unevenly: implementation that once took weeks can now be done in hours, while requirements, architecture, and verification remain stubbornly human-paced."

Result: not a faster version of the old SDLC — a *different* workflow where boundaries between phases blur, iteration cycles shorten from weeks to minutes, and the developer shifts from primary implementor to system designer and quality arbiter.

### How AI Transforms Each Phase

#### Requirements and Planning
- AI generates user stories from product briefs
- Identifies edge cases humans miss
- Produces API schemas from natural-language descriptions
- Generates interactive prototypes from specs
- Requirements become a *conversation* that produces spec and initial implementation simultaneously

#### Design and Architecture
- Architecture remains most human-centric phase — trade-offs depend on business context, org constraints, long-term strategy that AI cannot fully grasp
- AI excels at *implementing* architectural decisions once made
- Developer role shifts from writing boilerplate to making and documenting structural decisions

#### Implementation
- Industry surveys: 25-39% productivity improvements
- METR study: experienced developers using AI assistants took **19% longer** on certain tasks (time spent verifying, debugging, correcting AI output)
- > "AI does not eliminate implementation work so much as transform it from writing to reviewing, guiding, and verifying."

#### Testing and QA
- AI produces test cases including edge cases and property-based tests humans might miss
- **Quality flywheel:** evaluate against benchmark → diagnose failures by clustering root causes → optimize prompts/tools → verify fixes against regression suite → monitor production for new failure modes → repeat
- Tests and evals become the primary mechanism for *communicating intent* to AI agents

#### Code Review and Deployment
- AI serves as first-pass reviewer: bugs, style violations, security vulnerabilities, performance issues
- Human review still required for context-dependent design, maintainability, strategic alignment
- Deployment pipelines: AI monitors health, auto-rolls back problematic releases, predicts deployment risks

#### Maintenance and Evolution
- Legacy codebases once impenetrable can now be navigated with AI
- Technical debt that was "too risky to touch" can now be safely refactored
- AI agents can systematically migrate codebases, update deprecated APIs, modernize test suites

---

## 5. The Factory Model

> "In this model, the developer's primary output is not code — it's the system that produces code."

The factory model includes:
- Specifications and context defining what needs to be built
- Agents that translate specifications into implementation
- Tests and quality gates that verify correctness
- Feedback loops that route failures back to agents for correction
- Guardrails that constrain agents to safe, predictable behavior

> "A factory manager does not assemble every widget by hand. They design the assembly line and ensure quality control. The modern developer designs the development system and ensures that its output meets the required standard."

> "Success comes from giving agents success criteria rather than step-by-step instructions, then letting them iterate."

---

## 6. Harness Engineering

> "The model is one input into a running agent. Everything else — the prompts, the tools, the context policies, the hooks, the sandboxes, the sub-agents, the observability — is the harness."

**Key equation:**

```
Agent = Model + Harness
```

A raw model is not an agent. It becomes one once a harness gives it state, tool execution, feedback loops, and enforceable constraints.

> "The behaviour developers experience when working with Claude Code, Cursor, Codex, Antigravity, Aider, or Cline is dominated by what the harness does, not just by which model is underneath."

### What's in the Harness

1. **Instructions and Rule Files** — AGENTS.md, CLAUDE.md, GEMINI.md, skill files, sub-agent prompts
2. **Tools** — functions, MCP servers, APIs + prose that tells model when/how to call them
3. **Sandboxes and execution environments** — where agent code runs, what it has access to
4. **Orchestration logic** — sub-agent spawning, model routing, hand-offs between specialists
5. **Guardrails/Hooks** — deterministic code that runs at specific lifecycle points (before tool call, after file edit, before commit)
6. **Observability** — logs, traces, evaluations, cost and latency metering

> "If that sounds like a lot of surface area, it is. And it is the team's surface area, not the model provider's."

### Harness Across the SDLC

**Phase 1 — Requirements, Planning & Architecture (Configuring the Harness):**
- Create AGENTS.md, define architectural constraints
- Define tools the agent will have access to
- Set fundamental rules the agent cannot break

**Phase 2 — Implementation (Running the Harness):**
- Sandboxes and execution environments active
- Model generates code, executes within isolated sandbox
- Tool calls mediated by harness

**Phase 3 — Testing & QA (The Feedback Loop):**
- Orchestration logic + Guardrails used
- Harness captures test failure output, routes back to model for retry
- Creates automated think → act → observe loop

**Phase 4 — Code Review, Deployment & Maintenance (Observing the Harness):**
- Hooks + Observability used
- Deterministic hooks block unsafe actions (e.g., hard-coded password in commit)
- Observability layer tracks token costs, latency, agent drift

### The Harness Effect (Concrete Data)

- Terminal Bench 2.0: one team moved a coding agent from **outside Top 30 to Top 5** by changing only the harness — no model change
- LangChain study: raised coding agent score by **13.7 points** by tweaking only system prompt, tools, and middleware around a fixed model

> "Most agent failures, examined honestly, are configuration failures."

> "The transition from 'vibe coding' to 'agentic engineering' is not simply about the tools you use — a developer can vibe code or apply agentic engineering using the exact same agent. Instead, it is defined by how deliberately you configure and apply the harness."

---

## 7. Developer Roles: Conductor and Orchestrator

### The Conductor (hands-on, real-time direction)
- Works in real-time with AI pair-programmer in IDE
- Watches code appear, guides with prompts and corrections
- Maintains fine-grained control over what gets written
- Tools: GitHub Copilot, Gemini Code Assist, Cursor, Windsurf
- Risk: can become a bottleneck — if developer directs every keystroke, throughput improvement is limited

### The Orchestrator (async, multi-agent delegation)
- Operates at higher level of abstraction
- Defines goals, assigns to agents, reviews results — not watching line by line
- Agents may work in background, in parallel, on different codebase parts
- Tools: Google Jules, GitHub Copilot agent mode, Cursor's background agents, Claude Code
- Requires different skill set:
  - **Specification** — defining tasks precisely enough for agent execution without ambiguity
  - **Decomposition** — breaking large tasks into appropriately sized units for agents
  - **Evaluation** — quickly assessing whether agent output meets quality standards
  - **System design** — designing constraints, tests, and feedback loops that keep agents productive

---

## 8. The 80% Problem

> "AI agents can rapidly generate approximately 80% of the code for a feature, but the remaining 20% — the edge cases, error handling, integration points, and subtle correctness requirements — demands deep contextual knowledge that current models often lack."

Nature of AI errors has evolved: from simple syntax mistakes to more insidious conceptual failures:
- Wrong assumptions about business logic
- Failure to seek clarification on ambiguous requirements
- Missing edge cases
- Architectural decisions that create subtle long-term maintenance burdens

> "The developers who navigate this challenge most effectively adopt a specific posture: they use AI for what it's good at (rapid implementation of well-specified tasks) while reserving their own attention for what AI struggles with (ambiguous requirements, architectural trade-offs, and correctness verification)."

---

## 9. Coding Agents in Practice: Three Deployment Contexts

### In the Editor
- Inline completion, chat panels, whole-codebase awareness inside IDE
- Examples: GitHub Copilot, Cursor, Windsurf, JetBrains AI Assistant
- Best for: staying in flow while coding

### In the Terminal
- Agent launched from command line, handed a goal in plain language, works across codebase
- Full filesystem access, multi-file edits, runs tools/tests, iterates
- Examples: Antigravity CLI, Claude Code, Codex CLI, Open Code, Cline
- Best for: multi-file work, exploring unfamiliar codebases, tasks requiring code execution + observation

### In the Background
- Agents run autonomously in cloud-hosted sandboxes, often hours, produce PR as output
- Examples: Google Jules, GitHub Copilot agent mode, Cursor's background agents, Google AlphaEvolve
- Best for: well-specified tasks developer can walk away from (fix known bug, generate test suite, migrate framework)

---

## 10. Building Production-Ready Agents

### The Google Agents CLI Workflow

Seven skills covering the full ADK lifecycle:
- Scaffold a project
- Write the agent code
- Evaluate it
- Deploy to Agent Runtime
- Wire up observability

```bash
# One-time setup
uvx google-agents-cli setup

# Then in your coding agent:
> Build a support agent that answers questions from our docs.
> evaluate it on the FAQ dataset
> Deploy it to Agent Engine
```

Behind that single instruction: scaffold project → write ADK code → generate evalset → run it → deploy → report back.

### Multi-Agent Coordination Protocols
- **Shared session state** — for simple inter-agent coordination
- **Model Context Protocol (MCP)** — for tool access across agents
- **Agent2Agent (A2A) Protocol** — for cross-agent delegation

Anthropic experiment (early 2026): agent teams built a working C compiler in Rust over two weeks, with humans setting direction and reviewing output but not writing implementation.

> "The bottleneck moved from writing the code to specifying what it should do and verifying that the agents did it."

---

## 11. Economics of AI Development

### CapEx vs. OpEx Frame

**Vibe Coding (Low CapEx, High OpEx):**
- Near-zero upfront investment (just a subscription)
- Hidden compounding OpEx:
  - **Token burn rate** — unstructured context dumps + repeated prompting loops burn tokens with low first-pass success
  - **Maintenance tax** — ad-hoc code lacks structural consistency; 6 months later debugging unstructured "spaghetti" code costs days
  - **Security remediation** — fixing production security flaw costs exponentially more than catching at design phase

**Agentic Engineering (High CapEx, Low OpEx):**
- Deliberate upfront investment: design API schemas, build deterministic test suites, structure agent context
- Marginal cost of shipping and maintaining a feature drops dramatically
- AI operates within governed "factory" — output structurally sound, pre-tested, aligned with standards

### Context Engineering as a Financial Lever

> "In the token economy, context engineering is not just a technical skill — it is a financial strategy."

- Passing a full 100,000-token repository into every prompt is financially unviable at scale
- Effective context engineering: dense, high-signal payload (precise AGENTS.md + architectural guardrails) vs. sprawling noisy one
- Higher first-pass success rate → avoids costly trial-and-error loops

### Intelligent Model Routing

- Vibe coding: single frontier model for every interaction (expensive)
- Agentic engineering: route by task complexity
  - **Large models** → complex tasks: Requirements, Architecture, initial Implementation
  - **Smaller/cheaper models** → deterministic lower-complexity tasks: Test Generation, Code Review, CI/CD monitoring

---

## 12. Where to Start: Actionable Recommendations

### For Individual Developers

1. **Set up AGENTS.md** — start with 10 lines: stack, conventions, hard rules, workflow. Add a rule every time the agent does something it should not do again.
2. **Install skills for coding agents** (e.g., Agents CLI) to build, evaluate, deploy, optimize agents.
3. **Pick one repetitive workflow** and make it the first agent. Graduate it to production via Agents CLI when it earns its keep.
4. **Write tests and evals before generating code.** Together they are the contract with the AI. A well-written test and eval suite communicates intent more precisely than any natural-language prompt.
5. **Review every line the agent produces that is going to ship.** Be skeptical of anything that looks clever. Check imports for real packages. Verify error handling covers realistic failure modes.
6. **Maintain developer skills.** Treat AI as a way to apply expertise at greater scale, not as a substitute for it.

### For Engineering Leaders

1. **Make context engineering a first-class engineering practice.** Treat AGENTS.md, system prompts, eval suites, and skill libraries as code: reviewed in PRs, versioned, owned by named engineers.
2. **Set the bar at the eval, not the demo.** Define what you are scoring: task success, tool use quality, trajectory compliance, hallucination, response quality. Require eval coverage with explicit rubrics as a precondition for any agent shipping.
3. **Re-shape code review for AI-generated code.** Extra attention to: hallucinated dependencies, inadequate error handling, subtle correctness gaps that look right at a glance.
4. **Distinguish prototyping work from production work in team norms.** Make the boundary explicit. Teams that keep this blurry produce prototypes that ship by accident.
5. **Invest in harness components as a shared team asset.** Reusable system prompts, skill libraries, MCP server connections, and evaluation harnesses compound across projects.

### For Organizations

1. Treat AI-assisted development as an engineering investment, not a productivity feature.
2. Build the production substrate (evals in CI, traces, scoped permissions, security review) before the first production agent ships, not after.
3. Adopt MCP for tool access and A2A for cross-agent delegation — open standards that prevent re-platforming.
4. Plan for hybrid teams of humans and agents. Humans set direction, agents do implementation, clear handoff protocols govern the boundary.
5. Reframe hiring and skill development around judgment, not just implementation. Most valuable engineers: those who can direct agents well, not those who write the most code.

---

## 13. Three Durable Principles (Conclusion)

1. **"Structure scales, vibes don't."** For software organizations depend on, the discipline of agentic engineering is not optional. The gap between "it seems to work" and "it works correctly under all conditions" is where production outages, security vulnerabilities, and maintenance nightmares live.

2. **"AI amplifies your engineering culture."** Organizations with strong testing practices, clear architectural standards, and healthy code review processes get dramatically more value from AI-assisted development. AI is a force multiplier — it multiplies both strengths and weaknesses.

3. **"The human role is evolving, not diminishing."** Builders who understand architecture, define precise specifications, evaluate output critically, and design effective systems of constraints and feedback loops are more valuable than ever. Skills that matter are shifting from implementation to judgment.

> "Generation is solved. Verification, judgment, and direction are the new craft."

---

## Capstone Hooks

### Build / Demonstrate Opportunities

1. **Harness Engineering Demo** — build the same agent twice: once with minimal harness (vibe coding style), once with full harness (AGENTS.md, tools, guardrails, hooks, observability). Measure and compare: first-pass success rate, token cost, error rate, quality. Directly demonstrates the paper's central thesis.

2. **Context Engineering Optimization** — take a real coding task; run it with progressively better context engineering (no context → full static context → static + dynamic + skills). Track token cost, first-pass success rate, output quality across configurations.

3. **The Quality Flywheel** — implement the paper's continuous quality loop: benchmark eval → root cause clustering → prompt/tool optimization → regression verification → production monitoring. Show the loop compounding over multiple iterations.

4. **Eval Suite as Spec** — write the full eval suite (output evals + trajectory evals) BEFORE generating any code. Let the eval suite drive the agentic engineering workflow. Demonstrates tests-and-evals-as-contract pattern.

5. **Model Routing Factory** — implement intelligent model routing for a multi-step agent pipeline: large model for requirements/architecture, smaller models for test gen and CI/CD tasks. Measure TCO reduction vs. single-model approach.

6. **Agent Skills Library** — build a portable Agent Skills system with metadata-first progressive disclosure. Show how a generalist agent flexes into specialist roles on demand without paying full context cost upfront.

7. **Conductor-to-Orchestrator Case Study** — document the same feature built in conductor mode (IDE, line-by-line) vs. orchestrator mode (background agent with specs). Compare velocity, quality, cognitive load.

8. **Production Agent via Agents CLI** — use Google Agents CLI to take a prototype terminal script through the full lifecycle: scaffold → code → eval on a dataset → deploy → observe. Show prototype-to-production collapse in one workflow.

9. **CapEx vs. OpEx Measurement** — run the same development workflow under vibe coding and agentic engineering; measure token burn, time to fix bugs, code review rounds needed, test coverage. Produce an economics comparison.

10. **AGENTS.md Iteration Experiment** — start with a 10-line AGENTS.md, run an agent on a task, log failures, add rules, rerun. Show measurable improvement as the harness grows. Demonstrates "most agent failures are configuration failures."

---

## Key Stats and Benchmarks to Reference

- 85% professional devs use AI coding agents (early 2026)
- 41% of all new code is AI-generated
- 25-39% productivity improvement (industry surveys)
- METR study: experienced devs took **19% longer** with AI due to verification overhead
- Terminal Bench 2.0: harness-only change moved agent from **outside Top 30 → Top 5**
- LangChain: **+13.7 points** on benchmark from harness tuning alone, no model change
- Anthropic: agent team built C compiler in Rust over 2 weeks, humans only set direction + reviewed
