# G01 管寧割席 — 内容层规格（生动读本 + 逐句血缘）

**目的：** 这是"看得见的忠实 / Visible Faithfulness"demo 的**文字命根子**。视觉层可以后调，但每一句读本的**忠实血缘**必须先钉死。

## 锁定的合同
- **语气：** 生动读本 · 克制的生动（诗意留白，不堆辞藻）。
- **语言：** 文言源（繁体，原文）+ English 读本（可读层）。中文用于 chrome / 考据标签 / 印章。
- **纪律：** 生动只能用**原文已有的意象**（园、锄、金、瓦石、轩冕、门、书、席）与动词节奏；**绝不**加动机、评价、新动作。G01 `forbidden_claims` 是负面清单。
- **数据来源（全部 committed）：** `data/gold/canon_gold.yaml`（F01–F10、C01–C03 原文、B01–B03）· `runs/demo_clean/{adaptation,structured_claims}.yaml`。

## 血缘链（点击读本句 → 考据揭示）
`读本句 → 已核实 claim (C0x) → 事实 (F0x) → 文言原文短语（在 chunk 内高亮）`

| # | beat | 生动读本（English，可读层） | 已核实 claim（引擎核过的朴素句 C0x） | 事实 | 文言短语（考据高亮） | chunk |
|---|---|---|---|---|---|---|
| 1 | B01 | In the same garden, Guan Ning and Hua Xin bend to the same rows, hoes rising and falling. | Guan Ning and Hua Xin work the vegetable garden together. | F01 | 共園中鋤菜 | C01 |
| 2 | B01 | In the soil at their feet, half-buried, a piece of gold catches their eye. | Their hoes uncover a piece of gold lying in the soil. | F02 | 見地有片金 | C01 |
| 3 | B01 | Guan Ning does not slow — his hoe falls on the gold as on any tile or stone. | Guan Ning keeps hoeing, handling the gold no differently from a piece of tile or stone. | F03 | 管揮鋤與瓦石不異 | C01 |
| 4 | B01 | Hua Xin takes the gold in his hand — then throws it aside. | Hua Xin picks the gold up, then throws it away. | F04 | 華捉而擲去之 | C01 |
| 5 | B02 | One day, as the two sit reading on the same mat, someone in an official's carriage passes by the gate. | While the two sit reading, an official's carriage passes by the gate. | F05 (+F10 同席) | 又嘗同席讀書，有乘軒冕過門者 | C02 |
| 6 | B02 | Guan Ning's eyes never leave the page. | Guan Ning reads on as before. | F06 | 寧讀如故 | C02 |
| 7 | B02 | Hua Xin sets down his book and steps out to watch it pass. | Hua Xin puts down his book and goes out to look at the carriage. | F07 | 歆廢書出看 | C02 |
| 8 | B03 | Guan Ning cuts the mat in two and draws their seats apart. | Guan Ning cuts the mat and separates their seats. | F08 | 寧割席分坐 | C03 |
| 9 | B03 | "You are no friend of mine," he says. | Guan Ning says that Hua Xin is not his friend. | F09 | 曰：「子非吾友也。」 | C03 |
| — | 解读 | *Set side by side, their two answers to the gold may hint the friends weighed wealth differently.* (hedged) | Taken together, these contrasting responses to the gold may suggest the two friends place different value on wealth. | F03+F04 | （引申，非单句） | C01 |

> 注：F10（同席／same mat，committed context 事实，chunk C02「同席讀書」）现已**忠实织入第 5 句**——既给第 8 句「割席」补上"同一张席"的前情，又全部有据。徽章/灯火仍以 9 条情节 claim 计（F10 作 context 支撑，考据里可见）。

## 忠实自查 + 独立审校（教学点）
**我自查主动收住的：**
- **第 4 句**：草稿曾写 "lifts it to the light"，暗示"端详/动心"→ 走私微动机。收回；本轮再删 "stoops"（微弱"俯身去拿"戏剧化），只留 捉→擲。
- **第 8 句**：草稿曾写 "takes up a knife"，`割` 未言明器物，加"刀"是臆测器具。收回为 "cuts the mat in two"。

**独立审校（opus critic）抓到、我自查漏掉的（← 印证"作者/审校分开"）：**
- **第 2 句**：原写 "Their blades **turn up** a glint of gold"——F02 是 **見**（感知：看见金子在地里），但"blades turn up"让锄头成了**挖出**金子的施动者 = **新动作 / 推断当事实**，正是闸门要抓的 感知→动作 漂移。**已改**为感知框架 "…a piece of gold catches their eye"（复原 見，去掉"挖出"动作，顺带弃用有争议的 "glint"）。
- 审校确认：**假句**确与 F04「擲去之」矛盾、命中 forbidden #1，闸门 BLOCKED **合法**；**hedged 解读**确为真 hedge、对称不判高下。

**违禁清单核对：** 无"华歆留下金子 / 慕荣 / 弃书因慕荣 / 攻击 / 品德高下 / 和好 / 浪漫"——全避开。第 6/7 句只写动作（读如故 / 废书出看），不写动机。

**审校结论：** 一处必改（第 2 句）已改 → **PASS**。

## 「如果没有闸门」假句（对照第 4 句）
- **假句（未经闸门的 AI 会写）：** *"Hua Xin, tempted, slips the gold into his sleeve and keeps it."* → 断言 `Hua Xin keeps the gold`（committed `forbidden_claims` 原句）。
- **闸门判定：** 与已核实事实 **F04**（原文「**擲去之**」= 他把金子扔了）**矛盾** → `CONTRADICTED` → 内容闸门未过 → **禁止导出（BLOCKED）**。
- **朱笔呈现：** 假句以印章红朱笔勾去（strike-through），旁附拦截理由：「原文『擲去之』——他扔了金子；此句称他留下，与 F04 矛盾。」

## 信任徽章口径（B + C 透明度）
- **事实层（引擎确定性判定，本次 run `demo_clean`）：** `9/9 情节句已核实 · 3/3 情节覆盖(beat) · 0 虚构/矛盾`。
- **解读层：** `1 解读已标注（hedged，合理）` —— 单列，不进"已核实"分子。
- **读本层标注：** 明确标"读本 / adaptation"，与"已核实事实层"（考据里展示）区分。徽章**不声称**机器核过这些生动散文；每句挂考据链供读者自证。
- **"0 虚构"来源：** 引擎 `unsupported_critical_claims / contradicted_claims / unsupported_motivation_claims = 0`。

## 待办
- [x] 对抗式忠实审查（opus critic）→ REVISE→已改第2句→ **REVIEWED · PASS**（2026-07-01）。
- [x] 研究手册 → `RESEARCH-PLAYBOOK.md`（视觉技法/字体/颜色/反套路全在内）。
- [ ] 视觉层 v1（单文件离线 HTML）。
