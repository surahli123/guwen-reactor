# G03 道旁苦李 — 内容层规格(生动读本 + 逐句血缘)

**状态:REVIEWED · PASS(2026-07-02)— 两道关皆过,灯火可点亮。**
**引擎判定:** `9/9 SUPPORTED · coverage 5/5 · READY_FOR_APPROVAL`(`runs/g03_clean`)

## 锁定的合同(沿 G01/G02)
- **纪律:** 生动只能用**原文已有的意象**(道、李樹、子、枝、走、動、問、答、取)与动词节奏;**绝不**加动机、评价、新动作。G03 `forbidden_claims`(10 条)是负面清单。
- **道旁苦李专属护栏(annotation-guardrails.md §B——推论坑最集中的一篇):**
  ①「此必苦李」= 王戎的 **speech-act/主张**,读本只能作他的话引出,叙述者不判"李确实苦";
  ②「信然」只述"果如其言",**不写尝李、不写"确认是苦的"、不外推因果**;
  ③ 两次「取之」主语不同:C04 是诸儿竞走,C08 主语**未指明**——读本用被动收笔,绝不归给王戎;
  ④「折枝」= 压弯枝条,非折断;「不動」= 没去摘;
  ⑤ 零评价:不写聪明/早慧/雅量(编者门类是 connotation),不写诸儿贪/蠢;
  ⑥「看」(C03)主语未指明——用"映入眼帘"式感知框架,不点名谁看见。

## 血缘链
| # | beat | 生动读本(English) | 已核实 claim | 事实 | 文言短语 | chunk |
|---|---|---|---|---|---|---|
| 1 | B01 | Wang Rong is seven. | Wang Rong is seven years old. | F01 | 王戎七歲 | C01 |
| 2 | B01 | One day he is out roaming with a crowd of other children. | He is out roaming and playing with a group of other young children. | F02 | 嘗與諸小兒遊 | C02 |
| 3 | B02 | By the roadside a plum tree comes into view — thick with fruit, its branches bowed under the weight. | By the roadside, a plum tree laden with fruit comes into view, its branches weighed down. | F03 | 看道邊李樹多子折枝 | C03 |
| 4 | B03 | The other children break into a run, racing to pick the plums. | The other children race over to pick the plums. | F04 | 諸兒競走取之 | C04 |
| 5 | B03 | Only Wang Rong stays where he is. | Only Wang Rong does not move to pick. | F05 | 唯戎不動 | C05 |
| 6 | B04 | Someone asks him. | Someone asks Wang Rong. | F06 | 人問之 | C06 |
| 7 | B04 | His answer: "The tree stands by the road, yet hangs full of fruit — these must be bitter plums." | Wang Rong answers that the tree stands by the roadside yet has many fruits, so these must be bitter plums. | F07 | 答曰：「樹在道邊而多子，此必苦李。」 | C07 |
| 8 | B05 | The plums are picked — | Afterward the plums are picked, by an unspecified party. | F08 | 取之 | C08 |
| 9 | B05 | — and it is just as Wang Rong said. | It turns out to be just as Wang Rong had said. | F09 | 信然 | C09 |

## 忠实自查(作者侧,主动收住的)
- **第 6 句**:草稿曾写 "Someone asks him **why**" —— 原文只有 問之(问他),问题内容未载,"why" 是推断 → 删,保留最朴素的 "Someone asks him."
- **第 8 句**:被动语态收笔,不写"孩子们摘/有人尝"——第二个 取之 主语开放是本篇最著名的坑。
- **第 9 句**:严禁写 "and the plums were indeed bitter"(forbidden #1:尝出苦是无据的);信然 只承诺"果如其言"。
- **第 3 句**:"comes into view" 感知框架,不点名谁看(F03 主语未指明);"bowed" 非 "broken"(forbidden #8)。
- 全篇零"聪明/早慧/雅量"词汇(forbidden #4/5/6)——把判断留给读者,这正是原文的笔法。

## 独立审校(独立上下文,作者/审校分开)
**Round 1(Codex,2026-07-02):OVERALL PASS — 零 MUST-FIX,1 NIT 已吸收:**
- 第 1 句 "This year" 属无据时间框定(F01 只载"七岁")→ 改 "Wang Rong is seven."(审校建议措辞)
- 全部陷阱位获审校确认:折枝=压弯 ✓ · 不動=stays where he is ✓ · 問之 无内容推断 ✓ · 此必苦李 留在引号内 ✓ · 末次取之保持被动无主语 ✓ · 信然 无尝李无因果 ✓

**审校结论:REVIEWED · PASS(引擎 9/9 SUPPORTED + Codex 独立审校)→ 灯火点亮。**
