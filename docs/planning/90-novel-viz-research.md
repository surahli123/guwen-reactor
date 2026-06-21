# 90 — Novel-to-Visual Agent: Viability Judgment

Written 2026-06-20. Judging the idea: **an agent that turns novels the user has read
(古文 / 网文 / classics) into comics, short videos, or 吐槽/reaction commentary.**

Context: solo builder, 17 days, vibe-coding level. User differentiator = EVALUATION.
Stated capstone priorities: (1) broad recognition > technical purity, (2) right PROBLEM >
sophisticated architecture, (3) heavy visualization. Incumbent: **E2 ClaimGuard**
(medical-bill auditor) at 82/90 — viral proof point, objective arithmetic ground-truth eval,
low risk, reuses the WBFA trust-gate.

## Methods & source-quality note
- Source = a pre-collected scout JSON (6 channels: Bilibili/opencli, Reddit/opencli,
  CN-social/opencli, X/twitter CLI, PH+GitHub, Google market). I did NOT re-run the scouts;
  I am scoring the supplied signals against E2 and the rubric (`00-capstone-requirements.md`)
  and the E2 decision (`80-e2-vs-e6-decision.md`).
- **Signal-type caveat (load-bearing).** Almost every high-engagement number here measures
  *demand to CONSUME* novel-derived content (people watching 吐槽/解说/漫剧), or *creator demand
  to MONETIZE* a production pipeline. Very little measures demand for the *specific reader-side
  personal tool* this idea proposes. The two whitespace claims ("no reader-personalized 吐槽
  tool", "no reading-history-aware tool") are **signals from absence** — weak by construction.
- Self-reported product metrics (LlamaGen "100k users", "millions of comics") are unverified
  marketing; treated as low-strength.

---

## 1. Top themes (engagement-ranked demand clusters)

### Theme A — 吐槽 / 解说 / reaction commentary (CROWDED on supply, whitespace on tooling)
Strongest raw engagement in the entire scan.
- **7,614,188 views · 103,800 弹幕** — 玫瑰叔品三体 42-part 解说 series (durable, still #1 ranking).
- **10,790,274 views · 655,166 likes** — 云社_ literary reaction clip (highest single video found).
- **6,169,169 views · 62,958 likes** — 假如古代有Deepseek (AI × classics humor).
- **4,674,876 views · 169,379 likes · 18,589 shares** — 离谱网文盘点 5-min 吐槽 (best share ratio).
- **1,976,730 views · 21,363 弹幕** — 弱智网文盘点 (Feb 2026 — proves the format is *currently* viral, not legacy).

Read: the *audience* is enormous and durable. But the **tooling whitespace** ("AI that turns
a novel you read → personalized 吐槽 script") is an **absence signal** only — no product, no
upvotes, no stars proving anyone wants the *tool* (vs. wanting the *videos*). Supply side is
saturated with manual creators; that is a content market, not validated tool demand.
→ Marked **moderate** (huge consumption demand, unproven tool demand).

### Theme B — novel → short-video / 漫剧 / 动画 (CROWDED — funded, regulated, contested)
Largest *commercial* pull, and the most contested.
- **Market: ¥3,676.1B** total 网文 IP-adaptation (2025, +23% YoY); AI漫剧 sub-market **¥20B+**,
  180+ new titles/day; 阅文 漫剧助手 opened **100,000 licensed IPs**; platform subsidies **>¥10B**.
- **924,387 views** — ¥41.6 三体 fan animation ("made for $6" relatability hook).
- Creator-replication intent: **2,807 / 2,327 / 1,856 bookmarks** on X pipeline threads — the
  strongest *save* signals in the dataset, but all from *creators wanting income*, not readers.
- **REGULATION RED FLAG:** April 2026 mandatory pre-broadcast filing for AI漫剧; Korea
  mandatory AI-labeling (Jan 2026); WEBTOON boycotts + forced redraws on AI disclosure;
  CHI 2026 "reverse-halo" (enjoyment drops when AI use disclosed).

Read: massive market, but it is a *crowded, funded, now-regulated* arena (ArcReel 531★,
LumenX/Alibaba, Toonflow, waoowaoo, ViMax/HKU). A solo 17-day agent cannot out-build these,
and the IP is all copyrighted. → **crowded**.

### Theme C — novel → comic / manhua (whitespace on QUALITY, not on attempts)
- **Tool stars are thin & quality is the known gap:** ai-comic-factory **1,329★** (generic,
  no novel ingestion); Dashtoon **$5M seed**; HANASEE **$1.5M pre-seed**; Mangaka.app 105 PH
  upvotes *with quality complaints*. Direct novel→comic demos pull only **4K–45K views** vs.
  **4M+** for commentary — "interest exists, quality not solved."
- **Strongest *want* evidence is Reddit pain, not tool demand:** r/Manhua "this sub is dying…
  AI slop" **843↑**; faithful-adaptation rage **82↑/98↑**; SnowMTL shutdown panic
  **1,775↑/1,366c** (but that's *translation*, not generation).

Read: genuine unmet *quality* need, but "character consistency across a 百万字 novel" is
exactly the hard problem that funded startups have NOT solved. Wrong difficulty for a
vibe-coding solo in 17 days. → **moderate** (real gap, infeasible bar).

### Theme D — 古文 / classics → animation (the only copyright-safe corner)
- **1,298,674 views** — AI recreates a PRC-textbook story (《金色的鱼钩》); 古文 educational
  animation series 280K+/series.
- Adult creative 古文 manhua = "near-zero results" (low strength — could be no demand, not just
  no supply).

Read: smaller numbers, but **public-domain source** — the only sub-angle where copyright
isn't fatal. The seed of any survivable wedge lives here.

---

## 2. Sharpest wedge (most demoable + EVALUABLE + copyright-safe + solo-17-day)

**"古典名著 panel-storyboard agent with a faithfulness scorecard"** — input = a *public-domain*
classic (三国演义 / 西游记 / 红楼梦, or user-authored text) → agent extracts a character bible +
scene beats → generates a storyboard / comic strip → and (the eval wow) **scores each panel for
SOURCE FAITHFULNESS and CHARACTER CONSISTENCY against the extracted bible**, with a human-in-
the-loop gate that flags panels that drift.

Why this and not the viral versions:
- **Copyright-safe** because forced onto public-domain classics (or user-owned text). Every
  viral 网文 signal is copyrighted + now regulation-gated → unusable as a *demoable* corpus.
- **Evaluable** because the eval target is reframed from subjective "is this good art?" to
  semi-objective "does panel N contradict the established character bible / plot beat?" — a
  faithfulness/consistency check, which is closer to the user's NDCG/relevance instincts than
  punchline quality is.
- **Demoable** in 5 min: pick a famous scene everyone knows (三顾茅庐 / 大闹天宫) → show panels +
  the scorecard catching a drift → before/after. Recognizable, visual, has a "reveal."

Honest caveat: even here the eval is **weaker than E2's arithmetic**. "Faithful to the bible"
needs an LLM-as-judge or human pairwise; it is defensible but not *objective ground truth*.

---

## 3. Capstone fit

- **broad_recognition:** STRONG on raw audience (10.7M / 7.6M / 6.1M view clips). But that is
  recognition of *the content genre*, not of *this tool/problem*. E2's 36,998↑ "Claude cut a
  $195k bill" is recognition of *the exact product*. This idea has bigger eyeballs, weaker
  problem-recognition.
- **visualization:** BEST IN CLASS — this is the idea's single biggest edge. Comics/storyboards/
  reaction cards are inherently screenshot-and-video gold; trivially beats E2's bill-markup card
  for a 5-min YouTube "wow."
- **eval_feasibility (brutal):** This is the soft underbelly. The user's wow = a rigorous eval.
  Candidate metrics: (a) **faithfulness** to source (LLM-as-judge vs. extracted facts — semi-
  defensible); (b) **character consistency** across panels (CLIP/embedding similarity of a
  character's appearance, or judge — partially objective, genuinely measurable); (c) **笑点/
  punchline hit-rate** for 吐槽 (human pairwise A/B — pure vibes, position-bias-prone, NOT
  defensible as ground truth). Bottom line: a *defensible* eval CAN exist (consistency +
  faithfulness, calibrated to fail 30-40%), but it is **judge-based, not arithmetic** — strictly
  weaker than E2's injected-error arithmetic, and one bad rubric away from "measuring with a
  broken ruler."
- **copyright_risk:** HIGH and structural. The viral fuel (网文/名著 adaptations) is copyrighted;
  AI漫剧 now requires mandatory filing in China (Apr 2026) and AI-labeling in Korea (Jan 2026);
  disclosed-AI adaptation triggers boycotts. Mitigation = restrict to public-domain classics /
  user-authored text — which *removes the viral 网文 angle entirely*. The thing that makes it hot
  is the thing you can't legally demo.
- **solo_17day:** RISKY. Character consistency across a long novel is the exact unsolved problem
  funded startups ($5M, $1.5M) are still failing at. Feasible ONLY if scoped to one short famous
  scene + a handful of panels + the scorecard (treat generation as off-the-shelf, make the
  *agent + eval* the contribution). Full "novel → comic" is not 17-day feasible solo.
- **concepts_hit:** Agent/multi-agent (extractor → storyboarder → consistency-auditor) ✓;
  Evaluation (faithfulness/consistency harness) ✓ — the gate concept; Agent skills / Agents CLI ✓;
  Deployability ✓ (demo). MCP / Security / Antigravity = bolt-on, same as E2. Clears the ≥3 gate.

---

## 4. vs E2 (head-to-head)

**Where it BEATS E2**
- **Visualization & video wow:** comics/storyboards crush a bill-markup card for a 5-min reel.
- **Virality / fun / passion:** the genre has 10M-view proof of appetite; personally energizing.
- **Novelty:** "reader-personalized commentary/storyboard" is genuinely unbuilt.

**Where it LOSES to E2**
- **Eval rigor (decisive, ×3):** E2 = objective arithmetic + injected real-error taxonomy →
  a clean fail-30-40% scorecard. This idea = judge/embedding eval on creative output → softer,
  bias-prone, "is the rubric a broken ruler?" risk. The user's *entire differentiator* is the
  dimension where this loses.
- **"Real-world problem" framing (×3):** E2 saves people money on a painful bill (Agents-for-
  Good/Business slam dunk). This is entertainment/art — valid under "Agents for Good: art/
  literature," but a weaker "helps people" story for judges who "reward a wow [but] solve a real
  problem."
- **Copyright / risk (×2):** E2 = synthetic EOBs, zero IP risk. This = structural IP + active
  regulation. E2 wins cleanly.
- **Asset reuse (×1):** E2 reuses WBFA trust-gate 1:1. This builds eval from scratch.
- **Feasibility (×2):** E2 synthetic-EOB pipeline is trivial; consistency-eval is the harder lift.

**Bottom line:** On the user's *own* weighting (eval-cleanliness, problem, risk all ×3/×2),
this idea loses on exactly those axes and wins only on visualization (×2). Projected ~62-68/90
vs E2's 82 — it does not overtake.

---

## 5. Recommendation

**Keep E2 as the capstone.** It dominates on the three dimensions the user weighted highest
(eval ground-truth, real problem, low risk) and has the single strongest demand signal in the
entire research (the 36,998↑ "Claude cut a $195k bill" thread that literally *is* the product).
This novel-viz idea wins only on visualization/fun — and pays for it with judge-based eval
(undercuts the user's wow), structural copyright risk, and a feasibility wall (character
consistency) that funded teams haven't cleared.

**Optional hybrid (low-cost, high-upside):** borrow this idea's *visualization energy* for E2's
demo without adopting its risks — e.g., a comic-strip / storyboard rendering of the bill-dispute
narrative or an animated "$195k → $33k reveal" in the YouTube video. Keep E2's arithmetic eval
as the spine; bolt on the visual drama this genre proves audiences love.

If the user's priorities ever flip to *passion + virality > eval rigor*, revisit the **§2
public-domain-classics + faithfulness-scorecard** wedge — it is the only version that survives
copyright and gives the eval somewhere defensible to stand. But that is a different bet than the
one E2 was chosen on.
