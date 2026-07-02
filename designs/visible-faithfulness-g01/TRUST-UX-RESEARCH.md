# 信任UX研究 · Sonnet 5 六路深搜综合(2026-07-02)

**Run:** wf_cc720590-b60 · 6 研究员(事实核查/AI引用/Community Notes/C2PA/信任徽章/分层披露)+ 综合器 · 完整数据:`trust-ux-research-full.json`
**Owner 已同意执行方向(2026-07-02)。与 TRUST-UX-PROPOSAL.md 对表:高度一致,签名动作 = 闸门失败演示前置。**

---

# Verification UI — Ranked Recommendation Memo

## Top 8 Recommendations

**1. Full Fact's two-line skeleton → 考据 card, line one.** "Source says: [phrase]" / "Engine verdict: VERIFIED/CONTRADICTED" as the *first* thing shown, before literal-meaning + seal detail. Fits our 5-min non-technical reader: verdict in <2 sec without opening the whole card. Surface: **考据 card**. Effort: **S**.

**2. AFP's annotate-the-artifact pattern → gate toggle.** AFP never uses a separate meter — it draws red Xs directly on the evidence. Keep our strikethrough live and inline on the fabricated text itself (already planned), and add a one-line caption naming *what it conflicts with*, on the artifact, not off to the side. Surface: **gate toggle**. Effort: **S**.

**3. PNAS Community Notes finding → gate toggle detail.** Explanatory context (not source authority) is what moved trust 4.8–9.6pp in the one controlled study we have; bare crowd flags underperformed even expert flags. When CONTRADICTED fires, show the exact literal source phrase it disagrees with side-by-side — not just a red label. Surface: **gate toggle**. Effort: **S/M**.

**4. Baymard + Twitter blue-check → lamp, every instance.** A bare icon carries near-zero credibility for an unrecognized brand (a fake seal beat real minor-vendor seals in testing), and any perceived inconsistency retroactively poisons trust. Pair the lamp with a fixed, literal, narrow-scope sentence every time it appears ("Every factual claim checked against source text") — never the icon alone. Criteria must be described as mechanical, never discretionary. Surfaces: **lamp, index**. Effort: **S**.

**5. NotebookLM-style hover preview → 考据 card.** Click-through on inline verification affordances tops out at ~22% even on the best product (ChatGPT); ~80% never click. Add a hover/glance preview (source phrase + literal meaning, one line) so the majority who never click still register a real, inspectable check. Surface: **考据 card**. Effort: **M**.

**6. Model Cards' fixed section order → method page.** Google's Model Cards use an identical section order every visit specifically because they serve two audiences reading at different depths (skimmers vs. implementers) — exactly our educators-vs-judges split. Restructure as: *What This Checks → How It Checks → What It Doesn't Check → Known Limitations*, same order always. Surface: **method page**. Effort: **M**.

**7. NewsGuard's itemized, auditable rubric → method page.** Google's ClaimReview snippet died in 2025 partly because folded-in verdicts stopped reading as distinct signal. State the exact, numbered conditions that trigger CONTRADICTED in plain auditable language (not narrative marketing copy) so the rubric is checkable, not just asserted. Surface: **method page**. Effort: **M**.

**8. Museum tombstone-label tiering → badge+chips.** Physically separate tiers (title/date at the object → one paragraph of context → full catalogue) let casual visitors stop early without losing signal. Give any claim badge/chip a ~10-word tombstone label at glance level, with a "view full record" deep-link to the raw build-pipeline log reserved for the rare skeptic/judge — don't over-invest polish there; almost no lay reader reaches it (Wikipedia: 0.29% of pageviews click a citation). Surface: **badge+chips**. Effort: **S/M**.

## Tensions the data does NOT resolve — don't average these away

- **Confidence vs. hedging.** PolitiFact's clarity comes from a declarative closing line ("We rate the statement X"). C2PA/CDT warn hard against implying certainty you don't have (the "verified = true" conflation that broke Twitter's blue check). We need a **plain, literal, narrow-scope declarative** ("this claim was checked against [source]") — confident in wording, modest in scope. Avoid both a mushy hedge and an overclaim.
- **Passive vs. active trust-building.** Citation-UX research says most users never click (12–25%), arguing the *idle* state (lamp) must carry the trust load alone. But FDA nutrition-label data shows bigger/bolder numbers alone don't fix comprehension either — visual emphasis without adjacent plain-language anchoring is a dead end either way. Neither "make it bigger" nor "make it clickable" alone is enough; both need literal copy next to them.
- **Granularity.** Snopes retired 3 of ~20 rating tiers as "confusing"; Amazeen et al. found scale-granularity added no comprehension benefit for low-stakes content. This argues to **keep the lamp binary**, resisting any temptation to add a "partially verified" middle tier later.

## 3 Anti-Patterns to Avoid

1. **Multi-point granular verdict scales.** Snopes actively retired ambiguous middle categories; PolitiFact's 6-point gauge showed zero extra comprehension benefit over plain text once stakes rose. Don't build toward a "confidence score" or multi-tier rating.
2. **Clever abstract dichotomies in copy.** Wikipedia's "verifiability, not truth" was field-tested on millions of readers for 7 years and retired because it was consistently misread as the opposite of its intent. Don't frame "engine-checked" vs. "fact-checked" as a philosophical distinction anywhere — state literally what happened per line.
3. **Decorative badges with no adjacent claim, or folded into generic chrome.** Baymard's fake seal beat real minor certifications; Google killed ClaimReview once it blended into "a hodgepodge of other search features." The lamp/badge must be visually distinct every time AND never stand alone without its literal sentence.

## Signature Move

**Move the gate-off toggle's failure demo to the most prominent position on the page (ideally above the fold on the index/first article) and pair it with the source-phrase-side-by-side (rec #3), not tucked as a secondary control.** No pattern in any of the six families — not Norton's seal, not the blue check, not YouTube's AI label, not C2PA's pin — visibly demonstrates a *caught failure* live. Every real-world trust badge only ever says "yes." A skeptical judge watching CONTRADICTED + strikethrough + export-BLOCKED fire in real time, with the exact contradicting source text shown beside it, is the one thing on this list with no industry precedent to compete against — it converts "trust us" into "watch it fail and get caught," in under 15 seconds.