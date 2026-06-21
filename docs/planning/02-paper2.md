# Agent Skills — Whitepaper Summary
**Authors:** Tanvi Singhal, Gabriela Hernandez Larios, Debanshu Dus, Lavi Nigam, Smitha Kolan  
**Published:** May 2026 (Kaggle AI Agents: Intensive — Vibe Coding course)  
**Source:** Kaggle / Google Drive (course material)

---

## 1. Introduction — What Problem Do Agent Skills Solve?

> "Agent Skills turn any general-purpose agent into a specialist on demand. No context bloat. Portable and lightweight."

Four friction points Agent Skills address:

1. **Context rot** — Dumping every instruction into a single system prompt degrades LLM performance; Skills load exclusively on demand.
2. **Procedural memory gap** — LLMs have episodic memory (what happened) and semantic memory (facts) but lacked a credible primitive for *how* to do things step-by-step. "Agent Skills can be seen as the first credible procedural memory primitive for LLM Agents."
3. **Multi-agent overload** — Complex multi-agent systems are hard to build and maintain; a single general-purpose agent with a library of skills can flex into many specialist roles.
4. **Portability** — A folder with a markdown file is "a remarkably lightweight primitive. Any agent with filesystem access can use them."

---

## 2. What Is an Agent Skill?

> "Agent Skills are a primitive for giving a general-purpose agent on-demand specialist competence."

**Definition:** A Skill is a folder containing a `SKILL.md` file (required) plus optional `scripts/`, `references/`, and `assets/` subdirectories.

### Skill Anatomy & Folder Structure

```
skill_name/
├── SKILL.md          # Required: YAML frontmatter + markdown instructions
├── scripts/          # Optional: executable helper scripts (Python, Bash)
├── references/       # Optional: supplementary context loaded as needed
├── assets/           # Optional: templates, configs, schemas
└── ...               # Any additional files
```

**Progressive Disclosure** — Skills load in three levels:
1. **Metadata** (name + description) — always in the agent's context (tiny: ~30-80 tokens each)
2. **SKILL.md body** — loaded only when the skill triggers
3. **Bundled resources** — loaded strictly as needed; scripts execute without polluting the token window

This allows 100 installed skills to cost only ~100 × 50 tokens = ~5,000 tokens of always-loaded metadata.

### YAML Frontmatter (the activation trigger)

```yaml
---
name: cafe-preparation
description: |
  Calculates daily ingredient needs and generates prep sheets for cafe operations.
  Use when the user asks to estimate daily quantities, convert drinks to ingredients,
  or generate shopping lists.
  Do NOT use for employee shift scheduling or financial accounting.
version: 1.0.0
license: MIT
allowed-tools: [Optional] Read Bash Write
metadata:
  author: [Optional] your-handle
---
```

**The description field is the routing algorithm** — the only thing the model sees when deciding whether to load the skill.

### Two Creation Paths

**Path A: Translating what you already know**
- Subject matter experts with existing runbooks, guides, procedures
- Translate institutional knowledge into SKILL.md format
- No coding required

**Path B: Crystallizing what the agent just did**
- Watch agent execute a successful, reusable workflow
- Agent proposes a SKILL.md draft from the trace (meta-skills territory)
- Human reviews instead of authors

---

## 3. How to Install Skills

Three paradigms:

1. **File Drop (Coding Agents & CLIs):** Drop skill folder into a hidden directory (`.agents/skills/` is emerging convention). Tools like `skillport` or `openskills` symlink across multiple tool locations.
2. **UI Install (Web & Enterprise):** Visual registry in web platforms for team-wide installation.
3. **Programmatic Route (Custom Frameworks):** Register via `SkillToolset` class in frameworks like Google ADK; auto-generates `load_skill` routing tools.

---

## 4. Skill vs. MCP vs. AGENTS.md

> **One-line mental model:** "System prompt = instinct. AGENTS.md = project README. Tools / MCP = hands. RAG = library. Skills = the runbook the experienced colleague hands you on day one, and that the AI never forgets."

| Primitive | Purpose |
|---|---|
| Skills | **Know-how** — teaches the agent how to think about a particular kind of work |
| MCP | **Reach** — connects the agent to external systems (Drive, Salesforce, BigQuery, internal APIs) |
| AGENTS.md | **Always-loaded project context** — project conventions, stack, build commands |

- Skills and MCP **compose**, not compete: a skill tells the agent to call MCP tools for data.
- AGENTS.md stays tight; use it as a router into the skill library (short catalog at the bottom).

---

## 5. Why Skills Beat Multi-Agent (Often)

Skills do NOT kill multi-agent. Multi-agent remains right when there is:
- Genuine parallelism
- Real capability boundaries (different access, security postures, external systems)
- Hierarchical decomposition where abstraction layers actually differ
- Adversarial / check-and-balance setups
- Sub-agent intercommunication
- Heterogeneous models

**Logistics example with 100 process variants:**
- One giant context: context rot + exorbitant cost
- RAG over runbooks: vector DB + embedding model overhead, quality depends on chunking
- Multi-agent (100 subagents): 100 deployments, 100 eval surfaces, complex routing
- **One agent + 100 skills:** ~5,000 tokens of always-loaded metadata; procedures in version control; adding variant 101 = new folder, not new deployment

---

## 6. Evaluating Skills

> "An Agent Skill without a test is a hope, not a capability."

**SkillsBench (2025) finding:** 19% of skills performed *worse* than no skill. Poorly designed skills actively degrade capability.

### Four Failure Modes

| Mode | When it appears |
|---|---|
| **Trigger Failure** | Wrong skill fires, or correct one fails to fire |
| **Execution Failure** | Skill triggers correctly but produces incorrect output or errant tool calls |
| **Token Budget Failure** | Massive skill body crowds context window, degrading unrelated turns |
| **Regression** | Newly added skill overlaps with existing one, breaking previously working routing |

Trigger/execution failures = single-turn level; Token budget/regression failures = appear only under production multi-skill load.

### The Evaluation Toolkit (5 Patterns)

| Pattern | Description | Failure Mode Addressed | When Required |
|---|---|---|---|
| **Eval-as-Unit-Test** | Test file for skill running in CI on every change | All | Every skill, every change |
| **Golden Dataset** | Curated (input, expected output) pairs versioned with the skill | Execution, Trigger | Draft tier and above |
| **LLM-as-Judge** | Peer model evaluates output against rubric at scale | Execution | Read-only and draft |
| **Adversarial / Red-Team** | Systematic probing to expose failure modes | Trigger, Execution | Before action-allowed graduation |
| **Canary / Shadow Mode** | Deploy to controlled traffic before full rollout (Shadow: offline parallel; Canary: 1% live for 24h) | Regression | Before each action-allowed release |

### Trigger Accuracy

- **Industry standard: 90% trigger accuracy rate**
- Vercel production analysis found 56% non-invocation rate for expected-to-fire skills
- A skill stripped of instructions scored 58%; agent without skill scored 63% — a 5-point deficit showing poorly designed skills subtract capability
- AGENTS.md passive index achieved 100% pass rate vs. 53% baseline → skills best for narrow, action-specific workflows

**Four checks for 90% trigger accuracy:**
1. **Testable specificity:** Write 3 positive AND 3 negative triggers
2. **Clarity:** Ambiguous queries don't overlap with adjacent skills
3. **Execution fidelity:** Describes actual performance, not aspirational behavior
4. **Rephrasing stability:** Routes consistently regardless of how user phrases intent

### Evaluation-Driven Development (EDD)

Write three JSON evaluation cases (Input, Expected Tools, Expected Output) **before** drafting the SKILL.md:

```json
{
  "case_id": "refund_dup_charge_001",
  "input": "I was charged twice for order #4521 last Tuesday",
  "expected_skill": "refund_processor",
  "expected_tool_calls": [
    {"tool": "lookup_order", "args": {"order_id": "4521"}},
    {"tool": "check_duplicate_charge", "args": {"order_id": "4521"}}
  ],
  "expected_output_format": "confirmation_with_refund_id",
  "rubric": ["acknowledges duplicate", "cites order id", "provides next step"]
}
```

### Output Quality and Tool Trajectory

- Test **final output** (what agent says) AND **tool trajectory** (what agent does) separately
- Latitude analysis (March 2026): Final-output-only scoring passes 20-40% more cases than trajectory-aware scoring — those "false passes" are instances where agent reached correct answer via incorrect tool sequence
- In action-allowed skills, incorrect tool trajectories can cause irreversible side effects
- Google ADK eval trajectory modes: `EXACT`, `IN_ORDER`, `ANY_ORDER`
  - Read-only → `ANY_ORDER`; Action-allowed → `IN_ORDER` or `EXACT`

**LLM-as-Judge non-negotiables:**
1. Swap positions of reference and actual output to eliminate ordering bias
2. Calibrate against human ratings until 90% agreement

### Skill Authority Tiers

- **Read-Only:** LLM-as-Judge eval; 90% trigger accuracy
- **Draft-Only (Human Review):** Golden dataset of 20+ cases; human approval
- **Action-Allowed:** Full adversarial red-teaming; `pass^k` (success on every run of k runs); no rollback events

**pass^k:** GPT-4o scored 61% on pass^1 but dropped below 25% on pass^8 — single-run success is a poor predictor of production reliability.

**Production calibration factors:**
- ReliabilityBench: production performance drops 20-30% vs. offline benchmark pass@1
- "Lost in Simulation" finding: simulation-based evals have up to 9% optimistic bias

### Eval Coverage Checklist (4 conditions for "evaluated")

- ☐ **Trigger:** Positive AND negative test cases; 90% trigger accuracy
- ☐ **Execution:** Correct outputs across representative range of inputs
- ☐ **Regression:** Adding this skill causes zero drops in existing library suite
- ☐ **Token budget:** Co-loaded with 5-15 frequently-active skills, does not degrade unrelated turns

Failure on ANY single condition holds the skill at draft tier.

### System vs. Skill: The Evaluation Illusion

Use "Single-Skill Sub-Agent pattern" (Agent + 1 Skill vs. Base Agent) for calibration. Multi-skill co-loading only for advanced production staging.

**Two-Tiered Assert Framework:** Validate underlying tool code independently; audit `SKILL.md` triggers across multiple model families to catch brittle, architecture-locked descriptions.

---

## 7. Token Budget — Context Rot in Production

### The Research Foundation

- **"Lost in the Middle" (Liu et al., TACL 2024):** Performance highest when relevant info is at start or end of input; degrades in the middle — a U-curve that holds even for long-context models.
- **Context Rot (Chroma Research, 2025):** Across 18 frontier models (Claude 4 Opus/Sonnet, Gemini 2.5, Qwen3), performance degrades as input grows even when task difficulty is held constant. Every model gets worse, faster when relevant content is hard to distinguish from distractors.
- **MCPVerse:** 18.2% accuracy drop in Claude-4-Sonnet due to tool proliferation and context attention competition.

**Critical insight:** "Capacity is the wrong metric. A 1M-token window can show significant degradation at 50K tokens."

### Token Math Example

- 50 workflows as a single system prompt: **15,000 tokens every turn**
- 50 workflows as a skills library: **~4,000 tokens of descriptions + ~2,000-token body of one active skill = ~6,000 tokens total**
- Anthropic example: converting a workflow to skills cut active context from ~150,000 tokens to 2,000 — **>98% reduction**

**"Active context is a budget, not a vessel. Every token in front of the model takes attention from every other."**

Never evaluate a skill in isolation — agents in production co-load 5-15 skills simultaneously. A skill body exceeding **5,000 tokens** might work alone but cause context rot when co-loaded.

---

## 8. From Prototype to Production

### The Architecture Insight

Claude Code v2.1.88 reverse-engineering (Liu et al., 2026): 98.4% of codebase is operational infrastructure; only 1.6% is the agent loop itself. "As foundation models converge in baseline reasoning, the differentiator for autonomous reliability becomes the deterministic engineering around the model."

### Skills as the Unit of Improvement

**Comparison of improvement methodologies:**

| Style | Cycle Time | Failure Mode | Who Can Do It | Context Tax |
|---|---|---|---|---|
| Model swap | Days to weeks | Regression in unrelated tasks | ML/platform team | None (weights-based) |
| System prompt edit | Minutes to hours | Context rot, instruction conflict | Whoever owns prompt | Static (every turn pays) |
| Fine-tune | Weeks to months | Catastrophic forgetting, overfitting | ML team only | None (weights-based) |
| **New skill** | **Hours to days** | **Bounded with only matching turns** | **Any domain team** | **Dynamic (on-demand)** |

Three properties that make skills the right improvement unit:
- **Conditional:** Loaded only when description matches task
- **Composable:** One skill can call tools from another without either knowing about the other
- **Owned:** Each lives in a versioned folder with a clear author

### Google Agents CLI Example

Seven skills shipped as a single skills package covering the full agent lifecycle:
- Scaffold → Build → Evaluate → Deploy → Publish → Observe

"The expertise lives in the skills, not the runtime. The runtime is commoditized; the seven skills are the durable asset."

---

## 9. Meta-Skills and Self-Improving Skills

Skills whose job is to author, evaluate, or improve other skills. Four buckets:

1. **Authoring** — Takes a description of a workflow and produces a SKILL.md draft (Google ADK "skill factory" pattern; Anthropic `skill-creator` skill)
2. **Assisted authoring from traces** — Watch agent succeed → turn trace into skill; human reviews instead of authors
3. **Improvement** — Takes existing skill + failing eval cases, proposes edits (SkillOptimizer by Saboo; Karpathy's `autoresearch` pattern: propose → experiment → keep if metric improves)
4. **Library evolution** — Agent notices it solved a recurring problem → proposes adding a new skill (like Voyager's Minecraft skill library growth)

### Where This Falls Apart

- Meta-skills only work if your evaluation suite is good
- An agent optimizing its own skills will optimize for whatever metric you point at — including gaming easy metrics
- Without solid trigger accuracy tests, regression tests, and human spot-checks, an autonomous improvement loop "will quietly make your library worse while reporting that it's getting better"

**Safe habits:**
- Anything an agent writes enters library at **draft tier** regardless of meta-skill confidence
- Keep human in the loop for first few edits — even when metric clearly improves
- Don't start with meta-skills; get manual authoring loop working first

---

## 10. Composing and Packaging Skills

### DAG Orchestration

Early prompt-chaining proved brittle. Industry solution: **Directed Acyclic Graph (DAG) orchestration**.

- **Decoupled State:** State routing does NOT rely on accumulating execution history within LLM's prompt
- **File Message Bus:** DAG controller orchestrates handoffs by passing structured schema references between subagent nodes
- **Protected Attention:** Abstracting payload from model's text input prevents context bloat

### Capability Profiles

"Modular tool bundle" defining:
- Active skills and tool access
- System instructions and operational guardrails
- Automated workflows and subagent topologies
- LLM parameters (model choice, temperature)

During execution: strict teardown (flush previous instructions + stale variables) then rebuild with new profile → prevents context contamination.

### Canonical Skill Taxonomy (DAG Node Types)

| Node Type | Function |
|---|---|
| **Generator** | Convert user intent into structured artifacts |
| **Reviewer & Gate** | Deterministic gates blocking execution if validation fails |
| **Pipeline** | Orchestrate linear paths within broader DAG |
| **Inversion & Recovery** | Force agent to clarify assumptions before execution |
| **Domain Context Wrappers** | Reference nodes teaching domain conventions |

### Context Debt and Shifting Intelligence Left

**Context Debt:** Authors attempting deterministic behavior via bloated skill descriptions ("ALWAYS DO X"). Models learn to ignore capitalized imperatives the same way humans ignore walls of warning text.

**Shift Intelligence Left:** Push logic out of LLM's prompt into standard, testable scripts. "Instead of hoping an LLM correctly interprets complex rules at runtime, distill subjective judgments into skills."

### Architectural Tradeoffs

| Architecture | Mechanism | Primary Benefit | Best For |
|---|---|---|---|
| Linear Pipelines | Sequential text passing between fixed nodes | Low engineering overhead; rapid prototyping | Single-domain, low-complexity generative tasks |
| DAG Orchestration | Graph-based parallel execution with file-bus state passing | Cycle prevention and strict context isolation | Multi-agent workflows requiring high reliability |
| Capability Profiles | Swappable, version-controlled parameter and tool bundles | Rapid persona switching with lifecycle memory purging | Role-based deployment and domain-specific agents |

### Actionable Best Practices (Section 7)

- **Write Software, Not Rules:** Replace negative LLM instructions with deterministic software constraints that make invalid actions impossible
- **Implement Progressive Disclosure:** Load complex instructions dynamically only when skill is explicitly invoked
- **Decouple State:** Never use LLM context window as a database; pass only URIs or pointers via file system or message bus

---

## 11. Selecting Among Hundreds of Skills

By early 2026: 40,000+ listings in public skill marketplaces; Google launched `github.com/google/skills` (`npx skills install github.com/google/skills`).

**Three heuristics:**
1. **Prefer first-party skills** for vendor-specific tools (Google BigQuery skill, official Stripe skill — more correct and more maintained)
2. **Pin everything** you depend on — community skills evolve; unpinned = fragile
3. **Audit before adopting** — a skill is code that runs in your context; treat it like any dependency with supply-chain hygiene

**Trust categories:**

| Source | Trust Default | Who Maintains |
|---|---|---|
| First-party vendor skills | Trust by default; pin a version | Team that built the underlying product |
| Organization-curated skills | Trust within org; review on adoption | Your own domain teams, with PR review |
| Community skills | Audit before adopting; pin aggressively | Volunteer authors, varying commitment |

---

## 12. Appendix A — The Practical Cheatsheet

### Minimal SKILL.md Template

```markdown
---
name: skill-name
description: |
  [What it does in one verb-led sentence.] Use this skill when the user [trigger phrase 1],
  [trigger phrase 2], or [trigger phrase 3].
  Do NOT use for [anti-trigger 1] or [anti-trigger 2].
version: 1.0.0
license: MIT
allowed-tools: [Optional] Read Bash Write
metadata:
  author: [Optional] your-handle
---

# Skill Name

## When to use
- [Concrete scenario]
- [Concrete scenario]

## When NOT to use
- [Out-of-scope scenario]

## Workflow
1. [Step]
2. [Step]
3. See `references/advanced.md` for [edge case].

## Examples
- Input: "..." → Output: "..."

## Output format
- Use `assets/template.md` etc.

## Anti-patterns to avoid
- Don't [...]
```

### The Five Rules

1. **One skill, one job.** If you cannot describe what the skill does in one sentence, it is two skills.
2. **Descriptions are an interface.** The agent picks skills by reading descriptions. A vague description means an unused skill.
3. **Skills are dependencies.** Version them, pin them, review them in PRs. "A skill without a test is a hope, not a capability."
4. **The right team owns the right skill.** Domain experts own domain skills. Don't let the AI team be a bottleneck for domain knowledge.
5. **The agent runtime is interchangeable.** Don't tie skills to one runtime. Portability is part of the value.

### The Six Quality Principles

1. Run the task yourself first. Real failure produces signal. Speculation produces noise.
2. Give the reason, not just the rule. Models generalize to edge cases when they understand *why* an instruction exists. If you're typing "ALWAYS" or "NEVER" in caps, pause and explain the rationale instead.
3. Every line should earn its place. Keep gotchas, exact commands, business logic, anti-patterns. Cut boilerplate.
4. One skill, one job. If the description needs "and" between unrelated capabilities, split it.
5. Make instructions verifiable. If the agent can't tell whether it followed the rule, the rule is too vague.
6. Bundle what repeats. Helper code the agent keeps re-deriving belongs in `scripts/`.

### Naming Rules

- Directory name: `snake_case`
- Skill name: `kebab-case`
- Prefer gerund form: `processing-pdfs`, not `pdf-processor`
- Avoid generic names: `helper`, `utils`, `tools`, `data`
- Avoid vendor prefixes: `claude-*`, `gemini-*`, `anthropic-*`
- Avoid internal jargon outsiders won't recognize

### Description Field Rules

- State what it does AND when to use it
- Front-load trigger keywords ("Generate a commit message…", not "This skill helps with…")
- Include when NOT to use to prevent over-triggering
- Be pushy when the model under-triggers
- ≤200 chars for API; ≤1024 chars in YAML; aim for ~50 words

### Skill Smells (Revise If You See These)

- Over 5,000 words → probably two skills or references material
- Two domain teams could plausibly own it → not yet decomposed
- You can't write three test cases → description too vague
- It does not reference any other resource → might just belong in system prompt
- You keep adding "edge cases" sections → each edge case wants its own skill
- Description starts with "a helpful skill for…" → rewrite with trigger, inputs, output

### Deployment Checklist

- ☐ Frontmatter validates (lint passes)
- ☐ Description includes what + when + when-not
- ☐ Scripts have unit tests passing in CI
- ☐ Eval suite passes in CI with min-pass threshold
- ☐ Security scan clean (no secrets, no untrusted deps)
- ☐ Description reviewed by someone other than the author
- ☐ Cross-tool install paths tested if shipping publicly
- ☐ Org-level admin provisioning updated (if applicable)

### Where to Start Tomorrow

1. Take most experienced practitioner aside for an hour; ask them to narrate three workflows they do regularly. Record it.
2. Pick the most repeated workflow. Run prompts yourself without any skill loaded. Note where agent fails.
3. Draft a SKILL.md from the transcript. Write three eval cases (two positive, one negative) BEFORE drafting the body.
4. Ship to read-only tier. Test in production-like conditions. Iterate description until trigger accuracy clears 90%.

---

## 13. Appendix B — Case Study: Retail Skills Library

**Why retail is the canonical case:** Expertise locked in three inaccessible places — heads of senior buyers/merchandisers, 30-page operational runbooks no one reads, Slack threads from 2023.

### Three-Layer Architecture

- **Top layer:** Customer surfaces (web chat, mobile app, in-store kiosk, voice agent) — thin, forwards input and renders response
- **Middle layer:** Agent runtime + orchestrator (loads skills, calls tools, assembles reply)
- **Bottom layer:** Data/tools plane (product catalog, live inventory, customer profile, vector search over reviews/manuals/specs)

The runtime is generic (Google ADK, Anthropic Claude Agent SDK); the skills are the differentiation.

### Illustrative Skills Library (Home-Improvement Retailer)

| Skill | What It Does | Owner | Tier |
|---|---|---|---|
| `project-guidance` | Turns vague query ("how do I tile a shower?") into step-by-step plan with structural dependencies and common mistakes | Trades knowledge / category mgmt | Read-Only |
| `materials-list` | Takes project description → grouped bill-of-materials including items contractors forget | Pro merchandising | Draft-Only |
| `review-summarize` | Condenses long product reviews into pros/cons/use cases | Personalization | Read-Only |
| `delivery-window` | Computes last-mile delivery options and ETAs given customer location, store availability, freight network | Store operations / fulfillment | Read-Only |
| `return-policy` | Encodes return rules including exceptions (special-order, hazmat, custom cuts, contract pricing) | Customer service | Read-Only |

### Distributed Ownership Model

- Domain experts own domain skills (trades team edits project-guidance weekly anyway)
- AI team is NOT the bottleneck
- Skills library = durable strategic asset; runtime = commoditized

**"A retailer that invests heavily in custom agents but neglects its skills library is investing in the part of the stack that competitors will reach for free."**

### Read / Draft / Act Governance Ladder

| Tier | Capability | Review | Examples |
|---|---|---|---|
| Read-Only | Fetch, query, describe data; cannot mutate state | Domain team approval | `review-summarize`, `store-locator`, `project-guidance` |
| Draft-Only | Produce content for human review; cannot send or commit | Domain team + format owner | `draft-customer-email`, `materials-list` |
| Action-Allowed | Execute irreversible operations on real systems | Domain team + security/compliance + executive sign-off | `issue-refund`, `send-customer-message`, `reserve-inventory` |

---

## Key Metrics and Benchmarks

| Claim | Source | Number |
|---|---|---|
| Skills that performed worse than no skill | SkillsBench (2025) | 19% |
| Non-invocation rate for expected-to-fire skills | Vercel production analysis | 56% |
| Industry-standard trigger accuracy target | Paper | 90% |
| Accuracy drop due to tool proliferation | MCPVerse | 18.2% |
| Production performance drop vs. offline benchmark | ReliabilityBench | 20-30% |
| Simulation-based eval optimistic bias | "Lost in Simulation" | Up to 9% |
| pass^1 vs. pass^8 gap (GPT-4o) | tau-bench | 61% → <25% |
| Claude Code operational infrastructure vs. agent loop | Liu et al. (2026) | 98.4% vs. 1.6% |
| Context reduction from workflow-to-skills conversion | Anthropic | ~150,000 → 2,000 tokens (>98%) |
| Gemini skill improvement on SDK code generation | Google Developers Blog | 28.2% → 96.6% |
| False pass rate: final-output-only vs. trajectory-aware | Latitude (March 2026) | 20-40% more false passes |
| Final-output score for skill-stripped vs. no-skill baseline | Vercel | 58% vs. 63% |

---

## References (Selected Key Papers)

- SkillsBench (2025): arXiv:2602.12670
- Vercel production analysis: vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
- Latitude agent comparison: latitude.so/blog/agent-first-comparison-guide-vs-braintrust
- Google ADK eval: adk.dev/evaluate/
- EDD paper: arXiv:2411.13768v2
- MCPVerse tool proliferation: arXiv:2508.16260
- Context Rot (Chroma Research, 2025): research.trychroma.com/context-rot
- tau-bench (Yao et al., 2024): arXiv:2406.12045
- ReliabilityBench: arXiv:2601.06112
- Lost in Simulation: arXiv:2601.17087
- Lost in the Middle (Liu et al., TACL 2024): arXiv:2601.06112
- Voyager Minecraft skills: arXiv:2305.16291
- Claude Code reverse-engineering (Liu et al., 2026): ccunpacked.dev
- Ling et al. (2026) skills marketplace analysis: arXiv:2602.08004

---

## Capstone Hooks

1. **Build a multi-skill agent library** — pick a domain (search relevance, data science workflows), create 5+ skills with proper SKILL.md structure, demonstrate progressive disclosure in action vs. monolithic system prompt
2. **Implement EDD end-to-end** — write eval cases first, then build skills, run automated trigger + trajectory evals in CI, produce a pass^k report
3. **Meta-skill demonstration** — build a skill-creator meta-skill that harvests successful traces and proposes SKILL.md drafts; gate all proposed skills at draft tier until eval passes
4. **Skill vs. multi-agent comparison** — implement the same workflow both ways, measure token cost, trigger reliability, and iteration cycle time
5. **Skills governance system** — implement the Read/Draft/Act tier ladder with automated gates; demonstrate a skill being blocked from action-allowed promotion until adversarial tests pass
6. **Retail-style skills library** — apply the domain ownership model to any domain you know (search relevance: `query-understanding`, `ranking-explanation`, `ndcg-eval`); show how domain experts own their skills
7. **Context rot demonstration** — measure performance degradation as skills are co-loaded (1 vs. 5 vs. 15 skills), reproduce the U-curve from "Lost in the Middle"
