# 40 — Expanded Idea Slate (12 NEW ideas beyond A/B/C/D)

Built 2026-06-19 from the freshly-mined Reddit pains (6 domains) + prior demand themes
T1-T15. These are ADDITIONAL to the 4 existing candidates (A coach-you-can-audit,
B reliability-gate, C research+factuality, D outreach agent) — no rehashes.

Strategic throughline (unchanged): the user is a Senior Product DS in Search Relevance,
so **evaluation is the showpiece in every idea**. Each idea below names a concrete
`eval_wow` that puts ranking/judge/precision-recall expertise on display.

Hard gate: each idea plausibly demonstrates ≥3 of {ADK multi-agent, MCP server,
Antigravity, security features, deployability, agent skills/Agents CLI, evaluation}.

---

## Methods note (source quality + caveats)

- **Strongest signal** comes from the Health and Money/Admin/Bureaucracy domains — many
  threads in the 400-5,346 upvote range with hundreds of comments, plus structural
  corroboration (IRS service-level stats, USDA SNAP-recert research). These pains are
  loud, recurring, and emotionally charged → good demo material.
- **Home/Family** is dominated by meal-planning + parental-load pains (788-5,346 upvotes)
  but is **crowded** (Mealime, Whisk, dozens of meal-plan apps) — differentiation must
  be the eval rigor, not the feature.
- **Niche/Creative/Accessibility** has lower raw upvotes (most 25-352) but extremely high
  *specificity* and almost zero competition → whitespace, though demo-relatability varies.
- **Thin/failed sources flagged:** reddit.com blocked WebFetch across all scouts, so NO
  thread deep-dives — engagement counts are from search-result metadata, not full-thread
  reads, so treat comment-sentiment as inferred. opencli errored on complex OR queries
  (niche, business domains) → fell back to single-term queries + WebSearch; breadth in
  those two domains is slightly under-sampled. The LMS-fragmentation student pain and the
  email-drip and PDF-report work pains are "aggregated/recurring pattern, no single viral
  thread" — weaker evidence, used only as supporting not anchor pains.
- **Eval-fit lens:** I prioritized pains where ground truth is *checkable* (a benefits
  eligibility threshold, an EOB arithmetic error, a phantom-record hallucination, a
  pronunciation phoneme) because that is where the user's evaluation expertise produces a
  defensible, demoable scorecard rather than a vibes-based "the coach felt helpful."

---

## Pain → Idea table (12 new ideas)

| # | Idea | Track | Anchor pain (engagement) | Eval wow | Whitespace |
|---|---|---|---|---|---|
| E1 | BenefitsFinder (no-as-starting-point) | Good | SNAP/Medicaid/LIHEAP unclaimed (1,146↑/62c r/povertyfinance) | Eligibility precision/recall vs hand-labeled gold cases; calibrated "qualify?" confidence | whitespace |
| E2 | EOB/Claim Auditor | Concierge | Can't audit adjuster/EOB math (103c r/Insurance; weekly threads) | Discrepancy detection precision/recall + arithmetic-trap test suite | whitespace |
| E3 | RecordKeeper (anti-hallucination genealogy) | Good | AI fabricates genealogy records (148↑/93c + 109↑/43c r/Genealogy) | Hallucination/fabrication rate as the headline metric; abstention calibration | whitespace |
| E4 | TaxUnfreeze (back-taxes for gig/cash) | Good | Gig workers frozen for years (150↑/160c r/tax; 7-yr non-filer) | Schedule-C categorization accuracy + deduction recall vs labeled bank-tx set | moderate |
| E5 | PantryBrain (waste-minimizing meal agent) | Concierge | Meal planning waste + day-3 boredom (788↑/78c r/mealprep) | Ingredient-overlap optimization scored vs baseline; waste %; variety entropy | crowded |
| E6 | FamilyOps morning-briefing concierge | Concierge | Invisible parental mental load (5,346↑/842c r/Parenting viral) | Action-item extraction precision/recall from messy inbox/forms; "missed deadline" recall | moderate |
| E7 | FluencyCoach (live speaking eval) | Good | Apps give zero pronunciation/fluency feedback (2,468↑/772c r/languagelearning) | Phoneme-error detection accuracy vs native-labeled audio; top-5 error ranking | moderate |
| E8 | LitReview Synthesizer w/ contradiction-finder | Good | Lit review = months of manual slog (473↑+146↑ r/GradSchool) | Citation precision/recall + contradiction-detection F1 vs annotated corpus | crowded |
| E9 | A11y Regression Sentinel (screen-reader QA) | Good | A11y regressions ship, no blind QA (61↑/46c r/Blind) | Regression-catch rate vs seeded WCAG defects; severity-ranking quality | whitespace |
| E10 | ContractorVet (license + fraud due-diligence) | Business | Contractor vetting adversarial (1,816↑/464c r/HomeImprovement) | Red-flag detection precision/recall + scope-fraud (shingle-class) catch rate | whitespace |
| E11 | GrantPipeline (win-prob scoring) | Business | NPO grant writers burn out, can't pick funders (49↑/38c r/nonprofit) | Win-probability calibration (Brier/AUC) on historical award data; mission-fit ranking | moderate |
| E12 | DashboardKiller (proactive insight agent) | Business | 47 dashboards nobody reads (446↑/90c + 714↑/165c r/analytics, r/datascience) | Anomaly-alert precision/recall + "did stakeholder act?" downstream eval; alert-fatigue tuning | moderate |

---

## Full idea cards

### E1 — BenefitsFinder (Agents for Good)
**One-liner:** Given income/household/state, an agent maps every SNAP/Medicaid/LIHEAP/
ACA/CHIP/WIC program the user qualifies for, ranks by $ value, drafts applications, and
sets recert reminders — treating "no" as its starting point.
**Pain evidence:** "I left probably thousands of dollars on the table over three years"
— 1,146↑/62c, r/povertyfinance (highest-signal money pain). Recert-churn corroborated by
USDA research.
**Eval wow:** This is a *ranked-retrieval* problem in disguise — the user's home turf.
Build a hand-labeled gold set of synthetic households → score eligibility **precision/
recall** per program, **calibrated confidence** on each "you qualify," and rank programs
by expected $ (a relevance-ranking metric). Baseline = naive keyword match; show the lift.
**Concepts:** ADK (eligibility agent + form-drafting agent) · MCP (state-threshold lookup
tool) · Evaluation (showpiece) · Security (PII handling, HITL before any submission) ·
Deployability (recert reminder daemon). → 5.
**Solo feasibility:** high — thresholds are public, rules are tabular, no live gov APIs
needed for v1 (rules-as-data). **Existing asset:** greenfield (PAA scheduling reusable for
recert reminders). **Demoability:** high — "this family was leaving $4,200/yr on the
table." **Whitespace:** whitespace (Benefits.gov screener exists but is shallow,
non-agentic, no drafting/reminders).

### E2 — EOB / Claim Auditor (Concierge)
**One-liner:** Parse Explanation-of-Benefits PDFs + provider invoices into a line-item
ledger, flag arithmetic errors / retroactive offsets / balance-billing violations, and
draft appeal letters citing policy language.
**Pain evidence:** "changing reimbursement figures, arithmetic/transposition errors,
retroactive offsets... calculations that seemed to shift repeatedly" — r/Insurance, 3
threads 10-103c; "phantom insurer" EOB confusion weekly across r/Insurance + r/pf.
**Eval wow:** Ground truth is *objective math* → build a test suite of EOBs with **seeded
arithmetic traps** (transpositions, off-by-allowed, duplicate denied-then-approved) and
score **discrepancy-detection precision/recall**. This is the cleanest "broken-ruler-
proof" eval in the slate: false positives (crying wolf) vs false negatives (missed
overcharge) is a precision/recall tradeoff you can plot.
**Concepts:** ADK (parser agent + auditor agent + letter-drafter) · MCP (PDF/OCR tool) ·
Evaluation · Security (health-financial PII, HITL on letters) · Deployability. → 4-5.
**Solo feasibility:** high — synthetic EOBs are easy to generate with known ground truth.
**Existing asset:** greenfield. **Demoability:** very high — "the agent caught a $1,300
balance-billing violation the adjuster buried." **Whitespace:** whitespace.

### E3 — RecordKeeper: anti-hallucination genealogy transcriber (Agents for Good)
**One-liner:** Transcribe handwritten historical records (Kurrent/Gothic/Cyrillic),
cross-verify across 2+ models, flag low-confidence words, and NEVER auto-write to the
family tree without per-field confirmation.
**Pain evidence:** "It told me my great grandfather was in the CIRCUS... Entire families,
towns, dates — all fake" — 148↑/93c + 109↑/43c, r/Genealogy. Users copy fabrications into
shared trees before noticing.
**Eval wow:** The headline metric is literally **hallucination/fabrication rate** — and
the wow is **abstention calibration** (does the agent say "I don't know" exactly when it
should?). Build a gold set of transcribed records → measure fabrication rate, word-error-
rate, and the precision/recall of the low-confidence flag. This directly answers the
course's "trajectory is the truth" + factuality theme with a uniquely measurable harm.
**Concepts:** ADK (multi-model cross-verify = genuine multi-agent need) · MCP (OCR/archive
tools) · Evaluation · Security (never-auto-write guardrail = confused-deputy defense). → 4.
**Solo feasibility:** medium (handwriting models are fiddly; scope to one script + a small
gold set). **Existing asset:** greenfield (overlaps C's factuality harness — could reuse C's
scorer). **Demoability:** high — show it refusing to fabricate where ChatGPT confabulates.
**Whitespace:** whitespace (Transkribus exists but has no abstention/verification layer —
that's the exact gap users complain about).

### E4 — TaxUnfreeze: back-taxes agent for gig/cash workers (Agents for Good)
**One-liner:** Ingest bank statements → categorize income/expenses → draft Schedule C →
compute quarterly estimates → flag likely deductions → set deadline reminders, for the
self-employed who froze for years out of confusion.
**Pain evidence:** "Every time I tried to file I got confused and was afraid I was filling
it out wrong" — 150↑/160c r/tax; "Dancer haven't filed for 7 years."
**Eval wow:** Transaction categorization is a **classification problem with a confusion
matrix** — build a labeled bank-transaction set → score per-category precision/recall,
**deduction recall** (did it find the legit write-offs?), and a precision floor (no
fabricated deductions = audit risk). Cost-sensitive eval: a missed deduction vs a bogus
one have asymmetric penalties — exactly the kind of asymmetric-loss eval the user can
showcase.
**Concepts:** ADK (categorizer + form-drafter + estimator) · MCP (statement parser) ·
Evaluation · Security (financial PII, HITL, "not tax advice" guardrail) · Deployability. → 5.
**Solo feasibility:** medium-high (Schedule C logic is bounded; synthetic statements with
labels are buildable). **Existing asset:** greenfield. **Demoability:** high. **Whitespace:**
moderate (TurboTax/Keeper exist but the *frozen non-filer* + back-years niche is underserved).

### E5 — PantryBrain: waste-minimizing meal agent (Concierge)
**One-liner:** Ingest pantry photo + family preferences + budget → generate a themed
weekly plan that maximizes ingredient overlap, rotates cuisine profiles to beat day-3
boredom, and emits a de-duplicated store-section grocery list.
**Pain evidence:** "giant shopping list, half-used ingredients... fridge full of food my
kids aren't excited about by Wednesday" — 788↑/78c r/mealprep; "by day 3 I'm already
tired of eating it" (takeout relapse).
**Eval wow:** This is an **optimization problem with measurable objectives** — score plans
on **ingredient-overlap ratio, projected food-waste %, budget adherence, and variety
entropy** vs a naive baseline. You can run an offline "tournament" (pairwise LLM-judge on
plan quality) AND a hard-metric eval — a rare double where subjective + objective evals
co-exist, letting the user show both.
**Concepts:** ADK (planner + grocery-optimizer) · MCP (pantry-vision / recipe DB tool) ·
Evaluation · Deployability (weekly cron). → 4.
**Solo feasibility:** high. **Existing asset:** greenfield. **Demoability:** very high,
universally relatable. **Whitespace:** crowded (Mealime/Whisk/Samsung Food) — differentiation
is ONLY the optimization-eval rigor, which is risky as a wow but plays to the user's strength.

### E6 — FamilyOps: parental-load morning-briefing concierge (Concierge)
**One-liner:** A family concierge that holds a running list of school deadlines, appts,
permission slips, camp/activity registrations — surfaces "action needed" in a daily
morning briefing and drafts the emails/forms.
**Pain evidence:** "zero time left for actual family connection... the stress is
relentless" — 5,346↑/842c r/Parenting (viral); summer-logistics 2,311↑/252c.
**Eval wow:** The hard part is **information extraction from messy inputs** (forwarded
school emails, photographed forms). Build a gold set of realistic inbox/forms → score
**action-item extraction precision/recall** and, critically, **deadline-miss recall**
(the cost function: a missed permission slip is catastrophic, a false alarm is cheap →
recall-weighted eval). Add a "morning briefing quality" pairwise judge.
**Concepts:** ADK (extractor + briefer + drafter) · MCP (Gmail/Calendar tools — already in
PAA) · Evaluation · Security (family PII, HITL on sends) · Deployability (morning cron). → 5.
**Solo feasibility:** medium-high. **Existing asset:** PAA (Gmail/Telegram/scheduling) — strong
partial reuse. **Demoability:** high. **Whitespace:** moderate (Maple/Skylight exist but are
calendars, not extraction agents).

### E7 — FluencyCoach: live speaking eval (Agents for Good)
**One-liner:** Conduct live target-language speaking sessions, transcribe + analyze
phoneme-level errors, identify the learner's top-5 recurring pronunciation issues, and
generate targeted repeat-after-me drills.
**Pain evidence:** "341-day Duolingo streak and I sat through dinner nearly silent for
five hours" — 2,468↑/772c r/languagelearning; "shamed in Munich by native speakers"
(142↑/107c). No mainstream app gives spoken feedback.
**Eval wow:** Pronunciation scoring is a **measurement-validity problem** — does the
agent's phoneme-error judgment agree with human native-speaker labels? Build a small
native-labeled audio gold set → report **phoneme-error detection accuracy + the top-5
error-ranking quality (NDCG-style)**. The user's judge-calibration expertise is the
showpiece: "does my automated scorer agree with the human ground truth, and where does it
systematically err?"
**Concepts:** ADK (conversation agent + analyzer) · MCP (ASR/TTS tools) · Evaluation ·
Deployability. → 4.
**Solo feasibility:** medium (ASR phoneme alignment is fiddly; scope to one language +
small gold set). **Existing asset:** greenfield. **Demoability:** very high (live demo).
**Whitespace:** moderate (Speak/ELSA exist but are closed; the eval-transparency angle is open).

### E8 — LitReview Synthesizer with contradiction-finder (Agents for Good)
**One-liner:** Take a research question → fan out across Semantic Scholar/PubMed/arXiv →
cluster by theme/method/finding → surface contradictions AND consensus → draft a cited
literature narrative.
**Pain evidence:** "jumping between documents and tabs... finding missing articles in my
messy knowledge base" — 473↑/19c + 146↑/25c r/GradSchool; method-choice-opacity pain
561↑/193c r/PhD.
**Eval wow:** Two checkable metrics: **citation precision/recall** (the user's exact
toolkit) AND **contradiction-detection F1** against an annotated corpus where you've
labeled which papers actually disagree. The contradiction-finder is the differentiator —
most lit-review tools summarize; scoring "did it correctly identify that paper A's finding
contradicts paper B" is a novel, defensible eval.
**Concepts:** ADK (search + cluster + synthesize agents) · MCP (Semantic Scholar/arXiv
tools) · Evaluation · Deployability. → 4.
**Solo feasibility:** medium. **Existing asset:** overlaps candidate C heavily — this is C's
*academic vertical* with a contradiction twist; could be folded into C rather than separate.
**Demoability:** high. **Whitespace:** crowded (Elicit/SciSpace/Consensus) — contradiction-F1
eval is the only real wedge.

### E9 — A11y Regression Sentinel: screen-reader QA agent (Agents for Good)
**One-liner:** An agent that runs an automated VoiceOver/TalkBack-style regression suite
against app builds, files reproducible bug reports for accessibility regressions before
release, and ranks them by screen-reader-impact severity.
**Pain evidence:** "who is actually testing these products? Are they blind?" — 61↑/46c
r/Blind; regressions reset rotor options every OS update, breaking banking/messaging apps.
**Eval wow:** This is itself an **eval/QA agent** — perfectly meta for the course's
"agent-as-judge" theme. Seed a test app with known WCAG defects → measure the agent's
**defect-catch rate (recall) at a controlled false-positive budget** and the quality of
its **severity ranking** (does its priority order match expert blind-user ranking?). The
agent literally IS an evaluator, so the eval expertise is the product.
**Concepts:** ADK · MCP (accessibility-tree / browser tool) · Evaluation · Deployability
(CI gate). · Security. → 4-5.
**Solo feasibility:** medium (needs an a11y-tree harness; scope to web, not native iOS).
**Existing asset:** greenfield (overlaps B's CI-gate pattern — reuse B's regression-gate
plumbing). **Demoability:** medium-high. **Whitespace:** whitespace (axe-core exists but is
rules-only, not an agent that reasons about screen-reader *experience*).

### E10 — ContractorVet: license + fraud due-diligence agent (Agents for Business)
**One-liner:** Pull contractor license status, aggregate cross-platform reviews, flag
lawsuit/complaint history, detect material-downgrade fraud (e.g. Class-3-vs-4 shingles),
and generate a standardized scope-of-work + milestone-payment template.
**Pain evidence:** "[Asking if licensed] caused a major problem — they became very angry"
— 1,816↑/464c (contractor rage) + 837↑/403c (shingle fraud) + 349↑/173c (license-check
backlash), r/HomeImprovement. Very loud, high-$ stakes.
**Eval wow:** Red-flag detection is a **classification + ranking** task — build labeled
contractor profiles (some fraudulent) → score **red-flag precision/recall** and the
**fraud-catch rate** on seeded material-downgrade cases. Asymmetric loss again: missing a
bad actor (you get burned for $30k) >> a false flag.
**Concepts:** ADK (license-check + review-aggregator + scope-drafter) · MCP (state license
DB / review-scrape tools) · Evaluation · Security · Deployability. → 4-5.
**Solo feasibility:** medium (real license DBs vary by state; v1 = mock DB + real review
logic). **Existing asset:** greenfield. **Demoability:** high (high-stakes, relatable).
**Whitespace:** whitespace.

### E11 — GrantPipeline: win-probability scoring for small NPOs (Agents for Business)
**One-liner:** Track foundation deadlines across a portfolio, score win-probability per
funder via mission-fit + past-award data, draft narrative sections in the org's own voice,
and flag when the pipeline needs more hours than staff have.
**Pain evidence:** "30% win rate means $60k/month in new applications, 6-12 apps on top of
existing cycles" — 49↑/38c + 44↑/39c r/nonprofit. Solo grant writers managing 10-30 grants.
**Eval wow:** Win-probability is a **calibration problem** — the user's sweet spot. Score
the model with **Brier score / AUC / calibration curves** on historical award outcomes,
and **funder-ranking quality** (does the top-ranked funder actually win more often?). This
is the most explicitly statistical eval in the slate — pure DS resume material.
**Concepts:** ADK (tracker + scorer + drafter) · MCP (grant-DB tool) · Evaluation ·
Security (org data, voice-fidelity guardrail) · Deployability. → 4-5.
**Solo feasibility:** medium (needs a plausible award-outcome dataset — synthesize it).
**Existing asset:** AI Writing Suite (voice-matched drafting + LLM-judge) — strong partial
reuse for the narrative-drafting half. **Demoability:** medium-high. **Whitespace:** moderate
(Instrumentl exists for discovery but no calibrated win-prob + voice-drafting combo).

### E12 — DashboardKiller: proactive insight agent (Agents for Business)
**One-liner:** Instead of building dashboard #48, an agent monitors key metrics for
anomalies and pushes a daily "here's what changed and why it matters" briefing — tuned to
each stakeholder's known priorities.
**Pain evidence:** "47 dashboards, nobody looks at any of them... decisions on gut feel" —
446↑/90c r/analytics + "stakeholders cherry-pick or ignore findings" 714↑/165c
r/datascience. This is *literally the user's own profession's* pain.
**Eval wow:** Two-layer eval the user can uniquely nail: (1) **anomaly-alert precision/
recall** with explicit **alert-fatigue tuning** (the precision/recall frontier IS the
product decision — too many alerts = ignored, too few = missed), and (2) a **downstream
"did the stakeholder act?" eval** (the cherry-pick/ignore pain made measurable). This is
the most resume-aligned idea: it's a search-relevance-style relevance/precision problem
applied to insight surfacing.
**Concepts:** ADK (monitor + diagnoser + narrator) · MCP (warehouse/metrics tool) ·
Evaluation · Deployability (daily cron + Slack). → 4.
**Solo feasibility:** high (synthetic metric streams with injected anomalies = clean gold
set). **Existing asset:** greenfield (ds-brainstorm-agent persona-tailoring reusable for the
stakeholder-priority angle). **Demoability:** high to a technical Kaggle audience.
**Whitespace:** moderate (Anomalo/observe exist for data-quality, but stakeholder-tailored
narrative + act-rate eval is open).

---

## Top picks (highest demand × eval-fit × demoability × feasibility)

1. **E1 BenefitsFinder** — Highest-signal pain in the entire dataset (1,146↑), genuinely
   life-changing outcome, eligibility = a clean ranked-retrieval/precision-recall eval the
   user owns, all rules are public (no API blockers) → high feasibility + whitespace.
2. **E2 EOB/Claim Auditor** — The most "broken-ruler-proof" eval in the slate (objective
   arithmetic ground truth, seedable trap suite), whitespace, very demoable ("caught a
   $1,300 hidden overcharge"), synthetic data trivial to generate.
3. **E12 DashboardKiller** — Most resume-aligned: it *is* a search-relevance precision/
   recall + alert-fatigue-frontier problem, the user can out-eval anyone, and the pain is
   their own profession's (instant credibility in the writeup). High feasibility.
4. **E3 RecordKeeper** — Most distinctive eval headline (fabrication rate + abstention
   calibration) directly answering the course's factuality/"trajectory-is-truth" spine;
   whitespace and a vivid demo (refuses to confabulate where ChatGPT invents a circus
   ancestor). Slightly lower feasibility (handwriting models) keeps it 4th.
