# Capstone Synthesis + Existing-Project Fit Analysis

Companion to `00-capstone-requirements.md` (the rubric) and the 5 whitepaper notes
(`01-`..`05-`). Written 2026-06-19 for the brainstorming phase.

## 1. What the materials say the judges actually reward

From the rubric (Kaggle) + the 5 whitepapers + the NotebookLM livestream:

- **Implementation is 70%** of the score; the pitch (video+writeup) is 30%. The single
  biggest line item is **Technical Implementation (50 pts)** = architecture quality +
  *meaningful, central* use of agents + *clever use of existing toolsets*.
- **Hard gate: demonstrate ≥3 of** {ADK multi-agent, MCP server, Antigravity, security
  features, deployability, agent skills/Agents CLI}.
- **"Start simple, scale on boundaries."** Single agent + multiple skills (progressive
  disclosure); split to multi-agent only when you hit context/latency/tool-selection
  limits (~15-50 tools). Do NOT pre-build a swarm. (Livestream + New SDLC paper.)
- **Spec-driven, code-is-disposable.** Behavioral specs (Gherkin/BDD) are the durable
  source of truth; you act as architect. (SDD paper.)
- **"The trajectory is the truth."** Evaluation is the course's spine. A credible eval
  story = golden regression dataset (saved good trajectories) + trajectory-vs-output
  scoring + OpenTelemetry "flight-recorder" traces + LLM-as-judge via **pairwise**
  comparison (not 1-5) + a HITL reviewer UI + CI/CD eval gate.
- **Security = continuous "Effective Trust", not a checkbox.** Confused-Deputy defense
  (ephemeral sandbox + JIT down-scoped creds), HITL approval for high-stakes actions,
  Denial-of-Wallet (budget) defense, slopsquatting (pin deps). (Security paper.)
- **Anti-patterns to avoid:** redundant stacked agents ("more layers"), memory-as-workflow-
  controller (use DAG), thin API-wrapper tools (encapsulate high-level goals).

### The differentiation lever (specific to this user)
The user is a **Senior Product DS in Search Relevance** — evaluation IS their day job
(NDCG/MRR, experiment design, judge calibration). The course rewards eval depth and most
participants will do it shallowly. **A genuinely expert evaluation story is this user's
"wow factor."** Whatever project we pick, the eval harness should be the showpiece.

## 2. Reality constraints
- **17 days** (announce 6/19 → due 7/6 23:59 PT). Solo. Vibe-coding skill level
  (prompt-driven, limited debugging) → favor a project with a working head start and
  lean on specs + the eval harness over hand-written code.
- Must end with a **public repo + public demo/code (no login/paywall)** + ≤5-min YouTube
  video + ≤2,500-word Writeup + cover image.
- Course is **Google-stack**: ADK (Agent Dev Kit), Antigravity (IDE), Agents CLI, MCP.
  "Adapting" any project ≈ re-architecting around ADK+MCP + showing Antigravity in video.

## 3. Project fit scoring (all ~15 projects surveyed; top candidates detailed)

Legend: ●=strong ◐=partial ○=weak/none.

| Project | Agentic? | Head start (code) | Public-demoable | Concept coverage (of 6) | Eval-story potential | 17-day feasible | Track |
|---|---|---|---|---|---|---|---|
| **reward-ticket** | ● autonomous monitor + browser-use | ● v0.1 running + v0.2/0.3 scaffold | ◐ (local-only now → publish + sanitize creds) | ● ADK, MCP(flight tools), security(HITL/budget), deploy(daemon), evals | ● golden award-state set + browser-use trajectory eval | ● (extend, not build) | Concierge |
| **AI Writing Suite** | ◐ skill suite (passive, not autonomous) | ● mature, published plugins, CI | ● already public OSS | ● Agent skills✓✓, MCP, evals✓, security | ● already has LLM-judge + calibration band | ● lowest effort | Business |
| **PAA health coach** | ● clearly agentic (memory, tools, schedule) | ○ scaffold only (stubs) | ◐ personal data; demo with sample user | ● ADK, MCP(Garmin/Gmail), security(health privacy), deploy(launchd) | ◐ coaching-quality eval (outcomes slow) | ◐ big build from scaffold | Concierge/Good |
| **travel-agent** | ● literally a travel agent | ◐ active/hot, state in flux | ◐ depends | ● ADK, MCP, deploy | ◐ | ◐ (conflicts w/ active work?) | Concierge |
| **SMA v2** | ◐ orchestrator skill | ● mature, 420 tests | ○ in-house (Databricks/Confluence/Bitbucket) | ◐ Agent skills, evals✓✓ | ● expert LLM-judge already | ◐ but public-demo hard | Business |
| **autorefine** | ◐ meta (improves skills) | ● mature | ◐ abstract value | ◐ Agent skills, evals✓✓ | ● | ◐ | Business |
| **ASE search-eval** | ○ eval framework, not an agent | ○ design only, no repo | ◐ | ○ | ●● (your domain) | ○ build from zero | Business |
| **ds-brainstorm-agent** | ● multi-persona = multi-agent | ○ scaffold | ● | ● ADK✓✓ multi-agent | ◐ | ◐ build from scaffold | Business/Good |
| Writing Vault / Outpace / Water Bottle / Maven / DS Career / DS Teaching | ○/◐ | varies | varies | ○ | ○ | — | weak fit / dormant / done |

## 4. Recommendation

**Primary: reward-ticket.** Best balance of (a) a *working, genuinely autonomous* agent
with a real head start, (b) a clear, public-demoable, relatable real-world outcome
(find me award business-class seats SFO↔Tokyo), (c) natural coverage of ≥3 required
concepts, (d) it already embodies course safety principles (no-auto-book = HITL,
$2/day budget = Denial-of-Wallet defense), and (e) a strong eval-story surface (golden
award-state dataset + browser-use trajectory eval) where the user's evaluation expertise
becomes the wow factor. Concierge track. Main adaptation cost: re-architect around
ADK+MCP, build the eval harness, publish (sanitize the OpenRouter/Telegram creds).

**Close second: AI Writing Suite** — lowest effort, "Agent skills" nailed, eval harness
exists; but risks reading as a *skill/tool* rather than an autonomous *agent* the judges
expect. **Third: PAA** — highest "wow" but a near-from-scratch build, risky in 17 days.

> Final call is the user's (product owner). Pick drives the rest of the brainstorm.
