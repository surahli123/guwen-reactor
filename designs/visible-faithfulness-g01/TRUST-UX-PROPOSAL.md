# 提案:让 eval/信任在网站上"可被外部用户经验"

**作者:** Fable 5(个人意见,owner 决策)· 2026-07-02
**背景:** owner 两个痛点——①信任文案西方用户读不懂(今日已修:EN-first + 事实释文);②"验证对外部用户不工作"——他们只能听我们断言"程序核过了"。本文回答第二问的**根本设计**。

---

## 核心论点:信任不是一个徽章,是一条可下钻的证据链 × 一次可亲手扳动的失败

外部用户(教育者/评委)信任的来源有三种,强度递增:
1. **被告知**(assertion)——徽章、数字。最弱,任何网站都能写"已验证"。
2. **可查验**(inspectability)——点开任何一句都能看到出处与判定记录。中等。
3. **可证伪**(falsifiability)——**亲手让系统抓一次错**。最强:用户不是相信我们,是相信自己刚看到的。

我们的四层结构(灯→考据→闸门→方法页)已覆盖三种来源。缺的不是层,是**每层的"work"感**。以下按杠杆排序。

---

## 建议(按杠杆从高到低)

### 1. 【最高杠杆】闸门演示改为"真·在浏览器里跑规则"(S-M)
现状:闸门 toggle 展示的是**预录的判定**。诚实,但"验证在工作"仍是转述。
提案:把引擎里**这一个 demo 案例所需的最小规则**(G01 的 10 条事实 + forbidden 清单 + 矛盾判定)移植成 ~50 行 JS,toggle 时**现场跑给用户看**:输入假句 claim → 逐条对照 F01-F10 → 命中 F04 矛盾 → CONTRADICTED。UI 上用 300ms 的逐行核对动画(F01 ✓ pass … F04 ✗ contradiction)展示**真实计算过程**,不是装饰动画。
- 这让 "the eval works for external users" 从修辞变成字面事实(至少对 demo 案例)。
- 诚实边界:方法页注明"浏览器内运行的是引擎的 demo 子集;全量引擎(131 测试)在构建管线"。
- 延伸(M):加一个「try another fabrication」轮换 2-3 个 forbidden 案例——最有力的是 demo_script 里那条**动机走私**("cuts the mat because he envies Hua Xin's ambition"——引用了真实 F08 却发明动机),它证明引擎不是关键词匹配。

### 2. 徽章数字变"可审计台账"(S)
"9/9 已核实"是静态断言。让它可点:**点 9/9 → 台账视图**——9 行 claim,每行 ✓ PASS + 所据事实 + 跳到对应句;第 10 行"1 hedged interpretation — labeled, not counted";第 11 行"0 fabrications(见闸门演示)"。数字从修辞变成账本,账本天然可信。

### 3. 判定符号借用 CI 语法(S)
西方评委每天看 GitHub:绿✓/红✗ 的语义无需教学。所有判定 chip 加 ✓/✗ 前缀(✓ PASS、✗ CONTRADICTED),印章保留为文化皮肤。一行 CSS 的事,理解成本直降。

### 4. 首访 15 秒引导证据链(S)
评委不会自己找到考据。首访(localStorage 门控,与展卷同一机制):自动开 G01 → 自动展开第一句考据(已做)→ **闸门 toggle 轻微脉动一次**(单次动画,提示"扳我")。信任漏斗的入口是被设计的,不是碰运气。

### 5. 「View the raw record」怀疑者出口(S)
方法页加一个折叠区:**引擎判定的原始 JSON**(committed eval_report 摘录,pretty-printed)。99% 用户不看,但它的存在本身就是信号——"敢给你看原始记录"。评委(技术背景)会看,而他们正是打分的人。

### 6. 考據 词汇门槛(S)
考據/朱批/言必有據 对西方用户是陌生词。首次 hover/点击时 tooltip 一次性解释:"kǎojù — the classical Chinese scholar's practice of tracing every statement to its source. Here: click any line to trace it."把文化元素从门槛变成卖点(它是产品故事的一部分,但必须自我介绍)。

### 7. 不做的事(反模式)
- **不做假实时**:不给预录判定加"扫描中…"进度条。一旦被识破,全盘信任归零。
- **不做信任弹窗/角标轰炸**:研究(NNGroup/Baymard 一贯结论)表明泛滥的 trust badge 被无视甚至降低可信度。我们坚持"一层一动作"。
- **不把解读计入核实**(B+C 口径不动摇)——诚实的边界本身就是最强的信任信号。

---

## 信任漏斗全景(改后)

```
瞥一眼   灯亮/灯暗(按篇,诚实)
   ↓ 点
读一句   考据卡:高亮原文 + 字面释文 + ✓PASS claim + 印章
   ↓ 点
验一次   闸门:亲手扳,看引擎【现场】抓住编造 → ✗CONTRADICTED
   ↓ 点
查台账   9/9 → 可审计清单;方法页 4 步;raw JSON 出口
```

每层一次点击,层层可退出;怀疑走得越深,证据越硬。

## 实施顺序建议
1+3+4(一次改动,S)→ 2(S)→ 5+6(S)→ 1 延伸多案例(M)。
全部保持单文件离线;JS 规则子集 ~2KB。

## 交叉验证
Sonnet 5 深搜工作流(run `wf_cc720590-b60`)正在核查成熟产品的同类模式(事实核查机构/AI引用/Community Notes/C2PA/信任徽章研究/分层披露),结果回来后与本提案对表:一致处加执行信心,冲突处提交 owner 裁决。

---

## 附:X/Twitter 实战信号(agent-reach · twitter-cli,2026-07-02)

**诚实评级:信号偏薄**(4/6 路查询命中皆为噪音——crypto/SEO 帖),两条真金:

1. **"营养标签"是行业自己选的隐喻。** Scott Belsky(时任 Adobe CPO,@scottbelsky)公开把 Content Credentials 描述为内容的 **"nutrition label"**(21k views);SEO 从业者 @lilyraynyc 实测 LinkedIn 已**自动**给 ChatGPT 生成图挂 C2PA 标签;@RashiShrivast18(Forbes)报道 CR 标签进入移动端;另有帖称 YouTube 在静默集成 C2PA。→ **含义:小徽章(pin)→点开检查器(inspector)的两级模式正被平台批量普及,用户教育成本在快速下降。我们的 印章→方法页 结构与之同构,保持;徽章视觉可参考 CR pin 的"小而可点"而非横幅。**
2. **"确定性 + 测试数"是从业者互信的通货。** Microsoft Agent Governance Toolkit 的传播帖(@bibryam,638 likes)卖点原话:"**deterministic** policy enforcement…**13,000+ tests**"。→ **含义:我们方法页里 "a program, not an AI judge" + "131 passing tests" 的措辞方向正确,应保留在显眼层级,不要藏进小字。**

未命中主题(Community Notes 设计复盘、"show sources" UX 批评)交由 Sonnet 工作流的 web 深搜覆盖(X 上这两话题被垃圾帖淹没)。
