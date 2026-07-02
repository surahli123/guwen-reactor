# TRUST-UX-SPEC — 信任UX 定稿 v1

**Status: FINAL(owner 拍板 2026-07-02;三项形态决策已当面选定)**
**来源合并:** `TRUST-UX-PROPOSAL.md`(owner 已同意)× `TRUST-UX-RESEARCH.md`(Top-8/反模式/签名动作)× handover NEXT-1 执行清单
**改动对象:** `prototypes/proto-d-multiarticle-hub.html`(单文件离线,0 外部请求——每改必验)

---

## 0. 今日锁定的三项形态决策

| 决策 | 选定 |
|---|---|
| 闸门前置入口 | **朱封签牌**,地图首屏左下角常驻;首访轻微脉动一次;点击 → 开 G01 册页并滚至闸门 |
| 浏览器内真跑的视觉 | **朱批台账式**:逐行核对 F01✓…F0x✗(~250ms/行,楷体+CI 符号)→ 源文短语并排卡 → 朱笔现场划掉编造句 |
| 首屏地图框景 | **保持全国**(山河卷气魄;签牌与三驿站已验证不冲突) |

## 1. 信任漏斗(总纲,四层各一次点击)

```
瞥一眼   灯火(按篇,二元,恒带 literal copy,永不裸放)
   ↓ 点
读一句   考据卡:Full Fact 两行骨架领跑 + 原文高亮 + 印章
   ↓ 扳
验一次   闸门:浏览器内【真跑】规则子集,亲眼看编造被抓
   ↓ 查
查台账   9/9 chip → 可审计台账;方法页四节 + raw JSON 出口
```

铁律(反模式,来自研究,**不做**):
1. 不做多档评分/置信度分数——灯保持二元(Snopes/Amazeen 证据)。
2. 不做假实时——不加"扫描中…"假进度;动画只是**已算出结果的逐行揭示**(见 §3.4)。
3. 徽章/灯永不裸放,必配一句字面窄范围 copy(Baymard:假印章曾胜过真小厂认证)。
4. 文案不玩抽象二分(Wikipedia "verifiability, not truth" 七年后因被误读退役)——每处只字面陈述发生了什么。
5. B+C 口径不动摇:解读不计入核实,hedged 单列。

---

## 2. S1 · 朱封签牌(闸门前置入口)——签名动作的门面

- **位置:** 地图首屏左下角,fixed;避开右上 `.ctl` 区(z-index 两次 bug 教训:新浮层一律远离 .ctl,且检查 `body.panelopen` 状态下是否遮挡)。册页(右侧)打开时签牌**保持可见**(左下不冲突),但 z-index 低于 panel。
- **形态:** 褐纸签牌(复用 REFERENCE-guditu 签牌语法)+ 朱封圆点;宽 ~210px。
- **文案(EN-first,字面,自带 claim):**
  - EN(主):`Watch the engine catch a fabricated sentence — live.`
  - zh(小字):`亲手扳闸 · 看编造被当场抓住`
- **行为:** 点击 → `openArticle('G01')` → 平滑滚动至 `#gateBar` → 闸门 toggle **脉动一次**(动画只播一次,提示"扳我";**不自动扳**——可证伪性必须出自用户之手)。
- **首访引导(localStorage,与展卷同 key 体系):** 首访签牌本体轻微脉动一次;非首访静止。
- **窄屏(<760px):** 签牌收缩为小朱封按钮(仅圆点+"朱封"二字),点击行为同。demo 以桌面评审为主,不为移动端过度投入。

## 3. S2 · 闸门升级:浏览器内真跑(签名动作本体)

### 3.1 数据(全部嵌入单文件,来源 = committed gold)
- `G01_FACTS`:10 条 atomic facts(F01–F10,`data/gold/canon_gold.yaml` 逐字,已在 proto-d `sc.facts`)。
- `G01_FORBIDDEN`:7 条 forbidden claims(canon_gold 逐字):keeps the gold / physically attacks / drawn to status / envies wealth and rank / morally superior / reconcile / romantic。
- `GATE_CASES`:3 个预备编造案例(轮换):

| # | 编造句(EN) | 引擎判定路径 | 展示的失败行 |
|---|---|---|---|
| A(默认,现有 ghost) | "Hua Xin, tempted, slips the gold into his sleeve and keeps it." | 直接矛盾:F04「擲去之」= 他扔了金子;命中 forbidden #1 | `F04 ✗ CONTRADICTION` |
| B(动机走私,最有力) | "Guan Ning cuts the mat because he envies Hua Xin's ambition." | 事件真(F08 ✓)但动机为发明且未 hedge → unhedged-motive 规则 | `F08 ✓ event · ✗ UNSUPPORTED MOTIVE — no motive stated in source` |
| C(无中生有) | "Years later, the two reconcile and remain close friends." | 场景内无此事;命中 forbidden #6(reconcile) | `✗ NOT IN SOURCE — matches documented misreading list` |

案例 B 是证明"引擎不是关键词匹配"的关键(引用了真实 F08 事件仍被抓)。

### 3.2 规则子集(~50-80 行 JS,真计算)
移植引擎两条可在浏览器忠实复现的规则,输入为案例声明的结构化 claim(与引擎 StructuredClaim 同形):
1. **事实矛盾核对:** 逐条对 F01–F10 匹配案例的谓词(每案例携带机器可查的匹配谓词,与引擎 forbidden 匹配逻辑同构),命中 → CONTRADICTED。
2. **unhedged-motive 核对:** claim 带 motive 字段且无 hedge 标记且 source 无据 → BLOCKED。

**诚实边界(方法页原文,见 §6):** "The checker running in this page is a small subset of the real engine — the same 10 facts, the same forbidden list, simplified matching — run live in your browser on three prepared fabrications. The full engine (131 passing tests) runs in the build pipeline; every verdict shown for the published text is a committed record."

### 3.3 朱批台账(视觉,按选定形态)
扳闸后,编造句下方展开:
```
"…slips the gold into his sleeve and keeps it."
────────────────────────────────
Checking against source facts:      ← 楷体小标
 F01 ✓ pass
 F02 ✓ pass
 F03 ✓ pass
 F04 ✗ CONTRADICTION
┌─ Source says ──────────────┐      ← 并排源文卡(PNAS 证据)
│ 「捉而擲去之」               │
│  Hua Xin picks it up and    │
│  throws it away. (F04)      │
└────────────────────────────┘
✗ CONTRADICTED · export BLOCKED
```
- 台账行 ~250ms/行揭示;命中失败行即停(A 案停在 F04,不必跑满 10 行——真实引擎也短路)。
- 源文卡出现后,编造句上**朱笔划线动画**(现有 .strike 复用)。
- `#chipStats` 翻面 `✗ 1 fabrication blocked · export BLOCKED`(现有逻辑,加 ✗ 前缀)。
- 台账底部小链接:`Try another fabrication ↻`(轮换 A→B→C;Wave 3 交付,数据结构 Wave 1 就绪)。
- 关闸 → 全部复原,chipStats 回 `✓ 9/9`。

### 3.4 诚实动画原则(写进代码注释)
**先算后演:** toggle 时同步跑完规则子集拿到 verdict,再逐行揭示——动画是结果的排版,不是假装的进度。禁止 setTimeout 假装"正在扫描"。

## 4. S3 · 考据卡:Full Fact 两行骨架 + CI 符号

- 卡内容重排,**前两行固定**(判定 <2 秒可得,不展开也能读):
  ```
  Source says: 「寧讀如故」 — Guan keeps reading.
  Engine verdict: ✓ VERIFIED (F06)
  ```
  其后保留现有:字面释文 → engine-checked claim → 據印 stamp → zh 小结。
- **所有判定 chip 加 CI 前缀**(一行 CSS + 文案):`✓ REVIEWED·PASS`、`✓ 9/9 claims verified`、`✗ CONTRADICTED`、`✗ BLOCKED`。印章保留为文化皮肤,✓/✗ 承担语义。
- **hover 预览(M):** 未点击时 hover 任意句,浮出一行:源文短语 + 字面释文(~80% 用户从不点击,idle 态必须携带真信号)。桌面 hover;触屏退化为点击(现有行为)。

## 5. S4 · 9/9 → 可审计台账视图

- `#chipStats`(`✓ 9/9 claims verified`)变可点。点击 → 册页内切换到台账视图(非弹窗,同 panel 体系):
  - 9 行:`#句号 · claim 短句 · ✓ PASS · F0x · [跳转→]`(跳回该句并展开考据)。
  - 第 10 行:`1 interpretation — hedged, labeled, not counted as verified.`(B+C 口径的可见化)
  - 第 11 行:`0 fabrications in the published text — see what happens when one is introduced → [Watch it fail]`(链到闸门)。
- 每行即"墓碑标签"(museum tiering):~10 词止步,深链留给稀有怀疑者。
- 返回键回到读本视图。

## 6. S5 · 方法页(言必有據)重构:Model Cards 固定四节

节次**永远同序**(两类读者各取所需):
1. **What This Checks** — 每句英文读本的事实性 claim,对照《世說新語》原文的 10 条 committed facts。
2. **How It Checks** — a program, not an AI judge;deterministic rules;**131 passing tests**(此行保持显眼层级,X 研究:确定性+测试数=从业者信任通货);两道关(engine + independent human review)。
3. **What It Doesn't Check** — 文学质量、翻译风格、标注为 hedged 的解读、原文之外的任何事。
4. **Known Limitations** — 单标注者金标(已披露,复核待做);浏览器内为 demo 子集(§3.2 诚实边界原文);目前 1/3 篇通过全流程。

- **CONTRADICTED 触发条件编号化**(NewsGuard 式可审计条款,plain language):
  1. Claim 陈述的事件与已核实事实直接矛盾;
  2. Claim 给出 source 未载且未 hedge 的动机/情感;
  3. Claim 引用不存在或错幕的事实 id;
  4. Claim 命中本篇 documented misreading(forbidden)清单。
  (实施时与 `claim_validator.py`/`structural_audit.py` 逐条对表,措辞以引擎实际行为为准——**不得写引擎做不到的事**。)
- **View the raw record(折叠):** committed eval_report 摘录 pretty-printed JSON(怀疑者出口;评委正是会点开的人)。

## 7. S6 · 灯火 + 词汇门槛

- **灯火 literal copy 规则:** 灯出现的每一处(hint 栏、篇目榜行、册页头)配同一句窄范围字面文案:`Every factual claim checked against source text.` 现有 hint `lamp = verified` 升级为此句。灯本身保持二元(lit/ember),永不新增中间档。
- **考據 / 朱批 / 言必有據 tooltip(hover 即出,无状态门控):**
  - 考據:`kǎojù — the classical scholar's practice of tracing every statement to its source. Click any line to trace it.`
  - 朱批:`zhūpī — the vermilion ink reserved for a verdict. Here: the engine's rejection mark.`
  - 言必有據:`"Every claim must have a source" — how this page is checked.`

---

## 8. 实施顺序 + 验收(每 wave 必过再进下一个)

**通用验收(每改必跑):** `python3 -m http.server 8642` 亲开 → DevTools Network **0 外部请求** → console **0 错误** → 截图(绝对路径存 shots/)→ `body.panelopen` 下右上控件不被遮挡(第三次 z-index bug 预防)。

| Wave | 内容 | 专项验收 |
|---|---|---|
| **1(签名)** | §2 签牌 + §3 真跑闸门(案例 A 全链)+ CI 符号全量(§4 chip 部分)+ 首访脉动 | 签牌点击落点=闸门;先算后演(console.log verdict 先于首行揭示);台账停在 F04;源文卡与划线时序正确;关闸全复原 |
| **2** | §5 台账视图 + §7 灯火 literal copy + §6 方法页四节+编号条款+raw JSON | 台账 11 行跳转正确;方法页节序固定;JSON 折叠默认收起;编号条款与引擎代码对表记录留档 |
| **3** | §4 考据卡两行骨架重排 + hover 预览 + §7 tooltips + 案例 B/C 轮换 | 卡前两行 <2s 可读;hover 预览不与点击展开打架;案例 B 展示 `F08 ✓ event` 后再 ✗(证明非关键词匹配) |

**工程约束(handover 沿袭):** proto-d 已脱离 Edit 追踪 → 一律用 python 精确串替换管道打补丁(或整读后 Edit);G01 读本文本 REVIEWED·PASS **一字不动**(改字=重审);LXGW 字体子集是独立轨道(跨机 BLOCKER),不混入本 spec 的 wave。

## 9. 遗留开放项(不阻塞)

- 案例轮换是否加第 4 例(romantic / morally-superior)——Wave 3 后看密度再定。
- 台账视图入口是否同时挂在方法页——Wave 2 实施时看动线。
