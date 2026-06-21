# Engagement-Weighted Demand Research — Kaggle Capstone Agent Project

Written 2026-06-19 for the brainstorming phase. Companion to `00-capstone-requirements.md`
(rubric), `10-synthesis-and-project-fit.md` (project-fit scoring), and the 6 scout notes
(`scout-*.md`). Synthesis style borrows `/last30days`: cluster cross-source duplicates,
RANK by real engagement (upvotes / HN points / stars / X likes), cap ~3 items per
author/thread so one loud voice does not dominate, cite every source.

---

## 1. Methods & Sources (with thin-data / failure flags)

Six independent scouts (mid-May → mid-June 2026), ~80 raw signals. Tools: `opencli`
(Reddit/HN full-thread reads), `twitter` CLI, WebFetch/WebSearch (HN Algolia, Product
Hunt, GitHub trending, ossinsight, analyst surveys).

**Flags — sources/queries that returned thin or failed data (discount accordingly):**
- **r/fitness** returned 0 hits for "AI coach" / "wish app" (auth/strictness) — fitness-AI
  demand under-sampled; PAA's core sub-vertical is likely *under*-counted here.
- **X article bodies** hit HTTP 402 (paywalled) — X signals derived from tweet text +
  engagement metadata only, not full article content. Likes/bookmarks still reliable.
- **WebFetch budget cap** hit at call 16 on the Product Hunt/Google scout — later PH
  follower counts are single-fetch, not cross-validated; treat PH follower numbers as
  softer than Reddit/HN/GitHub raw counts.
- **HN raw points are the strongest currency** (open voting, dev-skeptical audience).
  GitHub weekly-star deltas are strong but trend-chasey. PH followers are weakest (launch
  hype). Reddit upvotes mid-strength. X likes inflated by reach — I weight bookmarks
  (intent-to-build) over likes.
- **Per-thread cap applied:** the r/Entrepreneur/1tvildd thread (124 up / 178 comments)
  and r/ChatGPT/1tolh94 (380 up / 310 comments) each spawned 4-6 sub-signals. I cluster
  each thread as ONE theme contributor and cite its top 2-3 comments, so a single viral
  thread cannot manufacture a fake "theme."

---

## 2. Ranked Demand Themes (engagement-weighted, cross-source clustered)

Ranked by strongest single engagement number in the cluster, then by cross-source breadth.

| # | Theme | Track | Strength | Top engagement (cited) | Why now / so-what | Example agent |
|---|---|---|---|---|---|---|
| **T1** | **Agent reliability / guardrails / cost-circuit-breakers** — stop runaway, cascading, or bankrupting agents | Business | **HIGH** | HN **1,466 pts / 534 comments** (agent bankrupted operator scanning DN42, top HN story of the month); HN 687/252 (Forge: guardrails 8B 53%→99%); HN 860/1,032 (agent deleted prod DB); HN 552/245 (Fedora amok); Reddit r/Entrepreneur 37-40 up / 97 comments ("80% works, nobody trusts it"); Forrester 49% of security leaders cite agentic AI as top concern | Capability isn't the bottleneck — **trust is**. "90% per-step → 40% failure over 5 steps." This is the #1 pain across HN + Reddit-business + analyst surveys, and it is **exactly an evaluation problem.** | Reliability wrapper: per-step trajectory eval + drift detection + budget circuit-breaker + HITL escalation before irreversible actions |
| **T2** | **Persistent cross-session agent memory** — stop "starting from zero" every session | Business / Concierge | **HIGH** | GitHub: claude-mem **83k stars**, mem0 58k, agentmemory **+6,900 stars/week** (rank 5 trending); X article "Burning Money Every Time It Starts From Zero"; Reddit r/QuantifiedSelf 11/20 ("re-pasting my whole setup… never builds on last week"); graphiti 27k | Memory is the most-starred agent primitive on GitHub right now. Every personal-agent thread independently re-derives the need. Cheap to demo, expensive to do *well* (eval of memory recall = your edge). | Agent with a queryable persistent memory store + eval of "did it correctly recall/apply prior context" |
| **T3** | **Autonomous personal life-orchestration** — meal/schedule/shopping/cognitive-load offload that fires on its own | Concierge | **HIGH** | Reddit r/ChatGPT/1tolh94 **380 up / 310 comments**; top comment 229 up ("Sunday agent → menu → shopping list, game changer"); daycare-waitlist comment **197 up** ("please share how"); "I'd pay someone to set this up"; PH: Bond ("to-do list that does itself") 1.4K followers | Highest-engagement *consumer* agent thread in the set. Revealed preference is strong (people DIY-build it). Maps cleanly to Concierge + privacy-first framing. | Weekly autonomous household orchestrator: reads calendar/weather/inventory → proposes plan → HITL approve → executes shopping list |
| **T4** | **ADHD / accountability execution agent** — externalize executive function, define "done", hold stakes | Concierge / Good | **HIGH** | Reddit r/ADHD: "define done in one testable sentence" **213 up / 107 comments**; "mental narrator that tells me what to do" 67 up / 204 comments (top comment 53); "understand executive dysfunction not motivation-speak" 53/52; r/getdisciplined public-progress streak 102/68 | Deep, emotional, repeated demand for an agent that *holds you to a behavioral contract* — not a tracker. Strong overlap with PAA's coaching loop. Privacy-sensitive (Concierge fit). | Accountability coach: forces one-sentence "done", daily check-in, escalating nudges, visible streak |
| **T5** | **Open-source / self-hosted coding agents & dev harness** — full-codebase context, scoped job-packets, no babysitting | Business / Freestyle | **HIGH** | GitHub: OpenCode **172k stars**, OpenHands 60k+ (Series A), Cline 63k; X SemiAnalysis **6,139 likes / 3.5M views** (throughput-per-dollar); X omarsar0 734/207k (autonomous long-running); Reddit r/ExperiencedDevs 66/127 ("scope drift burnout", top comment 154); X addyosmani 1,608 likes / 3,150 bookmarks (agentic code review) | Largest raw star counts in the set, but **crowded** — competing here means beating 172k-star incumbents. Better as a *technique* (job-packet + eval gate) than a product. | Dev-agent harness that scopes to a job packet + verified-PR eval gate (anti scope-drift) |
| **T6** | **Private / local-first personal AI with device + messaging access** | Concierge | **HIGH** | GitHub: OpenClaw **210k+ stars (fastest repo ever to 100k)**, openhuman +17,100 stars/week (rank 2), Ollama 147k; HN Moltworker 246/71; HN "surveillance nightmare" warning 349/104 | Privacy-first personal agent is a top-3 GitHub theme AND the explicit framing of the Concierge track. Demoability risk: connecting real WhatsApp/iMessage is heavy for 17 days. | Local-first personal agent with user-owned memory + one messaging channel (Telegram) |
| **T7** | **Agent observability / audit trail / action logging** — verifiable record of what the agent did | Business | **HIGH** | HN 386/162 (permission-fatigue game); Reddit r/artificial 44/45 (audit trail); Forrester "every action logged & defensible, cost too high"; PH Brief 264 up (context for humans+agents); HN A2A 91/41 (no way to validate agents work as advertised) | Sibling of T1 — the *evidence layer* that makes reliability provable. This is a trajectory-logging + eval-replay problem = your domain. | Flight-recorder: OTel trajectory log + replay + "did it do what it claimed" verifier |
| **T8** | **Pilot→production scaling gap: eval infra + monitoring + ownership** | Business | **HIGH** | Surveys: 78% have pilots / **only 14% scaled** (DigitalApplied); Forrester 79% adopt / 11% in prod; DataRobot 413 practitioners: 72% say *operating* costs more than building, 94% Day-2 ops issues; Reddit r/Entrepreneur governance 85/96 ("mystery glue waiting to break") | The enterprise money is in the 14%→production gap, and the gap IS eval + monitoring + governance. Direct match to user's eval expertise but hard to *demo* publicly (enterprise data). | Eval-gate + governance layer: golden regression set + CI eval gate + ownership/rollback docs |
| **T9** | **Research-at-scale agent** — read the internet/sources and synthesize, not just enrich | Good / Business | **MEDIUM-HIGH** | GitHub academic-research-skills **+11,600 stars/week (rank 3)**, DeerFlow 2.0 70k (#1 trending Feb); Reddit r/SideProject 35/24 ("go read the internet and think"); career-ops 54.8k | Strong GitHub pull; "research" generalizes (job search, lead research, lit review). Eval angle: factuality/citation scoring — your wheelhouse. | Multi-source research agent with citation-grounded synthesis + factuality eval |
| **T10** | **Personal health-context manager** — persistent health history as informed intermediary w/ doctors | Good / Concierge | **MEDIUM-HIGH** | Reddit r/loseit plateau diagnostic **162 up / 182 comments** (+ adjacent sleep-stall 157/117); r/ChatGPT "elite doctor who knows my context" 19 up / insomnia-cured story 76 up; r/QuantifiedSelf cross-silo "Sage" 7/37; food-logging void 272/174 | Health is high-stakes, high-engagement, privacy-sensitive. **Directly adjacent to PAA.** Plateau/data-diagnostic is a *reasoning-over-personal-data* problem with a measurable answer = evaluable. fitness-AI under-sampled (r/fitness failed) so likely *understated*. | Health-context agent: ingests labs/wearable/logs, runs cross-silo diagnostics (plateau root-cause), persistent memory |
| **T11** | **Job-search "Jarvis"** — profile→market→prioritize→auto-apply (gated)→track→handback | Good | **MEDIUM-HIGH** | Reddit r/SideProject/1twszph **819 up / 215 comments**; GitHub career-ops 54.8k stars | One of the highest single consumer-agent threads; clear orchestration story. Crowded incumbents (career-ops). Demoable. | Job-search orchestrator with HITL apply-gate + outcome tracking |
| **T12** | **Business comms / outreach / CRM-context automation** — monitor signals, draft context-aware outreach, update CRM | Business | **MEDIUM** | Reddit r/Entrepreneur/1tvildd cluster **124 up / 178 comments** (CEO-podcast→CRM, monthly auto-reports 50-up comment, inbound triage); r/Entrepreneur CRM-outreach 69/65; X AravSrinivas context-graphs 949/101k | This is **AI Writing Suite's territory** (context-aware drafting). Solid but mid-engagement; capped (one viral thread drives most of it). | Outreach agent: signal monitor → context-aware draft (voice-matched) → HITL send → CRM update |
| **T13** | **Voice / phone / scheduling agent for solo businesses** | Concierge / Good | **MEDIUM** | PH ElevenLabs 4.9★/188 reviews, Deepgram 4.9★/70; solopreneur research $24-60K VA replacement, 15-20 hrs/wk saved; Fundraisly 2.2K PH followers | Real money signal but voice latency infra is heavy and off your eval edge. Skip for a 17-day solo build. | Low-latency voice receptionist (out of scope — infra-heavy) |
| **T14** | **Browser-use / computer-use agents** — eyes+hands on the web without APIs | Business / Concierge | **MEDIUM** | GitHub browser-use **99k stars**, CloakBrowser +7,000/wk, stagehand 23k; X jxnlco computer-use 705/356k views | Powerful enabler but a *capability*, not a project; demoable but fragile. Useful as a *tool* inside another agent. | (Tool layer, not standalone project) |
| **T15** | **Emotional/delight desktop companion** — non-utilitarian presence layer | Freestyle | **MEDIUM (outlier)** | Reddit r/SideProject **1,322 up / 405 comments**, $150 day-1 revenue | Huge engagement but a novelty/delight play — no eval story, off-brief for a DS differentiator. Note as a cautionary "engagement ≠ fit" data point. | (Off-strategy for this user) |

---

## 3. Track Map (where the engagement concentrates)

- **Agents for Business** — by far the deepest + highest-engagement pool: T1 reliability,
  T2 memory, T5 dev-harness, T7 observability, T8 pilot→prod, T12 comms. The HN/analyst
  money-and-trust signals all land here. **This is where eval expertise is most rewarded
  and most differentiating.**
- **Concierge Agents** — strong consumer pull: T3 life-orchestration (380-up thread),
  T4 ADHD accountability (213-up), T6 local-first private agent (210k-star OpenClaw),
  T10 health-context. Privacy-first framing is native here. **Best demoability + relatability.**
- **Agents for Good** — T11 job-search Jarvis (819-up), T9 research, T10 health,
  T4 (overlaps). Fewer but high-engagement humanitarian-adjacent signals.
- **Freestyle** — T5 dev-harness techniques, T14 computer-use, T15 desktop pet. Mostly
  techniques or novelties; weakest strategic fit unless used to showcase agent best-practices.

**Cross-cutting meta-finding:** the single loudest demand across ALL six sources is the
**trust/reliability/eval/observability cluster (T1+T7+T8)** — and that cluster is the
user's exact professional edge. Demand and differentiation point at the same place.

---

## 4. Finalist Implications

### Finalist 1 — PAA (Personal Athletic Agent) — LEAD CHOICE
- **Rides:** T4 ADHD/accountability (HIGH, 213-up "define done"), T3 life-orchestration
  (HIGH, 380-up), T10 health-context (MED-HIGH, 162-up plateau diagnostic), T2 memory
  (HIGH), T6 local-first private (HIGH). **rides_demand = STRONG** — sits on 4-5 HIGH themes
  and the demand is *consumer-emotional* (revealed-preference DIY builds), not just claimed.
  Caveat: r/fitness failed → core fitness sub-vertical under-sampled, but the *adjacent*
  accountability + plateau-diagnostic + health-context threads more than cover it.
- **Sharpened idea:** A privacy-first **body-recomposition accountability coach** whose
  showpiece is the eval harness: persistent memory of the user's logs/wearable data →
  daily coaching that (a) forces a one-sentence testable "done" (T4), (b) runs a
  **plateau root-cause diagnostic** over the user's own data when progress stalls (T10,
  the 162-up unmet need), with a **golden trajectory eval set** scoring coaching quality +
  diagnostic correctness via pairwise LLM-judge. HITL approval before any external action
  (Garmin/Gmail/Telegram). Eval = the wow factor, not the coaching prose.
- **Risk:** Scaffold-only (stubs) → biggest BUILD of the three in 17 days; coaching-outcome
  quality is slow to validate (mitigate by evaluating *trajectory/decision quality* on a
  golden set, not real weight outcomes). Personal data → demo with a synthetic sample user.

### Finalist 2 — AI Writing Suite
- **Rides:** T12 business comms/outreach (MEDIUM, capped 124-up cluster), partially T2
  (voice memory) and T8 (its eval harness fits the pilot→prod eval-gate story).
  **rides_demand = MODERATE** — real but mid-engagement, and the comms theme is the most
  per-thread-concentrated (one viral thread). It does NOT ride the loudest cluster
  (T1/T7 reliability/observability).
- **Sharpened idea:** Reframe the suite as an **autonomous outreach/comms agent** (not a
  passive skill set): a signal-monitor → voice-matched context-aware draft → HITL send →
  CRM/record update loop (T12), with its existing LLM-judge eval harness upgraded to a
  **golden regression set + pairwise judge + CI eval gate** so it tells the pilot→prod
  eval-gate story (T8). Lowest build effort, already public OSS.
- **Risk:** Judges expect an *autonomous agent*; the suite reads as a **skill/tool suite**
  (passive). The agentic reframe is the make-or-break, and it's a positioning stretch more
  than a code lift. Mid-tier demand vs PAA's emotional pull.

### Finalist 3 — SMA v2 (Search Metric Analyzer)
- **Rides:** T1 reliability/eval (HIGH), T7 observability (HIGH), T8 pilot→prod eval infra
  (HIGH), T9 research-synthesis (MED-HIGH). **rides_demand = STRONG on the *highest-value
  business cluster*** — SMA's self-improving LLM-judge eval engine is a near-literal answer
  to T1/T7/T8, the loudest+best-paying demand in the set.
- **Sharpened idea:** Generalize SMA's LLM-judge + self-improvement engine into a public
  **"agent reliability / eval-gate" demo**: point it at *any* agent's trajectory logs,
  produce a golden regression set, score trajectory-vs-output via pairwise judge, detect
  drift, and gate CI — the exact T1+T7+T8 trifecta. Maximum overlap with the user's edge.
- **Risk:** **Public-demoability is the blocker** — it's Databricks/Confluence/Bitbucket-
  bound (in-house). Generalizing to a public, login-free demo on synthetic agent traces is
  real un-coupling work, and it risks reading as *infra/tooling* rather than an agent.

---

## 5. Recommendation

**Best combined bet: PAA — but explicitly engineered as an eval-showpiece.**

PAA uniquely combines (a) **engagement-backed demand on 4-5 HIGH consumer themes**
(T3 380-up, T4 213-up, T10 162-up, T2/T6 top GitHub stars) with emotional revealed-
preference, (b) a **public-demoable, relatable, privacy-first Concierge story** (the one
track where demoability is easy and the framing is native), and (c) a clean surface for
the user's **evaluation edge** to be the wow factor.

SMA rides the higher-*value* cluster (T1/T7/T8) and is the strongest pure eval-expertise
fit, but its public-demo blocker is severe for a 17-day public-repo deliverable — making
it the higher-risk pick despite the better demand-to-expertise match. AI Writing Suite is
lowest-effort but mid-demand and fights an "is-it-actually-an-agent" perception.

**One-line sharpened concept:**
> A privacy-first body-recomposition **accountability coach** with persistent memory that
> forces a one-sentence "done," runs a **plateau root-cause diagnostic over your own data**
> when you stall, and whose showpiece is a **golden-trajectory pairwise-LLM-judge eval
> harness** scoring coaching + diagnostic quality — demand (T3/T4/T10) meets the user's
> evaluation expertise.

*Decision tradeoff for the product owner:* if you prioritize **demand-to-expertise purity
+ resume value** over demoability, SMA's reliability/eval-gate reframe is the contrarian
pick on the loudest, best-paying cluster (T1/T7/T8) — but you must solve the public-demo
un-coupling first. PAA is the lower-risk, higher-relatability default.
