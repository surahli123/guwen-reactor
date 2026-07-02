# G02 詠雪 — 内容层规格(生动读本 + 逐句血缘)

**状态:REVIEWED · PASS(2026-07-02)— 两道关皆过,灯火可点亮。**
**引擎判定:** `9/9 SUPPORTED · coverage 5/5 · READY_FOR_APPROVAL`(`runs/g02_clean`)· **独立审校:** Codex 两轮(Round 1 FAIL→修,Round 2 PASS,详见文末)

## 锁定的合同(沿 G01)
- **语气:** 生动读本 · 克制的生动(诗意留白,不堆辞藻)。
- **纪律:** 生动只能用**原文已有的意象**(雪、內集、兒女、文義、鹽、空中、柳絮、風、笑)与动词节奏;**绝不**加动机、评价、新动作。G02 `forbidden_claims`(10 条)是负面清单。
- **詠雪专属护栏(annotation-guardrails.md §B):** ①孰优孰劣是禁述——原文只有「公大笑樂」,不写"更好/胜出/因她的答案而笑";②本名(謝安/謝朗/謝道韞)不进读本正文——标题沿接受史命名,由驿站 anchor_note 披露;③兒女=晚辈,非"his own sons and daughters";④篇末身份注=背景层,读本以"旁白补注"呈现,非情节。
- **数据来源(全部 committed):** `data/gold/canon_gold.yaml` G02(F01–F09、C01–C08、B01–B05)· `runs/g02_clean/{adaptation,structured_claims}.yaml`。

## 血缘链
`读本句 → 已核实 claim (C0x) → 事实 (F0x) → 文言短语(chunk 内高亮)`

| # | beat | 生动读本(English,可读层) | 已核实 claim(引擎核过的朴素句) | 事实 | 文言短语 | chunk |
|---|---|---|---|---|---|---|
| 1 | B01 | On a cold day of falling snow, Grand Tutor Xie gathers the family indoors. | On a cold, snowy day, Grand Tutor Xie holds a family gathering. | F01 | 謝太傅寒雪日內集 | C01 |
| 2 | B01 | With the younger ones of the family, he takes up the meaning of the texts. | He discusses the meaning of literary texts with the younger members of the family. | F02 | 與兒女講論文義 | C02 |
| 3 | B02 | Then, all at once, the snow thickens — flakes crowding thick and fast. | Soon the snow falls suddenly and heavily. | F03 | 俄而雪驟 | C03 |
| 4 | B02 | The Lord brightens: "All this whirling white snow — what does it resemble?" | Pleased, the Lord asks what the fast-falling white snow resembles. | F04 | 公欣然曰：「白雪紛紛何所似？」 | C04 |
| 5 | B03 | His elder brother's son, Hu'er, answers: "Scattering salt in the air — that might roughly compare." | Hu'er, the elder brother's son, says scattering salt in the air could roughly be compared to it. | F05 | 兄子胡兒曰：「撒鹽空中差可擬。」 | C05 |
| 6 | B04 | His elder brother's daughter says: "Not as good as willow catkins rising on the wind." | The elder brother's daughter says it is not as good as willow catkins rising on the wind. | F06 | 兄女曰：「未若柳絮因風起。」 | C06 |
| 7 | B05 | The Lord bursts into laughter, delighted. | The Lord laughs heartily and is delighted. | F07 | 公大笑樂 | C07 |
| 8 | 跋 | The story closes on the narrator's note: she was the daughter of the Lord's eldest brother, Wuyi — | The narrator notes she was the daughter of the Lord's eldest elder brother, Wuyi. | F08 | 即公大兄無奕女 | C08 |
| 9 | 跋 | — and the wife of Wang Ningzhi, General of the Left. | The narrator notes she was the wife of Wang Ningzhi, General of the Left. | F09 | 左將軍王凝之妻也 | C08 |

> 跋(#8–9)= 背景事实层(beat_id null;F08/F09 不属任何 required beat):计入 9/9 精确率,不计 5/5 幕覆盖。册页中以「跋 · 旁白身份补注」独立成节,与情节幕区分。

## 忠实自查(作者侧,主动收住的)
- **第 4 句**:草稿曾写 "The Lord looks out at the courtyard" —— 庭院、望向皆无据(原文只有 欣然曰)→ 删,改 "brightens"(欣然=已载神情)。
- **第 6 句**:草稿曾写 "counters, with the line that would outlive them all" —— "流传千古"是接受史评价走私 + 隐含胜出(forbidden #1/#8)→ 删。"offers hers" 中性,不比较。
- **第 7 句**:严禁接 "at her answer"(forbidden #2 因果)——句号收笔,只述大笑。
- **第 5 句** 草稿曾写 "answers first"——先后由语序承载即可,显式 "first" 是可省的推断(审校 NIT)→ 删。

## 独立审校(独立上下文,作者/审校分开)
**Round 1(Codex,2026-07-02):FAIL — 1 MUST-FIX + 1 NIT,均为作者自查漏掉:**
- **第 6 句 MUST-FIX**:原稿 "offers hers: 'Sooner say willow catkins…'" 把 **未若** 的比较锋芒磨掉了。比较判断是**她亲口说的**(speech-act 的一部分),读本必须保留;作者为避"叙述者背书"过度中性化,反而失真。已按审校建议改为 `says: "Not as good as willow catkins rising on the wind."`——比较留在引号内、归于说话人,叙述者零评价。(与 G01 第 2 句的教训成镜像:那次是**加**了无据之物,这次是**删**了有据之物——两个方向的漂移闸门都要防。)
- **第 5 句 NIT**:"answers first" → "answers"(已吸收)。
- 译名核对全过:欣然/驟/差可擬/兒女/內集 的处理均获确认。

**Round 2(revised lines 5+6 复审,2026-07-02):OVERALL PASS(9/9 行,零 MUST-FIX)。**
- 附 1 NIT 已吸收:第 2 句 "around him" 属无据空间摆位 → 改 "With the younger ones of the family, he takes up the meaning of the texts."(审校建议措辞)
- 译名复核确认:未若 已入引号归说话人,不构成叙述者判定;欣然/驟/差可擬/兒女/內集 均过。

**审校结论:REVIEWED · PASS(引擎 9/9 SUPPORTED + Codex 独立审校两轮)→ 灯火可点亮。**
