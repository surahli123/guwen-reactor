# Critical Review of the Expanded Ideas (E1–E12) vs the crystallized criteria

Written 2026-06-19. Reviews the 12 ideas from `40-expanded-ideas.md` through the
criteria that emerged in office-hours:
1. **Broad recognition** (universal, relatable, social-media-worthy) — the user's #1 goal
2. **Ground-truth / eval feasibility** (can a solo dev build a CREDIBLE gold set in days?) — the binding constraint
3. **Visualization potential** (open-design / Claude-design / hyperframes)
4. **Problem-fit > tech sophistication**
5. **Solo 17-day feasibility**
6. **WBFA reuse + low policy risk**

## The decisive filter: can you construct the ground truth?

| | Idea | Ground-truth source | Constructible solo? |
|---|---|---|---|
| ✅ | E2 medical bills | inject labeled errors into synthetic-but-grounded EOBs | YES (perfect labels) |
| ✅ | E4 tax | synthetic labeled bank transactions | YES |
| ✅ | E6 family ops | synthetic school emails/forms w/ labeled action-items+deadlines | YES |
| ✅ | E9 a11y | seed app with known WCAG defects | YES |
| ✅ | E10 contractor | synthetic contractor profiles w/ injected fraud signals | YES (realism fuzzier) |
| ✅ | E12 dashboard | inject anomalies into synthetic metric streams | YES (cleanest, your domain) |
| ❌ | E3 genealogy | needs correctly-transcribed handwriting gold (must read Kurrent/Gothic) | HARD |
| ❌ | E7 pronunciation | needs native-speaker-labeled phoneme audio | HARD |
| ❌ | E8 lit-review | needs an annotated corpus of which papers actually contradict | HARD |
| ❌ | E11 grants | needs historical grant→award outcome data | HARD |

The ❌ group is where the eval-as-wow strategy quietly dies for a solo 17-day build:
you can't produce trustworthy labels, so the impressive scorecard measures against a
broken ruler. Eliminate them regardless of demand.

## Ranked review of the constructible group

### E2 — Medical bill / EOB auditor ★ WINNER (already locked)
Broad recognition (universal US pain) · cleanest objective eval (arithmetic + injected
real error taxonomy) · most dramatic demo ($X recovered) · highest WBFA reuse (trust gate
1:1) · low policy risk · superb visualization. Caveat: don't let clean arithmetic seduce
you into the toy slice — inject the REAL error taxonomy (balance-billing, upcoding,
unbundling, OON) and keep a real-redacted-EOB reality-check holdout.

### E6 — FamilyOps (parental-load morning briefing) ◆ ONLY REAL RIVAL
- Recognition: viral (r/Parenting 5,346↑/842c) — every parent resonates, high share-ability.
- Ground truth: constructible (synthetic inbox/forms with labeled action-items + deadlines)
  → action-item extraction P/R + deadline-miss recall (recall-weighted cost).
- Viz: strong (morning-briefing card, action-needed list); PAA reuse (Gmail/Cal/Telegram).
- Why E2 still edges it: (1) financial drama ($1,300 recovered) is more visceral/viral than
  "don't miss the permission slip"; (2) E2's arithmetic ground truth is cleaner than "what
  counts as an action item" (E6 has labeling subjectivity); (3) higher WBFA reuse.
- Verdict: the legitimate backup. If the user wants Concierge-family over medical, this is it.

### E4 — TaxUnfreeze ◐ E2's dry sibling
Same synthetic-grounded eval pattern (labeled transactions → categorization confusion
matrix + deduction recall + asymmetric loss = very "you"). But: taxes are emotionally dry
vs medical-bill drama, and liability is the highest in the slate ("not tax advice" must be
loud). Loses to E2 on recognition-drama + risk.

### E10 — ContractorVet ◐ decent, narrower
Real drama (getting scammed, 1,816↑/837↑) + constructible synthetic profiles + good viz.
But narrower than universal medical bills, and "what's a real red flag" is fuzzier ground
truth than arithmetic, and state license DBs vary. Solid #3-ish, below E2/E6.

### E12 — DashboardKiller ◐ best eval-fit, wrong audience
Cleanest synthetic ground truth + literally your search-relevance domain (anomaly P/R +
alert-fatigue frontier). BUT niche analyst/DS audience + abstract demo → directly violates
the user's stated #1 goal (broad recognition, problem>tech). Great resume-purity, poor
recognition. Out under current criteria.

### E9 — A11y Regression Sentinel ◐ noble, niche
Constructible eval (seed WCAG defects), noble (accessibility), agent-as-judge meta-fit.
But niche audience + less consumer drama. Below E2/E6.

### E5 — PantryBrain ○ crowded + fuzzy
Very relatable + great viz, BUT crowded (Mealime/Whisk) and "correct meal plan" is fuzzy
(optimization metrics are computable, but quality is subjective). Differentiation is only
eval rigor in a crowded space — risky wow. Below the leaders.

## Eliminated (hard ground truth) — E3, E7, E8, E11
Real demand, but a solo dev can't produce trustworthy gold labels in 17 days
(paleography / native-audio / contradiction-corpus / award-outcome data). The eval-as-wow
strategy fails here. Cut.

## Bottom line
Nothing dethrones **E2**. **E6 (FamilyOps)** is the single genuine alternative — pick it
only if the user prefers a Concierge-family story over the medical-bill drama. E12 is the
contrarian resume-pure pick the user's own criteria rule out. Everything else is dominated
or eval-infeasible.
