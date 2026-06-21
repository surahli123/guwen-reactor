# Sharpened Idea Slate — Kaggle Capstone (solo, 17 days, eval-as-wow)

Built from `20-demand-research.md` (engagement-ranked demand) + `00-capstone-requirements.md`
(rubric) + the 5 whitepaper notes. Strategic throughline: the loudest demand (T1/T7/T8
reliability+eval+observability) == the user's professional edge == the course's most-rewarded
concepts. So **the evaluation / trust layer is the wow in EVERY option**; the vertical is
chosen for demoability + relatability + motivation.

Hard gate reminder: must demonstrate ≥3 of {ADK multi-agent | MCP server | Antigravity |
security | deployability | agent skills(Agents CLI)}. Rubric: Impl+docs 70%, pitch 30%.

---

## Option A — "A Coach You Can Audit" (Concierge / Agents for Good)  ★ Recommended (balanced)
**What:** A privacy-first personal **accountability + health-context coach**. Persistent
memory of the user's logs/wearable/calendar. Daily loop: forces a one-sentence *testable*
"done" (T4), and when progress stalls runs a **plateau root-cause diagnostic over the
user's own data** (T10, the 162-up unmet need). HITL approval before any external action.
**Wow = the eval harness:** golden trajectory set + pairwise LLM-judge scoring coaching
quality, diagnostic correctness, and memory recall; "glass-box" trajectory view.
**Rides demand:** T3 (380-up), T4 (213-up), T10 (162-up), T2/T6 (top GitHub). STRONG, consumer-emotional.
**Existing asset:** PAA scaffold (memory, modular prompts, Garmin/Gmail/Telegram, scheduling) — partial reuse.
**≥3 concepts:** ADK (single agent + skills) · MCP (wearable/calendar/log tools) · Security (personal-data privacy + HITL + budget cap) · Deployability (scheduled daemon) · Agent skills (Agents CLI) · **Evaluation** (the showpiece). → hits 4-5.
**5-min demo:** synthetic user "stalls" → agent detects plateau, diagnoses root cause from data, proposes a testable next step, asks HITL approval → show the eval dashboard scoring its trajectory.
**Solo/17-day:** Feasible. Single agent + 3-4 skills + Telegram + synthetic data. Biggest build of the reuse options but scaffold + spec exist.
**Risk:** PAA is scaffold-only (most code to write); coaching outcomes slow → evaluate *trajectory/decision quality* on a golden set, not real weight loss.

## Option B — "Agent Flight-Recorder / Reliability Gate" (Agents for Business / Freestyle)  ◆ Contrarian, highest expertise-purity
**What:** A public **agent-reliability + eval harness**: point it at any agent's run →
capture an OpenTelemetry **trajectory log** → build a golden regression set → **pairwise
LLM-judge** scores trajectory-vs-output → drift detection + **budget circuit-breaker** +
**HITL escalation before irreversible actions** → **CI eval gate** that blocks a bad deploy.
Ship it WITH a small demo agent it supervises, so there's a clear "agent" + its safety net.
This is "agent-as-judge" (explicitly a course concept).
**Rides demand:** T1 (HN 1,466), T7, T8 — the loudest + best-paying cluster. STRONG.
**Existing asset:** SMA's LLM-judge + self-improvement engine (generalize/decouple from in-house Databricks).
**≥3 concepts:** **Evaluation** · Security (circuit-breaker/HITL/guardrails) · Deployability (CI gate) · Observability(OTel) · MCP (expose the verifier as a tool). → hits 4-5, and they're the highest-value ones.
**5-min demo:** let a demo agent go off-rails (try to delete data / loop) → flight-recorder catches it, circuit-breaker fires, HITL prompt; then show golden-set regression + CI gate blocking a regression.
**Solo/17-day:** Feasible IF scoped to one demo agent + synthetic traces. Pure eval/infra = your wheelhouse → fast for you.
**Risk:** "Is it an agent?" perception (mitigate by bundling the supervised demo agent). Public-demo decoupling from in-house SMA is real work. Most abstract 5-min story.

## Option C — "Research Agent with a Factuality Scorecard" (Agents for Good / Business)
**What:** A multi-source research/synthesis agent (read sources → grounded synthesis with
inline citations) whose wow is a **factuality + citation-precision/recall eval** (your exact
metric toolkit). Generalizes to lit-review / market-research / due-diligence.
**Rides demand:** T9 (academic-research-skills +11,600 stars/wk; DeerFlow 70k). MED-HIGH.
**Existing asset:** none direct (closest: your deep-research-tiered workflow patterns) → more greenfield.
**≥3 concepts:** ADK · MCP (search/fetch tools) · **Evaluation** (factuality/citation scoring) · Deployability. → hits 3-4.
**5-min demo:** ask a research question → agent returns cited synthesis → show the scorecard (citation precision/recall, unsupported-claim flags) vs a no-eval baseline.
**Solo/17-day:** Feasible; clean scope. But crowded space; differentiation = the eval rigor.
**Risk:** Crowded; less "personal/wow" pull than A; more to build than B/D.

## Option D — "Autonomous Outreach Agent" (Agents for Business)  — lowest build effort
**What:** Reframe **AI Writing Suite** from a passive skill set into an autonomous agent:
signal-monitor → voice-matched context-aware draft → **HITL send** → CRM/record update.
Upgrade its existing LLM-judge eval into a **golden regression set + pairwise judge + CI
eval gate** (tells the T8 pilot→prod story).
**Rides demand:** T12 (124-up cluster). MODERATE (most per-thread-concentrated theme).
**Existing asset:** AI Writing Suite (mature, already public OSS, eval harness exists) — biggest head start.
**≥3 concepts:** Agent skills (Agents CLI) ✓✓ · MCP · **Evaluation** · Security(HITL/secrets). → hits 3-4.
**5-min demo:** new signal arrives → agent drafts voice-matched outreach → HITL approve → logs to CRM; show eval gate catching a quality regression.
**Solo/17-day:** Most feasible (least new code).
**Risk:** "Is it an agent?" (passive-suite perception); mid-tier demand; weakest emotional/wow pull.

---

## Quick compare

| | Demand | Expertise-fit (eval) | Demoability | Solo 17-day effort | "Clearly an agent?" | Asset head-start |
|---|---|---|---|---|---|---|
| **A Coach-you-can-audit** | High (consumer) | High | High | Med-High | Yes | PAA (partial) |
| **B Reliability gate** | Highest ($/trust) | Highest | Medium | Med (fast for you) | Needs bundling | SMA engine |
| **C Research+factuality** | Med-High | High | High | Medium | Yes | ~none |
| **D Outreach agent** | Medium | Med | High | Lowest | Stretch | Writing Suite (most) |

## Recommendation
**A** is the balanced pick (demand + demoable + eval-wow + relatable + reuses PAA). **B** is
the high-ceiling contrarian that most purely fuses the #1 demand with your resume/expertise,
at the cost of demoability + decoupling work. A can *absorb B's eval/reliability layer as
its showpiece* — so a strong default is "A vertical, B-grade eval harness." Pick the vertical
for what you'll enjoy demoing; the eval layer is the wow either way.
