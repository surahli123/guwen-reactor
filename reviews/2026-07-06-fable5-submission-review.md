# Guwen Reactor Capstone — 提交日端到端复审(Fable 5)

**日期:** 2026-07-06(截止 23:59 PT)
**VERIFIED_AGAINST:** origin/main @ 0c59b55 @ 2026-07-06 ~16:30 local
**评审方式:** Fable 5 orchestrator(视频视觉+音频、demo 双端浏览器冷读、Pages 状态)+ 3× OMC Opus 4.8 子代理(repo 复现 / claim 矩阵 / session 审计)。Codex xhigh 三线因 600s 硬顶全部超时,结论缺席(已在会话中熔断上报)。

> ✅ 定稿:全部四制品审毕,三个子代理结果已回填并对 HEAD 复核。结论:**条件 GO**(见文末)。

---

## 排名发现(BLOCKER / CONCERN / SUGGESTION)

### B1 [已解决 ✅ 2026-07-06 ~17:15] 线上 Pages 曾卡旧版原型 D
- **处置**:空 commit `a8914dd` 推 main 重触发 → 新构建 1 分钟内 `built` → 线上 "Flip the gate" 标记 0→2 处 → 浏览器目测新版(英文 hero + CTA + ①②③ tab)生效。demo 链接可提交。
- 原始诊断留档如下:
- 证据:线上 demo 截图(~16:20)= 竖排「世說新語」+「原型 D…」dev 标签,无英文 hero/CTA;`grep "Flip the gate"` 线上 0 处 vs 本地 2 处。
- `gh api pages/builds/latest` = `{commit: 0c59b55, status: building}`,但跨本会话 3 次查询(~16:30 / ~16:41 / ~16:57)**一直是 building** —— legacy 构建通常 <2 分钟,25+ 分钟未完成疑似卡死。
- 行动:**空 commit push 到 main 重触发 Pages 构建**,然后 curl 验证线上出现 "Flip the gate" 标记。**未翻新前不可提交 demo 链接。**

### B2 [已解决 ✅ 2026-07-06 ~17:35] YouTube 上传 + writeup line 214
- Owner 已上传:https://youtu.be/lLEzs0uBH8M(oembed 验证可访问,标题 "Guwen Reactor — Visible Faithfulness | Kaggle AI Agents Capstone")。
- writeup:214 占位符已替换并推送(commit `c684e19` → origin/main,raw.githubusercontent 复核确认)。YouTube 副本同时解除了"MP4 仅本地"的丢失风险。
- 剩余:Kaggle 表单提交本身(owner)。

### C1 [已解决 ✅ commit b92140c] README 把 136 标成 "engine" 测试数
- 已改为 writeup 拆分口径「131 engine tests; 136 in the full suite including 5 MCP-server wrapper tests」,raw 复核确认。原始诊断留档:
- README.md:117-119「The full deterministic engine (**136 tests**) runs in the build pipeline」;而 writeup:130 与 demo:1353 的口径是「engine **131** tests; full suite 136 incl. 5 MCP wrapper」。数字都真实(131+5=136),但同一个名词 "engine" 挂了两个数,交叉阅读的评委会抓到。
- 修复:README 采用 writeup 的拆分措辞。提交前唯一值得动手的文字修复。(发现:claim-audit 子代理;本会话已对 HEAD 复核 sed -n '116,120p')

### C2 [CONCERN·可辩护] 视频旁白 "a piece of the real engine runs right there in your browser"
- demo `gateCheck()`(index.html:865-879)= 引擎 5 规则中的 **2 条**(fact-contradiction + unhedged-motive)的 **JS 重写**,非 Python 引擎实际执行。writeup:179-180("two of the engine's rules, faithfully reproduced")与 demo UI 自身披露("subset of the engine… simplified matching")都诚实;视频旁白是四制品中最松的措辞,但屏幕角标 "LIVE RULE SUBSET IN BROWSER"(帧 f_025)承载了披露。
- 判定:**可辩护,不强制重录**;owner 可选收紧。

### C3 [CONCERN] TTS 品牌名发音疑似含混
- whisper 把结尾品牌句转成 "goo when reactor"(transcript line 38)。可能仅为转写噪声,但建议 owner 亲耳复核 3:30 附近 "Guwen Reactor" 发音;若含混,是否重录由 owner 定(draft 已被接受)。

### C4 [已解决 ✅ commit b92140c] 两个闸门布尔硬编码 True + TODO
- README Limitations 已加 bullet 点名 `source_policy_valid` / `workflow_integrity_pass` 为 default-pass stub,并申明真实内容闸门(零未支持声明 + coverage≥0.85 + safety deny-list),raw 复核确认。原始诊断留档:
- `evals/run_eval_suite.py:71` `source_policy_valid = True # TODO(4b/source)`、`:74` `workflow_integrity_pass = True # TODO(S9/4b.6)` —— 两者永不拦截导出。对一个以"deterministic gate, no trust-me"为论点的项目,较真评委打开该文件会 ding。
- 缓解:核心忠实性闸门是真的且被测(零未支持声明 + coverage≥0.85;`safety_pass` 走真实 `safety_check()`);代码注释自我披露 "default-pass with a TODO until their real steps land";writeup Limitations 泛化披露了 staging 但**没点名这两个 stub**。
- 修复选项:README/writeup Limitations 加一行点名(2 分钟),或接受现状。(发现:repo-repro;主会话已对 HEAD 复核 sed -n '68,82p')

### S1 [SUGGESTION] handover 声称视频 repo 有 "Red-team + Codex-critique reviews",实际 `reviews/` 只有 1 个文件
- `~/Documents/guwen-reactor-video/reviews/` 仅 `2026-07-03-video-redteam-claude.md`。不影响提交,影响 handover 可信度记录。

### S2 [SUGGESTION] `pip install -e .` 在干净环境 build 失败(根因已定,LOW)
- 根因:pyproject.toml 有 `[project]` 但无 `[build-system]`/packages 配置 → setuptools flat-layout 自动发现撞上 9 个顶层目录(`Multiple top-level packages discovered in a flat-layout`)。README 只用 `pip install -r requirements.txt`,评委不会踩到。可选修复:`[tool.setuptools] packages=["app","guwen_core"]`。(repo-repro 在一次性 venv 复现)

### S4 [SUGGESTION] `specs/writeup_outline.md:149-151` 有 `[PLACEHOLDER]` 行随 repo 发布
- 是规划归档文件(非真 writeup),但 grep "PLACEHOLDER" 的评委会看到。可加一行"planning archive"声明或忽略。(已对 HEAD 复核)

### S3 [SUGGESTION] "published" 动词漂移(README + demo)
- 项目纪律动词是 export/hand over(writeup、视频均守住);README:118「every **published** verdict」、demo index.html:1266/1353「**published** text/verdict」滑了口。语境里明显指"点灯导出的重述",非上线含义,不算过度声明 —— 顺手对齐即可。(claim-audit 发现,已复核)

---

## 视频逐帧+全文转写审查(✅ 完成,32 帧 @7s + whisper base.en)

| 检查项 | 结果 |
|---|---|
| 数字一致性(131 tests / 3-of-10) | ✅ 旁白 "backed by 131 tests"、"3 lamps lit…7 stay dark";帧 f_019 "3/10 已核实" |
| 动词纪律(hand over/export,无 publish/ship) | ✅ 旁白 "refuses to hand over"、"before anything is exported";帧 "trace before export"、"EXPORT BLOCKED" |
| motive-smuggle 框架 | ✅ f_025:"Every event is true. The invented reason is not anchored." + F01–F04 + 朱批 CONTRADICTED |
| 工具名(Claude Code/Codex/Antigravity) | ✅ 全片未提及(与 S5 refocus commit 7be48e5 一致)→ 无发音风险 |
| 视觉质量 | ✅ 1080p30 文字全部可读,双语排版统一,无 dev 泄漏;3:43 时长 |
| 待复核 | C1 "piece of the real engine"、C2 "Guwen" 发音 |

## Demo 双端冷读(✅ 完成,headless browser 1440×900)

- **本地新版(= 0c59b55,与将上线版本一致):90 秒冷读通过。** 英文 hero 一句话定位 + "3 of 10 stories verified · the other 7 left dark on purpose — we don't light a lamp we haven't checked" + 红 CTA + ①②③ 编号双语 tab。
- CTA 点击 → 直达管寧割席 + 考據卡(Source says「共園中鋤菜」/ Engine verdict ✓ VERIFIED (F01))。
- 闸门拨开 → **默认即 motive-smuggle 案例** ✅:"An ungated AI might write: Guan Ning cuts the mat because he envies Hua Xin's ambition."(整句红线划除)+ "Every event here is true — the source never states a motive… This is not keyword matching." + F01–F07 逐条核对。handover 的关键修复视觉确认。
- 线上版 = 旧原型 D(见 B1)。

## Repo fresh-clone 复现(✅ 完成 — repo-repro 子代理 Opus 4.8)

- **`pytest evals/ -q` → `136 passed in 3.93s`**;`--collect-only` = 136;`Python 3.14.4`(与 README pin 一致)。README Setup 逐字复现,干净安装。
- Secrets 扫描:干净(全部命中为良性:telemetry 字段名、路径穿越测试 fixture、字体 base64、市场调研文档提及 ElevenLabs)。
- 断链检查:README + writeup 相对链接全部存在。
- Junk 扫描:203 个 tracked 文件,无 .DS_Store/__pycache__/.env/.log。
- 发现:C4(闸门 stub)、S2(pip -e . 根因)、S4(outline 占位符)。

## Claim 矩阵 / writeup 冷读(✅ 完成 — claim-audit 子代理 Opus 4.8,关键引用已由主会话对 HEAD 复核)

**结论:8 项声明全部落到代码,无 BLOCKER。**

| # | 声明 | 各制品 | 代码事实 | 判定 |
|---|---|---|---|---|
| 1 | 测试数 | writeup/demo/视频 = "131 engine / 136 suite" | evals/ 131 个 `def test_`;+5 MCP wrapper = 136 | 数字准确;**README:118 措辞裂缝见 C1** |
| 2 | 3 亮 / 7 暗 | 四制品一致 | canon_gold.yaml 仅 G01-G03 有完整 facts+beats;tier2_registry.yaml G04-G10 显式「金标未建,灯火保持暗」 | ✅ 且结构上暗篇无法偷点灯 |
| 3 | 浏览器内=规则子集 | writeup/demo 明示 subset;视频最松(C2) | gateCheck() = 2/5 规则 JS 重写 | 可辩护 |
| 4 | 动词纪律 | writeup/视频守 export;README/demo 有 "published"(S3) | 无 ship/deploy 过度声明 | 轻微漂移 |
| 5 | motive-smuggle | 四制品同框架(事件全真、动机被拦) | structural_audit.py:84-87 B.4;fixture `subtle_motivation_spoof` + test_drift_injection.py | ✅ |
| 6 | MCP metadata-only | writeup:161;视频 "a pointer, never the raw source" | mcp_server.py:85-100 返回 source_id/char_count/URIs,从不返回 source_text | ✅ |
| 7 | demo 无 live LLM | "committed record, not live generation" | demo 零 fetch/XHR/外部请求 | ✅ |
| 8 | 引用文件存在 | — | designs/、specs/eval_plan.yaml、cover 均在;YouTube 占位符已知 | ✅ |

Writeup 冷读:limitations 段真诚(单标注者、LLM judge 仅 advisory、demo 子集、未 ship 的概念明说 "not in the repo today");无未兜底的最高级形容;"3 lit / 7 dark" 呈现为论点而非借口。

## Opus 4.8 session 审计(✅ 完成 — session-audit 子代理 Opus 4.8)

Handover 声明 vs 实际 tool 记录(16MB JSONL):

- **CONFIRMED**:narration v3 claim-honest;MP4 渲染+QA(首次渲染失败后 LOW_MEMORY 重试成功,未吞错);视频/writeup 动词对齐(grep 验证 "none found");70be508/693cf3f/74a77ef/0dd5f29/0c59b55 全部实推到 origin/main(push 记录逐条可查,origin/main HEAD=0c59b55)。
- **PARTIAL**:ElevenLabs 音频生成无本 session 记录(pre-compaction,仅 metadata+成品间接证据);demo 结构性修改大多在 compaction 前(commit msg + localhost 截图 QA 佐证)。
- **红旗 #1(已由本复审闭合)**:该 session **从未真正执行测试** —— 4 次 pytest 全是 `--collect-only`,"131/136 passing" 是沿用旧文本的断言。→ repo-repro 今日 fresh clone 实跑 **136 passed**,缺口闭合。
- 红旗 #2:线上 Pages 部署从未验证(honest 上报"still building")→ 即本报告 B1。
- 其余 pending 与 handover 的 Known PENDING 一致(YouTube/Pages/Kaggle 提交)。

---

## 跨制品一致性最终裁定

**一致(PASS)。** 四制品讲同一个故事:数字准确(131 engine + 5 MCP = 136,fresh clone 实跑验证;3-of-10 有数据结构背书且暗篇无法偷点灯)、motive-smuggle 框架四处同构、MCP metadata-only 有代码背书、无 live-generation 过度声明。仅存三处措辞级裂缝:C1(README 136-as-engine,最值得修)、C2(视频 "piece of the real engine",可辩护)、S3(README/demo "published" 漂移)。

## Go / No-Go 最终裁定

# **GO** ✅(2026-07-06 ~17:35 更新:两个 BLOCKER 均已关闭)

**必须(均已完成):**
1. ~~**B1** Pages 重触发~~ → ✅ `a8914dd` 重触发,线上新版验证通过
2. ~~**B2** YouTube + writeup:214~~ → ✅ https://youtu.be/lLEzs0uBH8M,`c684e19` 已推送
3. 剩余唯一动作:**Kaggle 表单提交**(owner)

**强烈建议(共 <10 分钟):**
3. **C1** README:118 改为 writeup 的 "131 engine + 5 MCP wrapper = 136" 拆分措辞
4. **C4** Limitations 加一行点名两个 default-pass stub(与项目的诚实论点自洽)

**Owner 自行决定(不改也可提交):** C2 旁白措辞、C3 "Guwen" 发音亲耳复核、S1-S4。

---
*评审执行记录:Fable 5(视频 32 帧视觉 + whisper 转写、demo 双端浏览器冷读、Pages API、全部子代理引用对 HEAD 复核)+ OMC Opus 4.8 子代理 ×3(repo-repro / claim-audit / session-audit)。Codex GPT-5.5 xhigh 三线因 600s 超时上限全部无产出,结论缺席(熔断后经 owner 定向改道 OMC)。*
