# HANDOFF → Fable 5: rebuild G01 管寧割席 as a MAP-CENTRIC 山河卷 UI

*Committed on `feat/phase-0-scaffold` so a fresh session onboards from git alone. A fuller session log is at `docs/handover-2026-07-01-g01-baoyu-v1.md` — kept local by the repo's session-artifact hook (readable on this machine), so its key content is mirrored here.*

## State
- **v1 built + verified** → `index.html` (this folder). Offline single-file demo: click a vivid English line → its 文言 source lights + the engine-verified claim + a 印章 stamp (考据); a 「如果没有闸门」toggle → a false line struck out in 朱笔 + `CONTRADICTED · BLOCKED`. **Verified:** 0 external network requests (offline-safe for Kaggle/Pages), 0 console errors, both interactions DOM-checked; retelling text **REVIEWED · PASS** (opus critic caught 1 perception→action smuggle → fixed).
- **Owner reviewed v1 and REDIRECTED:** the reading-column layout is **rejected**. They want a **map-centric 山河卷 UI** (an immersive 青绿山水 handscroll as the centerpiece + a right-side 册页 panel, like the reference). This is a **presentation rebuild** — reuse v1's faithfulness *logic*, replace the *shell*.

## Read these first (all committed on the branch)
1. **`reference/REFERENCE.md` + the 6 PNGs** (`shanhe-01-full-map` … `shanhe-06-fenghua-leaderboard`) — the aesthetic ground truth. **Open each image with the Read tool** — don't rely on the text alone.
2. **`index.html`** — v1: layout rejected, but its `SCENE` data model + 考据/朱笔/印章-徽章 logic is correct & verified. **Reuse the logic, rebuild the shell.**
3. **`content-retelling.md`** — the faithful bilingual text + blood-lineage (line → verified claim → fact → 文言 phrase). **REVIEWED · PASS — no wording change without a fresh adversarial faithfulness review** against G01 `forbidden_claims`.
4. **`RESEARCH-PLAYBOOK.md`** — 国风 vibe-coding technique + anti-slop rules + public-domain backdrop sources.

## The rebuild (owner's core ask)
Map-centric 山河卷 UI: an immersive **青绿山水 handscroll** base (real public-domain 《千里江山图》 crop — Wikimedia Commons `Category:A_Thousand_Li_of_Rivers_and_Mountains`, **base64-embedded so it stays single-file + offline**, muted mineral 青绿, 留白) as the stage → the **3 beats as 3 城池/驿站 stations** (金 / 軒冕 / 割席), each a 签牌 tablet (selected = 深松绿+米字) + an amber **灯火** (lit = verified) → **click a station → right-side 册页 panel** with that beat's reading lines → **click a line → 考据** (文言 phrase lit + verified claim + 印章「·Fxx」). Fold in: bundle a subset 行楷 title font (LXGW WenKai, `pyftsubset` used glyphs, base64) for a cross-machine brush title; contemplative handscroll pacing (no scroll-jacking).

## Locked (do not renegotiate)
Single-file **offline** (no CDN/webfont/network — after any change, verify **0 external requests**) · **vivid ≠ invented** (every reading line traces to a committed fact in `data/gold/canon_gold.yaml` G01; `forbidden_claims` = negative checklist) · badge口径 **B+C** (badge = engine's deterministic verdict on committed claims; reading layer = 改写; C10 = "1 解读已标注", not in "已核实") · aesthetic ground truth = the 6 screenshots (creator 「胡言乱语」 is not findable online — don't chase it).

## Kickoff prompt (paste to a fresh Fable 5 session — after `/context-prime continue with this repo`)

```text
你接手 Guwen Reactor（Kaggle capstone）的「看得见的忠实 / Visible Faithfulness」demo（场景 G01 管寧割席）。已有一版 v1，但版式被否——你的活是把 UI 重做成"以地图为中心"的山河卷。我是资深产品数据科学家，vibe coding：请用中文、讲清楚、分阶段、大动作前先要我确认。

项目：~/Documents/guwen-reactor · 分支 feat/phase-0-scaffold · 目录 designs/visible-faithfulness-g01/。

先按序读：designs/visible-faithfulness-g01/FABLE-KICKOFF.md（本文件，全状态 + 方向）→ reference/ —— REFERENCE.md（目标"地图为中心"的山河卷 + 6 张截图逐张拆解），并务必用 Read 工具逐张查看 shanhe-01…06 这 6 张原图，亲眼对齐美学（青绿山水手卷+右侧册页+签牌+灯火+印章），别只读文字（这 6 张 = 美学地面真值）→ index.html（v1——版式作废，但忠实逻辑/数据正确且已验证：复用逻辑，重建外壳）→ content-retelling.md（忠实文本+血缘，REVIEWED·PASS，改字须重新忠实审校）→ RESEARCH-PLAYBOOK.md（技法+反套路+底图来源）。然后 invoke /baoyu-design。

你的活——重做成"以地图为中心"的山河卷 UI：沉浸式青绿山水手卷作舞台（用公有领域《千里江山图》crop，Wikimedia Category:A_Thousand_Li_of_Rivers_and_Mountains，base64 内嵌保持单文件离线，发暗矿物青绿 + 留白）→ 3 个 beat 作 3 个城池/驿站（金/軒冕/割席），各一枚签牌（选中=深松绿+米字）+ 琥珀灯火（亮=已核实）→ 点驿站 → 右侧册页面板（该 beat 读本）→ 点句 → 考据（文言点亮 + 已核实 claim + 印章·Fxx）。复用 v1 的 SCENE 数据 + 考据/朱笔「如果没有闸门」/印章徽章逻辑；只换外壳。顺带内嵌子集行楷标题字体（LXGW，跨机毛笔感）；手卷节奏克制（不劫持滚动）。

铁律（不可谈判）：单文件离线（无 CDN/网络请求，改后必验 0 外部请求）；生动≠虚构（每句读本溯源到 data/gold/canon_gold.yaml G01 的已核实事实，forbidden_claims 是负面清单）；徽章口径 B+C；美学地面真值 = reference 里的 6 张截图（作者「胡言乱语」全网查不到，别追）。

流程：每次改动后 serve + 验 0 外部请求 + console 干净 + 截图，才算 done；作者/审校分开（改文本 → 独立忠实审校）。先读完这些文件，给我诚实的 UI 批评 + 具体重做计划，等我 go。
```
