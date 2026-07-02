# Changelog

All notable changes to Guwen Reactor. Format: [Keep a Changelog](https://keepachangelog.com); dates are ISO (YYYY-MM-DD).

## [Unreleased]

### Added — 2026-07-01/02 — 山河卷多篇中心站(原型 D)+ 真投影舆图 + EN-first 信任层
- **舞台三原型 A/B/C**(单变量实验)→ owner 圈定 B/C → **三线评审合议 C-modified**(5×Opus workflow + Codex critique theatre(真调 `open-design-critique-theater`)+ baoyu 准则 critic;7 视角一致),B 降级篇内可选;5 项 BLOCKER 修法 → `reviews/2026-07-01-proto-bc-synthesis.md`。
- **proto-d 多篇中心站**:节点=文章(G01/G02/G03),beat 下沉册页;篇目榜(門類分组、中性排序);按篇灯火诚实(仅 G01 亮);印章作用域注(已核实 1/3 篇);密度预览(12 签牌);展卷 localStorage 首访一次(Q2 拍板)。
- **底图两次革命**:手绘 SVG(r1-r4 画室迭代)→ **Natural Earth 50m + Albers(25°/47°N,105°E)真投影**(owner 要求真比例+真地点):轮廓/长江黄河/40 山系全部经纬重锚;驿站=考订地点(朱虛/建康/臨沂,引线指真锚,册页锚点行带史源,詠雪注明"地點史文未明依門第")。古图研究(Codex web 实爬 LOC/Wikimedia)落地:计里画方淡网格、山形三族(丘/三瓣符/低脊晕)、河流双笔+竖排河名、建康城郭符、褐纸签签牌、洛陽/長安/會稽静默标注 → `designs/visible-faithfulness-g01/REFERENCE-guditu.md`(含 PD 高清直链)。
- **EN-first 信任层**(主用户=英语教育者):两道关口径、考据卡加事实英文释文(canon_gold 逐字)、**朱笔闸门接线**(实弹演示:编造句被抓→CONTRADICTED·export BLOCKED,chip 翻面已取证)、**言必有據方法页**(4 步+诚实声明"构建期核验,页面展示记录在案判定")、面板开时控件签牌左移(两次同类 z-index bug 教训)。
- **信任UX三方研究**:自研提案 `TRUST-UX-PROPOSAL.md` + X 实战信号(agent-reach;营养标签隐喻/确定性+测试数=信任通货)+ **Sonnet 5 六路 web 深搜** `TRUST-UX-RESEARCH.md`(Top-8+反模式+签名动作,全量 JSON 入库)。**Owner 已拍板执行;签名动作 = 闸门失败演示浏览器内真跑引擎规则子集并前置。**
- 评审归档:`reviews/2026-07-02-map-critique-theatre.md`(Keep-with-fixes,3 BLOCKER 当场修毕)。
- 全程验证纪律:每改 serve + 0 外部请求 + console 0 错误 + 截图亲验(shots/ 过程稿 19MB 留本地不入库)。

### Added — 2026-06-30 — Phase 4b pipeline + Phase 5.2 canvas (offline prototype complete)
- **Phase 4b (Wave 2):** `safety_eval` (deterministic deny-list, wired real into `evaluate_run`), `regen_loop` (`run_with_regen`, fail-closed at 3 attempts), `trace` + `workflow_integrity` (OTel JSONL + IN_ORDER; event-vocabulary conformance-locked to the YAML), `approval` + `export_bundle` (refuses unless content-clean AND human-approved; sha256 + AIGC-label manifest), and **`app/cli.py`** — the non-cuttable e2e: `run <dir> --approve` exports; a drift run is BLOCKED with no manifest.
- **Phase 5.2:** `render_canvas` → self-contained no-key `docs/demo/index.html` (D5: zero external refs, 19 tests).
- **Independent code review of the eval core caught + closed a MAJOR `beat_id=None` gate bypass** before it shipped (a beat-less claim citing a real beat-owned fact now BLOCKS).
- **`pytest evals/` = 131 passed.** Commits `4f8e0a7`, `adc8b4f`, `19784fd`.

### Changed — 2026-06-30 — demo direction reframed (owner review)
- The static demo canvas (storyboard + gate table) was **rejected by the owner** as "just a Chinese→English translation, not demo-ready." The engine (131 tests) is sound and reusable; the *presentation* was throwaway.
- **New demo concept: "看得见的忠实 / Visible Faithfulness"** — an engaging grounded retelling where clicking any line reveals (考据-style) the original Classical Chinese it is grounded in + a ✓-verified stamp, plus a "如果没有闸门" toggle showing what an ungated AI would fabricate. Faithfulness made *visible and tactile*, not a table. "Trustworthy cultural education" is the framing; the gate is the quiet trust layer.
- **Aesthetic target:** 《中国诗词山河卷》 handscroll style (青绿山水 on silk, glowing data-lights, woodblock 册页 panels, seal-red, serif). Its **考据** (provenance) feature maps exactly onto our faithfulness-provenance — same interaction.
- **Tooling:** installed `baoyu-design` (the Claude Design engine, global `~/.claude/skills/`) as the front-end design tool; audited it (Med-Risk score = Playwright/esbuild deps, not malice; core path is offline). `render_canvas` / `index.html` will be **superseded** by the new baoyu-design build.

### Added — 2026-06-28 — Phase 2 (security core) + Phase 3 (fixtures) + Phase 4a (eval core — the wow)
- **Adversarial review of the session goal spec** (4 OMC lenses + independent Codex, refute-verified → execute-with-edits, 0 blockers): 6 reconciliations applied before the build (`reviews/2026-06-28-goal-spec-adversarial.md`). A follow-up independent code review of the eval core then caught + closed a **MAJOR `beat_id=None` gate bypass**.
- **Phase 2 — security core:** `guwen_core/source_sanitizer.py` (NFKC + zero-width strip + sha256), `guwen_core/safe_prompt.py` (fenced judge prompt + `detect_injection`), `app/policy_gate.py` (loads the single canonical gate; injection + fact-id gated). (Built earlier; now recorded.)
- **Phase 3 — fixtures:** `runs/demo_clean/{adaptation,structured_claims}.yaml` (G01, 10 claims, beat-aligned, coverage 1.0) + `guwen_core/adaptation_gen.py` (offline loader; live Gemini stays `[CONTRACT]`/S13). `.gitignore` carve-out so the demo fixtures are committable.
- **Phase 4a — eval core (NON-CUTTABLE; the deterministic faithfulness gate):** `claim_validator.py` (Contract A) · `structural_audit.py` (Contract B, **strengthened rule 5: beat↔fact-id alignment** — blocks fabricated events citing real-but-wrong / undeclared-beat ids) · `coverage.py` (Contract C, plot-claims only) · `evals/run_eval_suite.py::evaluate_run` (Contract E, stage-aware `export_status`) · specificity over-block guard (Contract G).
- **`pytest evals/` = 65 passed.** Clean fixture → `READY_FOR_APPROVAL`; injection / invalid-id / forbidden / unhedged-motive / empty-id / wrong-beat / beat-less-bypass → BLOCKED; valid hedged interpretation → not blocked.

### Added — 2026-06-26 — Phase 1 (schemas + sources + 3-scene chinese-anchored gold)
- **Scene picks** (research + adversarial-labelability workflow, one decision at a time): video=三顧茅廬; 3 measured eval scenes **G01 管寧割席 · G02 詠雪 · G03 道旁苦李**; gold check = route 2+3 + second-reader cross-validation (deferred).
- **Protocols:** `docs/plan/gold-cross-validation-protocol.md` (2-reader blind, percent-agreement + κ small-N caveat) + `docs/plan/annotation-guardrails.md` (通用 + 每場景 + specificity/drift two-way proof).
- **Task 1.1** `guwen_core/schema_validator.py` + `evals/test_schema.py` — `StructuredClaim` (Contract A) + chunk-anchored `AtomicFact` (Contract D) + enums (TDD RED→GREEN).
- **Task 1.2** locked 3 scene `source.zh.txt` + `source_metadata.yaml` (`english_translation_ingested:false`) + `_fixture_unclear_license` (Phase-2 negative fixture).
- **Task 1.3** `data/gold/canon_gold.yaml` (G01 10 facts / G02 9 / G03 9, every fact chunk-anchored) + `data/gold/independent_check_notes.md`. **`pytest evals/` = 7 passed.**
- **Adversarial gold audits** (3-lens workflows) caught real contamination in 3/3 scenes (incl. 2 in the spec's own G01 gold) → fixes applied; single-annotator / no-IAA disclosed, human denotation check pending.

### Added — 2026-06-22 — repo genesis + Phase 0
- Initialized the project repo from the `~/notes/kaggle-vibecoding/` planning trail (`docs/planning/`).
- Implementation plan `docs/plan/implementation-plan.md` (1094 lines) — structured-claim generation + deterministic structural-audit eval core.
- Locked decisions **D1–D4** + contracts spine (`docs/plan/decisions-locked.md`); review-gauntlet trail (`docs/plan/reviews/`: eng-review, independent Codex adversarial, reconciliation).
- **Phase 0:** Python env (3.14.4, pinned deps), `evals/test_env.py` (passing), package skeleton.
- Seed specs: **`specs/eval_plan.yaml`** (the single canonical export gate), `product_spec`, `threat_model`, `behavior.feature`, `demo_script`, `writeup_outline`; `AGENTS.md`; `docs/build_log.md`; `docs/capstone_writeup.md` stub.
- Live decision board `docs/plan/session-map.html`.

### Notes
- Eval core is **offline-fixture-first**; live Gemini/MCP/ADK auth is an owner action, off the critical path.
- Python 3.14 is bleeding-edge — reproducers/judges should use **3.11–3.13** (`requires-python = ">=3.11"`).
