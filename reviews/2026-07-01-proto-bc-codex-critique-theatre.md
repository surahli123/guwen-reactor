# Codex Critique Theatre — 原型 B vs C(多篇中心站语境)

- **评审器:** Codex (GPT-5.5) · 独立上下文 · read-only 沙箱 · 本机已装 `open-design-critique-theater` skill(真实调用,非模拟)
- **工件类型:** UI 设计原型(交互式单文件 HTML),校准镜头 = 设计质量 + 交互 + 产品契合
- **发起:** /adversarial-review(2026-07-01),完整原始输出见 session task `bf6d7uqz7`
- **VERIFIED_AGAINST:** feat/phase-0-scaffold @ b3413a7382bf06e49cb910dd6bdd210d42e28d64 @ 2026-07-01 15:22:13 PDT

---

## 1. Theatre Transcript(四评论家三轮)

### 「策展人」The Curator
- B has the truer 展卷 ritual: right-to-left, scroll body, stations as 驿站.
- C is closer to the reference's "map is protagonist" state: full-viewport map, labels always visible.
- Both still look like elegant CSS scenery, not 山河卷 ground truth. The real crop is not optional for final build.
- B's emptiness becomes tasteful for one story, but thin for a multi-article website.

### 「架构师」The Information Architect
- Both are architecturally wrong for the pivot: map stations are beats, not articles.
- Multi-article hub needs `article -> beat -> line`; current structure is `beat -> line`.
- B becomes a linear tape at 10+ articles. C can become a hub.
- The beat layer belongs inside the 册页 panel as tabs/list/accordion, not as top-level map stations.

### 「教师」The Educator-User
- The buyer needs "safe for class," not a beautiful guessing game.
- G01 can be marked verified; G02/G03 must be visibly "gold draft / reading not reviewed."
- C gets the judge to the whole product faster after animation. B risks "where am I?" for mouse-wheel users.
- Trust badge copy must not imply the adaptation layer itself is deterministically verified.

### 「工程剧评人」The Stage Engineer
- B's `240vw` canvas plus real base64 artwork is the danger path: base64 adds size, long-canvas detail costs more.
- B wisely avoids wheel hijacking, but that shifts burden to buttons/arrow keys for normal mouse users.
- C's fixed stage is cheaper and more controllable offline.
- C's 3.4s unroll is acceptable only as skippable, one-time, and off by default for judge/demo mode.

### Cross-Examination
- Curator defends B's authentic handscroll; Stage Engineer counters that authenticity collapses if the asset is bloated or low-res.
- IA attacks both: "beats as cities" worked only for G01. Curator says beats are more poetic; Educator says the buyer needs article selection first.
- Educator attacks C's opening animation as wasted Kaggle time; Curator says it establishes ritual. Verdict: keep it optional, never blocking.
- IA wants unreviewed articles visible as future capacity; Educator insists they must look unavailable/unverified, not half-trusted.

### Final Per-Critic Verdict
- Curator: B for single-story ritual; **C-modified for site**.
- IA: **C-modified, decisively**.
- Educator: **C-modified**, with trust-state hardening.
- Stage Engineer: **C-modified**; B only as optional article-detail mode.

---

## 2. Consolidated Findings

### BLOCKER
1. **Both: top-level stations are beats, not articles.** See B `data-beat` stations (proto-b-handscroll.html:267) and C (proto-c-unroll-intro.html:258). Why: fails centralized multi-article hub. Fix: map stations = G01/G02/G03 articles; panel contains beat nav and line-level 考据.
2. **Both: trust state is too broad.** `灯火=已核实` appears in panel foot, while G02/G03 are pending human denotation check (canon_gold.yaml:56). Fix: badge per article: `Verified`, `Gold draft`, `Reading not reviewed`; no amber lamps for unreviewed reading.
3. **Both: final aesthetic still lacks the reference map asset.** Reference requires 青绿山水 map as protagonist (REFERENCE.md:14). Fix: embed one compressed public-domain 千里江山图 crop; budget base64 carefully, especially if B remains.

### CONCERN
1. **B:** `#canvas { width:240vw }` and fixed `55vw` beat segments (proto-b-handscroll.html:38) do not scale to 10+ articles. Fix: do not use B as hub; reserve it for inside a selected article.
2. **C:** opening unroll (proto-c-unroll-intro.html:45) risks wasting judge attention. Fix: default to completed map in demo mode; keep replay/skip.
3. **Both:** panel is beat-detail, not article-detail. Reference panel has metadata, quote, filters, list. Fix: article panel header first, then beat list, then selected beat's lines and 考据.

### SUGGESTION
1. **C:** add right-top controls for article filters/status, not disabled placeholders.
2. **Both:** embed a tiny title font subset as playbook recommends; system CJK fallback may degrade on Kaggle/Linux.
3. **Both:** use lamps as verified density signals at article level, then line-level proof inside panel.

---

## 3. Hard Questions(必须回答后再动工)

1. Why is a map metaphor still justified for only 3 articles if the articles are not geographic? What semantic axis places G01/G02/G03 on the landscape?
2. Why should a first-time educator spend 3.4 seconds watching unroll before seeing whether the product prevents hallucinations?
3. At 10+ articles, what is the promised wayfinding: spatial clusters, chronological order, source collection, classroom theme, or verification status?

---

## 4. Final Verdict

**C-modified.** As-is, both fail the multi-article pivot. B is a beautiful single-article handscroll, but a weak centralized website. C's fixed map upgrades cleanly into an article hub: articles as stations, beat layer inside 册页, verified/unverified status visible before reading. Borrow B's handscroll ritual only as an optional article-detail mode.
