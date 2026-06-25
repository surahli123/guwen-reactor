# Gold 双标注交叉验证协议 (Gold Cross-Validation Protocol)

**适用范围**：3 个被测场景 `管宁割席 / 咏雪 / 道旁苦李`。
**来由**：落实 D2 的「independent check」，并按 owner 决定（2026-06-23）从「单标注」升级为「双标注交叉验证」。
**字段名用英文（与 gold schema 对齐），说明用中文。**

---

## 0. 为什么要双标注 (why)
gold = 评测的「标准答案」。若 gold 把**动机/评价**当成**字面事实**，gate 就是在拿一把歪尺量——会把忠实的改写误判为不忠实。
单标注者可能整条漏过这种污染；两个**互相看不见**的标注者互为对照，能把它逼出来。这就是交叉验证的唯一目的：**抓 gold 污染**。

## 1. 判断单元 (unit of judgment)
每个 scene 的 gold = 一组 `atomic_fact`，每条带 `grounding` 标签。两位 reader 对**每一条**事实判三件事：

| 代号 | 判什么 | 不通过的例子 |
|---|---|---|
| **M** membership | 这条字面事实该不该进 gold？（完整 + 无多余） | 漏掉「歆废书出看」；或凭空加一条原文没有的 |
| **G** grounding ⭐ | 纯 denotation（字面），还是偷渡了 inference/evaluation？ | 「华歆贪慕钱财」← 原文只有『捉而掷去之』，贪慕是评价 |
| **S** segmentation | 是否原子？（两事并一条 / 一事拆两条都不行） | 「戳蛋+没戳中」切成两条 → 重叠计分 |

G 是最关键的一项——本项目的 faithfulness 论证全靠它守住。

## 2. 流程 (steps)
1. **Draft（AI）**：AI 从原文生成候选 `atomic_fact` 列表。这是**草稿，不是答案**。
2. **Reader A 独立审**：照原文逐条判 M/G/S，增删改，产出 A 版。
3. **Reader B 独立审**：同样逐条判，**全程不看 A 的结果**（blind）。产出 B 版。
4. **Compare**：对齐 A、B，逐条标 `agree / disagree`。
5. **Adjudicate**：分歧逐条裁决（见 §4），产出 final gold。
6. **Record**：写进 gold 文件的标注字段 + `data/gold/independent_check_notes.md`。

> 关键纪律：**A、B 必须独立**。若 B 看着 A 的答案「核对」，那只是复读，不是交叉验证——一致率会虚高、抓不到污染。

## 3. 一致性怎么量 (agreement metric — 小样本诚实版)
- 数据量：3 scene × ~10 fact ≈ **30 条**。这是小样本，指标要按小样本诚实地选。
- **主指标 = percent agreement**：对 `A ∪ B` 的候选事实，两人在 M+G+S 三项都一致的比例。直观、n≈30 稳。
- **Cohen's κ = 次要/可选，且必须带 caveat**：n 太小 + 分布偏斜（绝大多数事实都是 `include-literal`）→ κ 有「高 prevalence 悖论」，可能算出很低的值却是假象。**报 κ 必须连同 percent agreement + 说明，绝不单报 κ。**
- 真正要看的是**分歧清单本身**（哪条、为什么不一致），不是一个聚合数字。一个数字过不了关，分歧清单才是改 gold 的依据。

## 4. 分歧裁决 (adjudication)
1. 先讨论求共识。
2. **预注册 tie-break（裁决前先定死，不可看了结果再改）**：`存疑 → 排除出字面 gold / 降到 advisory`。保守原则——**宁可漏一条，不可污一条**（漏只损召回，污会让 gate 歪）。
3. 每条分歧记录：最终决定 + 理由（一句话）。

## 5. 记录与揭露 (recording + disclosure)
- gold 的每条 fact 增加字段：`annotator_A` / `annotator_B` / `agreed`(bool) / `adjudication_note`。
- scene 级记 `agreement_pct`。
- `docs/measured_results.md` 必须揭露：**2 名标注者 · percent agreement · 分歧如何裁决 · κ 的小样本 caveat**。诚实披露方法局限，是这把尺可信的前提。

## 6. 谁来标 + 不阻塞 build (who + non-blocking)
- 两名标注者须是**中文母语 / 文言可读的人**（owner 可担任其一）。
- **AI 只能 draft，不能当「独立标注者」**：生成器/judge 与标注同源 → 不独立，会自我印证。若退而求其次用 AI 当「第二读者」，只能算 lint（机器初筛），**不得记为人类 IAA**，且需在揭露里写明。
- 若实在只有 1 名人类读者 → 退回单标注 + 揭露 `no-IAA`（即原路径 3）。
- **offline-first 不阻塞**：代码（schema / gate / `evaluate_run`）**不依赖**第二名 reader。
  先用 A 版产出 committed fixture gold 把 build 跑通；B 版到位后**回填** agreement 字段、升级 gold。
  → 别让「找第二个人」卡住 Phase-1 编码。

## 附：一个具体例子（管宁割席）
候选事实 `「华歆见金而贪慕」`：
- **Reader A** 受「管宁割席=鄙视贪财慕荣」典故影响，误标为 `literal`。
- **Reader B** 标 `disagree`：原文只有『华捉而掷去之』(动作)，「贪慕」是后世评价 → **G 不通过**。
- **裁决**：移出字面 gold（可入 advisory 的 interpretation 层）。

→ 这就是交叉验证「抓污染」的实战：单标注者可能整条漏过，双标注把它逼出来。对照原文的 10 条 denotation（见 `specs` / 取证），全部是动作与言语，**零动机、零评价**——final gold 必须长这样。

---
*本协议同时是 ⑤ 标注护栏的一部分；Phase-1 写 `canon_gold.yaml` 时按此执行，结果落 `data/gold/independent_check_notes.md`（Contract D 交付物）。*
