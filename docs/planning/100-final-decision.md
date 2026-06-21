# Final Idea Decision — E2 vs E6 vs Guwen Reactor

Written 2026-06-20. Closes the ideation phase after: 16+ ideas, 4 research workflows
(whitepapers, demand scan, pain-point expansion, novel-viz scan), NotebookLM livestream,
Kaggle rubric, office-hours, and two head-to-heads. Companion to `00`–`90` notes.

## The three finalists
- **E2 ClaimGuard** — agent that audits medical/insurance bills (EOBs) for billing errors
  + drafts cited appeal letters. Concierge / Agents-for-Good. Reuses WBFA trust-gate + eval.
- **E6 FamilyOps** — family "mental load" agent: reads messy school emails/forms → daily
  "action needed" briefing + drafts. Concierge. Reuses PAA.
- **Guwen Reactor** (ChatGPT 5.5 Pro shape) — multi-agent workflow: public-domain Classical
  Chinese story → modern explanation + character memory + reaction script + storyboard +
  subtitles + visual prompts + evaluation report. Agents-for-Good (Freestyle-ish). Greenfield.

## Weighted decision table (max 90; weights = user's stated priorities)
Weights: broad recognition ×3, demo drama ×3, eval cleanliness ×3, visualization ×2,
policy/risk ×2, solo-17day feasibility ×2, "clearly an agent" ×2, asset reuse ×1.

| Dimension (weight) | E2 | E6 | Guwen Reactor |
|---|---|---|---|
| Broad recognition (×3) | 5 — 36,998↑ "Claude cut $195k→$33k" IS the product | 5 — r/Parenting 5,346↑ cluster | 4 — 7.6M/10.7M-view 解说 clips, but genre-recognition not problem-recognition |
| Demo drama (×3) | 5 — recover $1,300 live | 3 | 4 — famous scene + scorecard reveal |
| **Eval cleanliness (×3)** | **5 — objective arithmetic + injected error taxonomy** | 3 — action-item boundary subjective | **2 — judge/embedding eval on creative output, broken-ruler risk** |
| Visualization (×2) | 4 | 4 | **5 — best in class** |
| Policy / copyright risk (×2) | 4 — synthetic EOBs, zero IP | 3 — family PII | 2 — structural IP + Apr-2026 filing/labeling regs |
| Solo 17-day feasibility (×2) | 4 — synthetic pipeline trivial | 4 | 3 — character-consistency wall ($5M/$1.5M teams unsolved) |
| "Clearly an agent" (×2) | 4 | 4 | 4 — multi-agent |
| Asset reuse (×1) | 5 — WBFA trust-gate 1:1 | 4 — PAA | 2 — greenfield |
| **Weighted total** | **82** | **67** | **~60** |

## Verdict: E2, decisively (82 vs 67 vs 60)
Guwen Reactor wins ONLY on visualization (×2) and loses on the three highest-weighted axes
(eval ×3, real-problem ×3, risk ×2) — it attacks the user's own differentiator (rigorous
eval) with a subjective creative output. E6 is the strongest "useful" alternative but trails
E2 on drama, eval cleanliness, and reuse.

## The hybrid (steal the best of the loser)
Take the novel-viz genre's **visualization energy** for E2's deliverables — render the
5-min YouTube demo as a **comic-strip / animated "$195k → $33k reveal"** (build with
design / hyperframes) — while keeping **E2's arithmetic eval scorecard as the spine**.
Best of both: Guwen's visual wow + E2's bulletproof eval + zero copyright risk.

## UPDATE (2026-06-20): Guwen Reactor v2 (polished, post-adversarial-review)

ChatGPT ran a YC-investor + AI-engineer adversarial pass and fixed every wall this
research raised:
- **Copyright** → public-domain only + reframed as EDUCATION (English-speaking educators/creators).
- **Eval softness** → reframed to **source-grounded faithfulness + cultural-accuracy + consistency** (LLM-judge calibration = the user's wheelhouse, not "is the art good").
- **Feasibility / character-consistency wall** → **MVP drops video generation**; exports Markdown / YAML / SRT + interactive storyboard/slideshow.
- **"More Layers" anti-pattern** → orchestrator + skills library + **DAG artifact handoff** + evaluator suite + policy gate + HITL (the course's recommended architecture).
- **Differentiator** → "not translation, not video-gen: source-grounded cross-cultural adaptation with evaluation."

### Re-score (Guwen v2)
| Dimension (weight) | E2 | Guwen v2 |
|---|---|---|
| Broad recognition (×3) | 5 | 4 (niche: English educators of Classical Chinese lit) |
| Demo drama (×3) | 5 | 4 |
| Eval cleanliness (×3) | 5 (arithmetic) | 3 (judge-calibration, defensible but softer) |
| Visualization (×2) | 4 | 5 |
| Policy/copyright risk (×2) | 4 | 4 (public-domain + edu) |
| Solo 17-day feasibility (×2) | 4 | 4 (video dropped) |
| Clearly-an-agent / course-concept density (×2) | 4 | 5 (orchestrator+skills+DAG+eval+policy+HITL) |
| Asset reuse (×1) | 5 (WBFA) | 3 (WBFA eval-gate pattern transfers to evaluator+policy gate) |
| **Weighted total** | **82** | **~72** |

### Revised verdict
Guwen v2 is now the legitimate #2 (72), past E6 (67), within 10 of E2 (82). E2 still
leads on the user's two top stated criteria (broad recognition + real-problem) and on
eval-cleanliness (×3). Guwen v2 wins on visualization (×2), course-concept density (×2),
and — crucially, off-rubric — the user's revealed PASSION (raised 3×, self-run adversarial
review). For a solo 17-day sprint, the motivation multiplier can close a 10-point gap.

**This is now a value call, not a math call:** E2 = rubric-maximizer / broad reach /
bulletproof eval. Guwen v2 = passion + visualization + denser course-concept showcase,
with a defensible-but-softer judge-calibration eval. Recommend E2 strictly by the user's
stated criteria; endorse Guwen v2 if the user is genuinely more excited (valid override).

## Locked concept (pending user "lock")
> **ClaimGuard** — a privacy-first agent that audits a medical/insurance bill (EOB) for
> arithmetic + balance-billing + upcoding/unbundling + coverage errors, ranks them by
> dollar impact, and drafts a cited appeal letter — with a **synthetic-but-grounded gold
> set + seeded real-error taxonomy → precision/recall + dollar-weighted recall + trust-gate
> calibration** as the showpiece eval, HITL before any output, built on WBFA's trust-gate
> architecture. Track: Concierge (or Agents for Good). Demonstrates ADK multi-agent
> (parser→auditor→drafter) + MCP (price-reference/OCR tools) + Evaluation + Security
> (PII/HITL) + Deployability → 5 of the 6 required concepts.

## Next steps
1. Finish office-hours → formal design doc (fold in the hybrid viz-demo strategy).
2. /grill-me to stress-test every branch.
3. Produce a 17-day solo execution plan (plan-only; build on explicit "go").

## Evidence trail
00 requirements · 10 project-fit · 20 demand · 30 idea-slate · 40 expanded-ideas ·
50 WBFA · 70 other-ideas-review · 80 E2-vs-E6 · 90 novel-viz-research · (this) 100 final.
