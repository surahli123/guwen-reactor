# Demo Narrative Critique (impeccable lens) — is the story legible to a foreign judge?

VERIFIED_AGAINST: docs/demo/index.html @ origin/main 0dd5f29 · live surahli123.github.io/guwen-reactor/demo/ · viewed 2026-07-04

**Test applied:** a Google/Kaggle DevRel judge who reads **no Chinese** lands cold, gives it ~90 seconds. Can they answer: *what is this, what do I do, why should I trust it?*

## Verdict: FAILS the 90-second test for a non-Chinese judge.
The handscroll is beautiful, but the beauty currently works *against* comprehension — it reads as "a pretty Chinese artifact," not "a trust engine you can falsify yourself." The whole pitch (source-grounded faithfulness + a gate you flip to catch a fabrication) is present in the build but not *legible on landing*. Every orienting surface — title, tabs, status, the CTA to the wow — is Chinese or buried.

## Findings, ranked

**[BLOCKER 1] No English entry point.** Landing view gives a non-Chinese judge nothing to anchor on: giant 看得見的忠實 / 世說新語, three Chinese tabs, Chinese status. In 5 seconds they can't say what this is. → A prominent English headline + one-line "what this is" is the single highest-leverage fix.

**[BLOCKER 2] The wow is a footnote.** The best moment — *flip the gate, watch a fabricated sentence get struck down live, including the motive-smuggling hard case* — sits in a small corner seal-card ("Watch the engine catch a fabricated sentence — live"). A 90-second skim may never trigger it. The demo's strongest, most judge-friendly proof is not the focal action. → Make "Flip the gate" the hero CTA.

**[BLOCKER 3] The map is the landing, and the map is the least self-explanatory view.** 10 vertical Chinese tablets + colliding English + Chinese place-names = overload with no reading order, and no statement that this is "10 stories, 3 verified." A foreigner doesn't know what a lit vs dark lamp means without reading Chinese. → Lead with the framing (what a lamp means; 3-of-10) and make the tablets legible.

**[HIGH 4] The three tabs are unlabeled modes, not a journey.** 篇目 / 言必有據 / 如果没有闸门 carry English only in hidden aria-labels. A judge can't tell they are Index / Method / Gate-demo, nor the order to walk them. This is the "top-right doesn't tell a consistent story" problem. → Relabel bilingually and sequence as a guided 1 → 2 → 3.

**[HIGH 5] Dev-label leak.** `原型 D · 多篇中心站(真投影舆图+篇目榜) · LXGW 文楷内嵌` (the `proto-tag`, index.html:548) is internal scaffolding shown on a submission artifact. → Delete.

**[MED 6] The overlap bug destroys the one affordance foreigners depend on.** The floating italic English names (`st-en`, index.html:127/885) are the ONLY thing a non-Chinese judge can read on the map — and they collide with each other and the place-names into illegibility (worst in the dense southeast: "The Plum Grove Ahead" / "Xun Jubo Stays" / "Yuanfang at the Gate" pile up). → Move the English name onto its tablet; drop the free-floating gloss; dim the Chinese place-name layer.

**[MED 7] The key trust stat is in Chinese.** `已核实 3 / 10 篇` (index.html:541) and the geo-note (556) are Chinese. "3 of 10 verified — the rest honestly dark" is the thesis in one line; a foreigner can't read it. → English-forward status.

## Intended story vs what lands
Intended: **Problem** (AI adaptation hallucinates; a teacher can't trust it) → **Wow** (flip the gate, catch a fabrication live) → **Trust** (honest 3-of-10 tiering). Currently a foreign judge gets none of these three beats on landing; they get an inscrutable pretty map.

## Cheapest set of changes to make the story self-guiding (recommended, keeps the Chinese aesthetic)
The Chinese *source material* stays Chinese — that is the point of the project. The fix is an **English scaffold around the Chinese core**:
1. **English orienting header (BLOCKER 1+2+7):** "Visible Faithfulness" title + one line ("Classical Chinese → English, every sentence checked against the source · 3 of 10 verified") + a primary CTA **"▶ Flip the gate — watch a fabrication get caught"** that jumps straight to the wow.
2. **Legible tablets (MED 6 + BLOCKER 3):** English name on each tablet; remove floating colliding glosses; dim place-names.
3. **Tabs as a 1-2-3 journey (HIGH 4):** ① Stories / 篇目 · ② How it's checked / 言必有據 · ③ Flip the gate / 如果没有闸门.
4. **Delete the proto-tag (HIGH 5).**
5. **English status + footer (MED 7).**

Net: same handscroll, but a non-Chinese judge now reads the problem, finds the wow, and gets the 3-of-10 honesty — in under 90 seconds.
