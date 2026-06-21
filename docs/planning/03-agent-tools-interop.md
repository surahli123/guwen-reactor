# Agent Tools & Interoperability
**Kaggle Vibe Coding Course — Whitepaper 03**
Authors: Kanchana Patlolla, Łukasz Olejniczak, Pier Paolo Ippolito | May 2026

---

## Overview / Core Thesis

> "Software's next evolution isn't written: it's orchestrated by interoperable agents."

The paper argues that MCP, A2A, A2UI, AP2, and UCP are the **Industry Standards** — the uniform communication layers — that transform isolated "custom machine" agents into a modular, plug-and-play platform. Without them, every agent is a tech-debt island; with them, a developer shifts from low-leverage **Conductor** (wiring APIs) to high-leverage **Orchestrator** (directing intent).

---

## Protocol Ecosystem Map

| Protocol | Metaphor | Role |
|---|---|---|
| MCP (Model Context Protocol) | "USB-C" | Connects models to tools/data (databases, filesystems, APIs) |
| A2A (Agent-to-Agent) | "Factory Radio" | Lets specialized agents negotiate, brainstorm, and delegate tasks |
| A2UI (Agent-to-User Interface) | "Generative Display Window" | Turns agent outputs into safe, interactive visual components |
| AP2 (Agent Payments Protocol) | "Parent's Credit Card with Strict Rules" | Secure, authorized agent payments |
| UCP (Universal Commerce Protocol) | "Ultimate Food Delivery App" | Agent-to-merchant catalog/order negotiation |
| OpenResponses & Interactions API | "Power Plugs" | Modern LLM inference APIs supporting long-running tasks |
| Skills | "Playbooks" | Markdown instructions + scripts for sandbox execution |

---

## Section 1: MCP — The Vibe Coder's View

### Three Steps to Onboard an MCP Server

1. **Discovery** — find pre-built servers from:
   - Public registries (e.g., `registry.modelcontextprotocol.io`, `github.com/mcp`) — unvetted, use at own risk
   - Third-party remote MCP servers — vetted, managed (e.g., Google Maps, BigQuery, Google Docs official servers)
   - Internal registries — API gateways, GCP Agent Registry, private microservice portals

2. **Configuration** — set scope, permissions, environment files for credentials (PATs, OAuth), define read/write permissions

3. **Connection** — client handshake: list available tools, validate output schema

### The NxM Problem (Why MCP Matters)

Traditional integration = O(N × M): 5 models × 10 tools = 50 bespoke integration points.
MCP integration = O(N + M): linear scale.

```
Traditional:                    MCP:
[Model A] ── [Tool 1]          [Model A] ──┐    ┌── [Tool 1]
[Model B] ── [Tool 2]          [Model B] ──┼─[MCP]┼── [Tool 2]
[Model C] ── [Tool 3]          [Model C] ──┘    └── [Tool 3]
Effort: O(N x M)               Effort: O(N + M)
```

### Transport Options

- **stdio** (Standard I/O): Local prototyping. Host launches MCP server as subprocess, passes JSON-RPC 2.0 over stdin/stdout. No network setup required.
- **SSE (Server-Sent Events) over HTTP**: Remote MCP endpoint. Fewer deps, always up to date, smaller footprint — but higher burden on cloud-hosted server.

### Debugging MCP Issues

- **MCP Inspector**: Native dev tool — local web panel to manually query any local/remote MCP server, view tool schemas, test payloads, inspect raw JSON-RPC 2.0 packets — WITHOUT running the main agent workflow.
- **Chrome DevTools**: For web-based environments or SSE connections — trace incoming web streams, check server latencies.

### Vibe Coder Toolkit — Do's

- Audit public servers before connection — review open-source code before attaching to agent with filesystem/credential access
- **Use RAG for tools**: dynamically load tools from registry only when needed; drop from context when task completes (prevents attention dilution)
- Leverage internal API gateways and registries for governed, approved schemas
- Use MCP Inspector first when agent hallucinates tool calls — don't blindly tweak system prompt
- **Include HITL**: show tool inputs to user before calling server (prevents accidental data exfiltration)
- Log tool usage for audit purposes

### Vibe Coder Toolkit — Don'ts

- Don't build if you can consume — search for existing MCP server first
- Don't use public/unverified MCPs in production
- Don't hardcode credentials — use environment variables
- Don't connect to production data — use dev environment with non-production / obfuscated data
- Don't use for writes unless necessary — set server to read-only mode when possible
- Don't provide wide access — scope MCP server to specific project resources

---

## Section 2: A2A — Agent-to-Agent Interoperability

### Evolution of Agentic Architectures

The paper draws a parallel to the **Monolithic → Microservices** shift in software history, and to **AutoML → production ML pipelines**.

**Stage 1: Single Agent Monolith ("Swiss Army Knife")**
- One agent, one huge prompt, many tools
- Problems:
  - **Scaling Friction**: Can't optimize DB logic without confusing UI logic; more tools = worse decision-making (search space too large → hallucinated parameters)
  - **Contextual Overload**: System instructions + dozens of tool schemas + conversation history maxes out context window
  - **Single Point of Failure**: Bug in one tool crashes entire agent; corrupted context carries forward

**Stage 2: Internal Specialization (Modular Monolith)**
- Logically partition into distinct sub-agents, each with focused system prompt + relevant tool subset
- Still single runtime + shared memory (no network boundaries)
- Benefits: reduces search space, mitigates attention dilution, optimizes contextual load

**Stage 3: Distributed Multi-Agent Architecture**
- Orchestrator delegates across network boundaries to remote, domain-specific agents
- Industry leaders deploying: Google, Salesforce, ServiceNow, Workday — each offering domain-specific AI agents
- Problem: fragmentation — each agent built with different tech, different payload structures, different transport layers

**A2A solves fragmentation.** Donated by Google to the Linux Foundation. As of 2026: 150+ organizations, in major cloud platforms, enterprise production use.

> "Just as HTTP standardized the web, A2A standardizes the virtual workforce."

### Tools vs. Agents: The Fundamental Distinction

| Dimension | Tool (MCP) | Agent (A2A) |
|---|---|---|
| Domain | Bounded — fixed input/output schema | Unbounded — ambiguous requirements, multi-turn clarification |
| Control flow | Fire-and-forget | Can pause, reach back, negotiate, resume |
| State | Stateless | Maintains conversational state |
| Engagement | Passive instrument | Collaborative partner |

**The GOTO Problem**: Forcing an agent into a tool wrapper introduces unstructured control flow. The agent may never return if user changes intent. A2A isolates this messy multi-turn state, keeping MCP clean and predictable.

### Building the Virtual Workforce

**The Agent Card** — the machine-readable "CV" of the AI world:
- Capabilities: what tasks the agent can perform
- Security & Compliance: data handling policies and permission requirements
- Interaction Schemas: how to communicate via A2A protocol

**Agent Registries** — two paths:
1. **Public Registries (Marketplaces)**: like a global talent agency; enables licensing specialist expertise to thousands of orchestrators
2. **Private Registries**: enterprise-internal, governed environment; secure cross-department sharing

### Implementing A2A — Two Motions

**Supply side (Exposing a native agent as A2A):**
1. Define the Agent Card (formal agent specification)
2. Implement the Agent Executor (translation layer between A2A and underlying framework — ADK, LangGraph, bespoke)
3. Establish the A2A Endpoint (expose executor as A2A-compliant endpoint)

**Demand side (Connecting to remote A2A agents):**

Pattern 1 — Direct point-to-point:
```python
billing_specialist = RemoteA2aAgent(
    name="billing_agent",
    endpoint="https://api.vendor.com/v1/billing/a2a"
)
```

Pattern 2 — Via Agent Registry:
```python
registry = AgentRegistry(project_id=project_id, location=location)
agent_name = f"projects/{project_id}/locations/{location}/agents/YOUR_AGENT_ID"
my_remote_agent = registry.get_remote_a2a_agent(agent_name=agent_name)
```

### Monetizing A2A: Agent-as-a-Service (AaaS)

- Follows the SaaS playbook: consumption-based model
- Google Cloud Marketplace: list A2A agents to reach enterprise GCP customers; leverages existing GCP financial commitments
- Native support for hybrid pricing: "Flat fee with usage" model
- Permissionless microtransactions: x402 / L402 standard — server returns HTTP 402 with machine-readable invoice; calling agent pays autonomously and retries with cryptographic proof-of-payment token

### A2A Extensions

Three foundational frameworks built as native extensions atop A2A:
1. **A2UI** — dynamic, stateful user experiences
2. **UCP** — secure, autonomous agentic commerce
3. **AP2** — trusted, verifiable agentic payments

---

## Section 3: A2UI — Agent-to-User Interface Interoperability

### The Communication Gap

Agents return raw JSON. Humans share insights through visuals. A2UI bridges this — agents generate complete, interactive UIs as outputs.

### Generative UI — Definition

> "Generative UI is the concept of LLMs dynamically creating user interfaces at runtime based on user intent and context. Instead of developers hard-coding every possible UI state, the model generates appropriate interfaces on demand."

Challenge: running arbitrary LLM-generated UI code → security risks (code injection, XSS, uncontrolled side effects).

### A2UI — Definition and Security Model

> "A2UI is a framework-agnostic standard for declaring UI intent — Google's open-source way of letting agents describe interfaces in a portable, declarative format instead of streaming raw data or shipping arbitrary code."

Analogy: **A2UI is sheet music for UI.** The agent writes the intent; any renderer (React, Angular, Lit, Flutter, Jetpack Compose, SwiftUI) performs it natively.

**Security model**: Agents can't inject arbitrary code. They can only request components from a trusted catalog the renderer already trusts. Compositional like LEGO blocks — but the blocks are UI components from your design system.

### The Basic Catalog (v0.9)

18 ready-to-use components:

| Category | Components |
|---|---|
| Layout | Row, Column, List |
| Display | Text, Image, Icon, Divider |
| Containers | Card, Modal, Tabs |
| Media | Video, AudioPlayer |
| Interactive | Button, TextField, CheckBox, Slider, DateTimeInput, ChoicePicker |

Note: called "standard" in v0.8, renamed to "basic" in v0.9 — deliberate signal that production frontends should bring their own catalog (map existing design-system components). `ChoicePicker` was `MultipleChoice` in v0.8.

### A2UI Message Format (v0.9)

```json
{
  "version": "v0.9",
  "updateComponents": {
    "surfaceId": "main",
    "components": [
      {"id": "root", "component": "Column", "children": ["title", "summary", "export"]},
      {"id": "title", "component": "Text", "text": "Q4 Sales", "variant": "h1"},
      {"id": "summary", "component": "Text", "text": "Revenue grew 12% QoQ"},
      {"id": "export", "component": "Button", "child": "export-label",
       "action": {"event": {"name": "export_csv"}}},
      {"id": "export-label", "component": "Text", "text": "Export CSV"}
    ]
  }
}
```

Components form a **flat adjacency list** referenced by id — easy for LLM to generate incrementally, easy for client to update without full re-render.

### Two Patterns for Generating A2UI

**Pattern 1: LLM emits A2UI directly** (default)
- LLM owns the layout, adapts to user intent
- Uses `a2ui-agent-sdk`: `A2uiSchemaManager` builds system prompt with catalog schema + worked examples baked in
- Validate output with catalog's JSON-Schema validator; retry on schema errors
- Use when layout is **intent-driven** (e.g., "Compare these regions")

**Pattern 2: Tool returns fixed A2UI structure** (specialization)
- One tool call, no LLM tokens spent on UI generation, fully predictable output
- Tool acts as server-side template
- Use when layout is **deterministic from inputs** (e.g., "Show me my dashboard" — every dashboard has same fields)
- `A2uiPartConverter` from `a2ui-agent-sdk` intercepts tool response and routes to client as A2UI part

### Query → Output Decision Table

| Query | Return |
|---|---|
| "What's the average?" | Data (text) |
| "Compare these regions" | UI generated by LLM |
| "Show me my dashboard" | UI built by a tool |
| API-to-API | Data (JSON) |

### Canvas + A2UI

- Traditional chat: linear, static responses
- Canvas: persistent workspace where both agent and user can edit
- Living document where agent modifies sections and user edits manually, both reflected in real-time
- A2UI + Canvas = UI as communication medium; agent observes user interactions and responds

### Best Practices

**A2uiSchemaManager pattern (LLM-generates-UI):**
```python
# pip install a2ui-agent-sdk google-adk
from a2ui.schema.manager import A2uiSchemaManager
from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.constants import VERSION_0_9
from a2ui.parser.parser import parse_response

schema_manager = A2uiSchemaManager(
    version=VERSION_0_9,
    catalogs=[BasicCatalog.get_config(version=VERSION_0_9)],
)

agent = LlmAgent(
    model=Gemini(model="gemini-flash-latest"),
    name="ui_agent",
    instruction=schema_manager.generate_system_prompt(
        role_description="You generate interactive UIs as A2UI v0.9 messages.",
        ui_description="Use Cards, Lists, ChoicePickers, and Buttons to present data.",
        include_schema=True,
        include_examples=True,
    ),
)
```

- Parse `<a2ui-json>` blocks with `parse_response()`
- Validate with `catalog.validator.validate(m)` — retry on `jsonschema.ValidationError`
- Max retries = 3; fall back to text response on persistent schema-validation failure
- LLM output is stochastic — renderer must never see a malformed payload

**Hybrid Output pattern (flexibility):**
```json
{
  "data": {"sales": [...]},
  "ui": {"version": "v0.9", "updateComponents": {...}},
  "ui_available": true
}
```
API clients use `data`; human-facing clients render `ui`.

---

## Section 4: AP2 and UCP — Agents and Commerce

### The Shift: Read → Action

Earlier protocols (MCP, A2A, A2UI) are mostly "read" operations. AP2 and UCP enable agents to execute **actions with real-world financial implications**.

### UCP — Universal Commerce Protocol

**What it does**: Agent-to-merchant standardized catalog/order negotiation. A universal translator — every merchant publishes menu/catalog/options in standard machine language.

**Workflow**: AI uses UCP to query availability → build order with customizations → receive confirmation with tax, delivery fee, ETA.

**Before UCP**: Each merchant interaction had to be orchestrated individually (bespoke).
**After UCP**: Standardized interaction — non-humans can interact with each other without custom code per merchant.

### AP2 — Agent Payments Protocol

**Definition**: "The open, shared protocol that provides a common language for secure, compliant transactions between agents and merchants."

**Three mechanisms**:
- **The Mandate (Guardrails)**: User pre-approves digital rule before agent acts ("You can spend up to $25 at Taco Bell")
- **The Handshake**: Agent shows encrypted "promissory note" signed by user, not raw card number; merchant bank verifies digital signature
- **Constraint Enforcement**: Protocol blocks transactions that violate pre-approved rules (blocks $50 charge when $18.50 was signed off)

### UCP vs AP2 Comparison

| | UCP | AP2 |
|---|---|---|
| Role | Brain — decides what to buy, handles catalog, builds cart | Wallet — securely handles payment |
| Integrates with | Any business provider | Payment processors |
| Key features | Unified integration, shared language, extensible architecture | Authorization & auditability, authenticity of intent, agent error/hallucination accountability |

### AP2 Key Properties

- **Authorization & Auditability**: every transaction is authorized and logged
- **Authenticity of Intent**: cryptographic proof that human approved the action
- **Agent Error and Hallucination Accountability**: protocol-level guardrails block unauthorized transactions

---

## Section 5: AGENTS.MD Applied Tip (Coding Agent Discipline)

The paper embeds a coding discipline directly into the whitepaper (applicable to any agent-building workflow):

1. **Think deeply before coding** — state assumptions, surface tradeoffs, halt at ambiguity rather than guessing silently
2. **Write absolute minimum code** — no speculative features, no unrequested abstractions, no predictive configurations
3. **Surgical edits** — restrict to exact lines necessary; maintain existing style; leave adjacent untouched code alone
4. **Goal-driven execution** — break into step-by-step plan with strong success criteria (write failing test first; loop through verification until goal met)

---

## Key Architectural Insights

- **Build vs. Buy lens**: Custom sub-agents for third-party platforms carry "Maintenance Tax" — every upstream API change requires prompt/tool updates. Prefer official specialist agents maintained by domain experts.
- **Specialization as scaling mechanism**: Fundamental law of system design — narrow the tool set → reduce hallucinations → improve reasoning.
- **A2A Extensions pattern**: Core A2A = transport/negotiation backbone. Richer capabilities (UI, commerce) built as standardized extensions atop it — agents advertise and negotiate optional higher-order functionalities.
- **Agent-as-a-Service (AaaS)**: Specialist agents can be listed on Cloud Marketplace, consumption-based pricing, reaching enterprise customers via their existing cloud commitments.

---

## Conclusion (Verbatim)

> "By adopting foundational standards like MCP, A2A, A2UI, AP2 and UCP, organizations can eliminate the crushing technical debt of bespoke integrations and focus entirely on orchestrating high-value business logic. This paradigm shift fundamentally elevates developers from mere mechanics wiring fragile APIs into true architects of a global, autonomous workforce."

---

## Key References

- A2A Protocol: https://a2a-protocol.org/latest/topics/extensions/
- A2UI GitHub: https://github.com/google/A2UI
- AP2 Protocol: https://ap2-protocol.org/
- UCP Integration: https://developers.google.com/merchant/ucp/guides/integration-ui/integration
- MCP Spec: https://modelcontextprotocol.io/specification/2025-11-25
- ADK Commerce Codelab: https://codelabs.developers.google.com/next26/adk-agent-commerce#0
- GCP Agent Registry: https://docs.cloud.google.com/agent-registry/register-agents
- rad-skills (rapid agent dev): https://github.com/VeerMuchandi/rad-skills
