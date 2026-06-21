# Vibe Coding Agent Security and Evaluation

**Source:** Kaggle AI Agents Intensive — Vibe Coding, May 2026
**Authors:** Sokratis Kartakis, Aron Eidelman, Wafae Bakkali, Meltem Subasioglu

---

## Core Thesis

> "Security tells you if the agent stayed inside the boundary, ensuring it operates safely and without malicious intent. Evaluation tells you whether what happened inside that boundary is actually worth shipping."

Software engineering is shifting from *writing code* to *expressing intent*. This creates two new trust axes that must both be solved to operationalise vibe coding in the enterprise:

- **Security** — did the agent stay inside the boundary?
- **Evaluation** — was what happened inside that boundary worth shipping?

---

## Part 1: Security

### The Fundamental Shift

> "A raw AI model is not an agent. It only becomes one when wrapped in a 'harness'—the scaffolding that gives it state, tool execution, feedback loops, and enforceable constraints. Securing this new paradigm requires shifting our focus from securing code syntax to securing this harness."

Traditional security = deterministic, binary trust (code compiles, tests pass, credentials valid).
Agentic security = **Effective Trust** — a *continuous metric* evaluated across supply chain, identity, runtime behaviour, and contextual associations.

The perimeter model shifts from **Identity-as-a-Perimeter** (RBAC) → **Context-as-a-Perimeter** (ABAC + JIT).

---

### The 7-Pillar Agent Security Architecture

The foundational baseline that must be in place before any autonomous agent operates in enterprise:

#### Pillar 1 — Infrastructure & Networking
- Isolate runtime in **ephemeral, kernel-level sandboxes** (e.g., gVisor)
- Strict **network egress governance**: agent-generated data travels only through authorised offline caches or explicit internal proxies
- Prevents: container escapes, upstream poisoning, inadvertent public exfiltration

#### Pillar 2 — Data
- Data at rest: **Customer-Managed Encryption Keys (CMEK)**
- Data in transit: **mutual TLS (mTLS)**
- Scope data access down: enforce **least privilege**
- Vector databases: enforce **strict tenant partitioning** to prevent Cross-Tenant Vector Poisoning

#### Pillar 3 — Model
- Treat system instructions and prompt templates as **cryptographically attested artifacts**
- "The prompt and the 'Instructions and Rule Files'... serve as the new source code"
- Secures against **semantic attacks** that subvert model instructions

#### Pillar 4 — Application & Runtime
- Deploy **LLM firewalls** for dynamic prompt and response filtering
- **Deterministic hooks** at lifecycle points (before tool call, after file edit)
- **Centralised Agent Gateways** governing Agent-to-Agent (A2A) orchestration
- Prevents: unauthorised lateral movement, MCP spoofing

#### Pillar 5 — Identity and Access Management (IAM)
- Assign **unique, cryptographic identities** (SPIFFE IDs) to every individual agent
- Use **Attribute-Based Access Control (ABAC)** + **Just-In-Time (JIT) token downscoping**
- Permissions matrix: **Intent × User × Time**
- Tokens expire immediately after task concludes
- Prevents: the Confused Deputy problem

#### Pillar 6 — Observability & Security Ops
- Deploy autonomous **SecOps triad**: Red + Blue + Green teams
- **Blue Team**: OpenTelemetry + Agent Behavioural Analytics (ABA)
- **Red Team**: proactive multi-hop attack simulation
- **Green Team**: Stateful Quarantines on anomaly detection
- Prevents: invisible failures, infinite reasoning loops

#### Pillar 7 — Governance
- **EU AI Act** compliance: Algorithmic Impact Assessments for high-risk agents
- **Immutable audit trail** attributing every action to a specific agent and the human who deployed/approved it
- Replace approval buttons with mandatory **Logic Reviews** (plain-language translation of generated code)
- **Risk-Stratified Attestation**: bind digital signatures to agent outputs

---

### Sandboxes and Supply Chain Defence (Pillars 1 & 4)

#### Ephemeral Sandboxing
- All skill-generated code executes in ephemeral, network-isolated sandboxes
- Sandboxes must: block raw host access + completely reset state between runs
- Even if a script contains severe vulnerability, the compromised logic cannot persist

#### Mitigating Hallucinated Packages ("Slopsquatting")
> "Attackers actively exploit the tendency of language models to hallucinate dependency names: they upload malicious packages using these fabricated names so that automated agents will inadvertently download them."

Defences:
- Source dependencies exclusively from **vetted providers or internal enterprise registries**
- Enforce **strict cryptographic version pinning**
- CI/CD pipelines must automatically verify **Software Bill of Materials (SBOM)** entries and digital signatures via **Binary Authorisation**

#### Egress Governance
- Restrict agents to **non-interactive internet access**
- Force all external data through **offline caches or pre-sanitised web-crawling services**
- Simple allowlists are insufficient (cannot protect against indirect prompt injections in third-party pages)

---

### Securing Application Logic (Pillar 4)

#### Common Application Vulnerabilities from Vibe Coding
1. **Frontend trust failure**: AI handles sensitive operations client-side — API keys, password validation, session flags in browser, readable via DevTools
2. **Default-open backend**: row-level database security skipped, private data exposed publicly; admin dashboards connected without access controls

#### IDE vs CI/CD Balance
- **Developer Advisory Linters in the IDE**: real-time guidance only, never hard-block (causes friction, easily bypassed)
- **CI/CD pipeline**: unyielding enforcement via:
  - **SAST** (Static Application Security Testing)
  - **SCA** (Software Composition Analysis)

#### MCP Spoofing and Contextual Authorisation
- Forged MCP servers can inject payloads or demand excessive privileges autonomously
- Defences:
  - **Runtime LLM firewall** in front of active agent: dynamically intercepts prompt injections
  - **Centralised Agent Gateway**: evaluates Contextual Authorisation — verifies if agent's tool request aligns with developer's original intent

---

### Identity, Trust & High-Stakes Actions (Pillar 5)

#### The Confused Deputy Problem
- Prompt injection in an open-source repo pasted into IDE context tricks over-privileged agent into executing unauthorised commands
- Fix: agent must never be final arbiter of access; must authenticate as **dedicated agentic identity** (not delegated user credentials)

#### Zero Ambient Authority + JIT Downscoping
> "An agent executing a 'vibe' must never inherit the developer's full, ambient administrative privileges."

- Execution sandbox receives **fresh, hyper-restricted credentials** scoped to exact data sources for that specific script
- **File-tree allowlists**: deny-by-default, confine read/write to project directories, block secrets/build scripts/production manifests
- Tokens expire the exact moment the task concludes

#### Elicitation and the "Vibe Diff"
High-stakes actions (production DB modifications, financial transfers, IAM changes) require:

1. **Cryptographic Hardware MFA**: physical USB security key touch to cryptographically approve execution
2. **The Vibe Diff**: an Evaluator Quorum intercepts the request and translates complex generated code into a plain-English summary showing how fuzzy intent maps to proposed execution steps — requires explicit human cryptographic consent

> The "It Works, Ship It" fallacy: simple approval gates cause confirmation fatigue → developers blindly authorise code they don't understand.

---

### Red, Blue, and Green Security Teaming (Pillar 6)

#### Invisible Payloads and Repository Poisoning
> "Threat actors can compromise repositories by inserting zero-width Unicode characters or homoglyphs directly into the codebase... these 'invisible payloads hide in plain sight and bypass human review'... a single hidden payload can 'spread across hundreds of files in minutes'."

#### Red Team (Agent Attacker)
- Deploys **Virtual Red-Teaming Agents** that proactively inject "Adversarial Vibes"
- Techniques: sophisticated roleplay jailbreaks, hiding malicious instructions inside massive RAG context blocks or dummy forum posts
- Tests whether target agent gets distracted by poisoned context and hallucinates insecure solutions

#### Blue Team (Agent Defender)
- Replaces traditional **UEBA** (User and Entity Behaviour Analytics) with **Agent Behavioural Analytics (ABA)**
- Continuously monitors the **Runtime Agent Bill of Materials (AgBOM)** — a dynamic inventory of tools, models, and data sources at any given millisecond
- Flags: sudden querying of unusual tools, unbounded resource loops, intent drift

#### Green Team (Agent Fixer)
- Executes **Stateful Quarantine** via SOAR playbooks on anomaly detection
- Gracefully revokes tool access, freezes autonomous execution, preserves short-term memory for forensic analysis
- Performs **Auto-Refactoring**: autonomously rewrites insecure code and presents the fix in the IDE

#### Integrating the Triad
- Enforce **small batch sizes**: block agent from modifying tests and implementation code simultaneously (test = objective baseline)
- Three phases:
  - **Planner Phase**: threat-modelling skill evaluates plan for logical flaws and policy violations
  - **Evaluator Phase**: Evaluator quorum reviews trace; Blue simultaneously verifies AgBOM and monitors for intent drift
  - **Executor Phase**: Green monitors real-world tool execution, ready to quarantine or trigger auto-refactoring

---

### Observability: Auditing the Agent's Mind (Pillars 6 & 7)

> "You cannot secure what you cannot see."

In agentic systems, HTTP 200 OK might mask an agent quietly cascading into a hallucination loop. This creates:

- **Denial of Wallet (DoW) attacks**: adversaries trigger infinite, computationally expensive API loops to bankrupt cloud/LLM billing accounts

#### Tracing the "Vibe Trajectory"
- Use **OpenTelemetry** to aggregate: API calls, tool inputs/outputs, RAG retrievals, token latency
- Log the cognitive leap from initial prompt → compiled Abstract Syntax Tree (AST)
- Pair with **Centralised Content Scanning** for dynamic code snippets retrieved at runtime

#### Intent Drift and Trust Decay
- Monitor **Runtime AgBOM** (living document, not static SBOM — static ones are instantly stale)
- **Trust Decay**: trust is lost when agent's chain of thought pursues sub-goals diverging from original intent
  - Example: "optimise the database query" drifts into downloading unauthorised indexing library
- **Agent Trust Score**: continuously updated; dropping below threshold trips circuit breaker

#### Checkpoints and Stateful Circuit Breakers
- Before any codebase modification: generate **version control checkpoint**
- If Agent Trust Score drops below threshold: automated circuit breaker rolls back changes, gracefully revokes tool access, preserves state for forensic analysis

---

### Security Recap Checklist

1. **Sandbox the Vibe Loop**: ephemeral, network-isolated, kernel-level sandboxes + SCA before production
2. **Shift the Perimeter Left**: trusted registries + advisory IDE linters + strict CI/CD deterministic checks
3. **Enforce Zero Ambient Authority**: delegated identities + JIT hyper-restricted tokens + Vibe Diff for high-stakes
4. **Deploy Agentic SecOps**: Virtual Red-Teaming Agents + ABA monitoring dynamic AgBOM + Green Team auto-refactoring
5. **Trace the Execution Trajectory**: log API calls, tool inputs, reasoning steps + version control checkpoints for rollback

---

## Part 2: Evaluation

### Why Vibe Coding Evaluation is Different

Three unique constraints:

#### 1. The Underspecification Gap (No Spec)
> "Vibe coding is the exact opposite [of traditional testing]: the user's natural language prompt is inherently underspecified. 'Make the dashboard load faster' is not a test case."

The first job of evaluation: determine whether the agent successfully bridged this gap and reconstructed the right unstated spec.

#### 2. The User Cannot Validate the Output
> "The gap between 'the agent thinks it succeeded' and 'the code is actually correct' is wider here than in any other agent category."

Non-technical users cannot review 600 lines of code. Neither can experienced engineers, in real time.

#### 3. The Session is Iterative; the Codebase is State
Each turn modifies real files. Bad early decisions compound. Evaluation must cover not just turn-level decisions but the full arc of a multi-turn conversation on a living codebase.

---

### 7 Evaluation Dimensions

**User-facing dimensions:**

1. **Intent Satisfaction** — Did the agent build what the user *meant*, not just what they *said*? Hardest to evaluate; what the user ultimately judges.

2. **Functional Correctness** — Does the code build, run, and pass tests? The floor, not the ceiling. Easy to game (tests can be deleted or mocked).

3. **Visual and Behavioural Correctness** — For UI/web agents, the rendered output is the artifact. Code-level metrics miss this entirely.

4. **Cost and Efficiency** — Token spend, wall-clock latency, tool-call count, iteration count. An agent that lands the right diff in 1 turn is a different product from one that needs 8 corrections.

**Internal dimensions:**

5. **Code Quality and Convention Matching** — Does the code match the project's idioms, patterns, and conventions? A diff that passes tests but violates codebase style is a vibe-coding failure.

6. **Trajectory Quality** — Did the agent take a sensible path: read related files first, sequence edits coherently, pick the right tool at each step? Correct output from bad reasoning is a fragile success.

7. **Self-Repair Behaviour** — When build fails, test breaks, or user says "no, not like that," does the agent recover or compound the failure?

**Transversal:** Safety and Responsible AI intersects all dimensions (code vulnerabilities, refusal behaviour, content safety, IP exposure).

> "Stronger trajectory quality (dimension 6) tends to mean stronger functional correctness (dimension 2), which is a prerequisite for intent satisfaction (dimension 1)."

---

### 7 Evaluation Methods

| Method | Best For |
|---|---|
| Automated functional testing (pytest, jest, eslint, mypy) | Dimensions 2, 5 (rule-checkable parts) |
| Security and safety evaluation (Snyk, Semgrep, git-secrets, red-team scripts) | Cross-cutting safety + all dimensions |
| LLM-as-judge / Agent-as-judge | Dimensions 1, 5, 6 (where rules don't capture the right answer) |
| Browser-based testing (Playwright + screenshot comparison) | Dimension 3 (UI/visual correctness) |
| Trajectory inspection (OpenTelemetry spans + trace-replay tools) | Dimensions 6, 7 |
| Human review (structured annotation by senior engineers) | Dimensions 1, 5, safety judgment calls |
| Online evaluation (sampled live traffic scored against rubrics) | All dimensions at sample rate |

---

### Standardised Benchmarks

- **Vibe Code Bench**: evaluates zero-to-one web app generation
- **SWE-bench Verified**: evaluates code changes on real GitHub repos
- **LiveCodeBench**: contamination-resistant signal for code generation
- **Kaggle Standardised Agent Exams (SAE)**: "zero-setup" autonomous evaluation
  - Deployed via SKILL.md file
  - Agent autonomously registers, fetches exam questions, executes in sandboxed environment, publishes score to live leaderboard
  - Tests multi-hop reasoning and adversarial safety under pressure

**Benchmark Tradeoff Warning:**
> "Agents can be hyper-optimized to achieve top-tier scores on static Kaggle datasets but fail catastrophically when exposed to the messy, contradictory realities of human intent in production."

Use benchmarks strictly for **cognitive calibration**, not as replacement for evaluating custom intent.

---

### Observability as Evaluation Prerequisite

> "Observability is the absolute prerequisite for Glass Box evaluation; without it, agent failures appear as inexplicable monolithic events."

**OpenTelemetry span types:**
- `agent.session` — entire task duration
- `agent.think` — internal reasoning and prompting cycle prior to action
- `agent.tool` — specific arguments and latencies of environmental interactions

**Dynamic Tail-Based Sampling**: drop routine successes, retain traces containing errors or excessive self-repair loops.

---

### Applied Evaluation Tips (with Code)

#### Tip 1: Use Session Prefix as Intent Rubric
> "Treat [the first 1-2 user messages] as the rubric: derive evaluation criteria automatically from the session prefix, then score every subsequent turn against them."

```python
from google import genai

client = genai.Client(vertexai=True, project="...", location="us-central1")

# Derive criteria from the user's opening turns
opening = " ".join(session.user_messages[:2])
criteria = client.models.generate_content(
    model="gemini-3-pro",
    contents=f"Produce 3-5 acceptance criteria for: {opening}. Return JSON.",
).parsed["criteria"]

# Score every agent turn against the derived criteria
score = client.models.generate_content(
    model="gemini-3-pro",
    contents=f"Does this output satisfy {criteria}? Score 1-5 with rationale."
    f"Output: {agent_response}",
).parsed
```

#### Tip 2: Judge the Rendered Artifact, Not the Code
> "A multimodal model looking at the rendered page catches problems that code-level evaluation misses entirely: layout broken on mobile, contrast too low for accessibility, button states wrong."

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project="...", location="...")

result = client.models.generate_content(
    model="gemini-3-pro",
    contents=[
        "Score this rendered web app against the spec on layout_match, styling, "
        "and interactive_correctness (1-5 each). Return JSON.",
        user_spec,
        types.Part.from_bytes(data=screenshot_bytes, mime_type="image/png"),
    ],
)
```

#### Tip 3: Evaluate Session Convergence, Not Turn-Level Accuracy
> "The relevant question is not 'was turn 4 correct?' but 'did the user converge on something they wanted?' Sessions abandoned mid-flow are the most informative failures."

```python
from google.cloud import trace_v2

trace = trace_v2.TraceServiceClient().get_trace(
    name=f"projects/{project}/traces/{session_id}"
)

def session_outcome(trace):
    return {
        "converged": trace.last_turn.user_signal == "satisfied",
        "turns_to_converge": trace.user_correction_count,
        "abandoned": trace.last_user_action == "close",
        "cost_to_converge": trace.total_token_cost_usd,
    }
```

#### Tip 4: Mine User Corrections as Labeled Failure Data
> "Every 'no, not like that' from the user is a labeled failure example, and vibe coding produces these in volume. Cluster them and the systematic gaps in the agent become visible."

```python
from google import genai
from sklearn.cluster import KMeans

client = genai.Client(vertexai=True, project="...", location="...")

corrections = [t.user_message for trace in traces for t in trace.turns if t.is_correction]

emb = client.models.embed_content(
    model="text-embedding-005",
    contents=corrections,
)
vectors = [e.values for e in emb.embeddings]

clusters = KMeans(n_clusters=8).fit(vectors)
# clusters.labels_ is the prioritized list of failure modes for the next iteration
```

---

## Conclusion

> "Generation is largely a solved problem. Verification, security, and architectural judgment are the new craft."

The bottlenecks in software creation have shifted from typing boilerplate → defining boundaries, evaluating outputs, and securing execution environments. A raw AI model only becomes an enterprise-ready agent when wrapped in:

1. **7-Pillar Security Architecture** (sandboxing + contextual ABAC + agentic Red/Blue/Green teaming)
2. **Rigorous Evaluation Framework** (intent satisfaction + trajectory quality + visual correctness)

---

## Key Reference Tools/Standards Mentioned

- **gVisor** — kernel-level sandbox
- **SPIFFE IDs** — cryptographic agent identities
- **OpenTelemetry** — observability framework
- **CMEK** — Customer-Managed Encryption Keys
- **mTLS** — mutual TLS for data in transit
- **SBOM / AgBOM** — Software/Agent Bill of Materials
- **Binary Authorisation** — CI/CD artifact gate
- **SAST** (Snyk, Semgrep) — static security analysis
- **SCA** — Software Composition Analysis
- **SOAR playbooks** — automated incident response
- **MCP** — Model Context Protocol (A2A tool coordination)
- **Playwright** — browser-based UI testing
- **pytest, jest, eslint, mypy** — automated functional testing
- **git-secrets** — credential leak detection
- **Vibe Code Bench, SWE-bench Verified, LiveCodeBench** — standardised benchmarks
- **Kaggle SAE** — Standardised Agent Exams (zero-setup)
- **Google Vertex AI / genai SDK / Cloud Trace** — eval infrastructure
