# 国风 vibe-coding 研究手册 → 落地 G01 山河卷 demo

*来源：后台深度研究 workflow（6 路 · 对抗验证）。原始发现存于 workflow 输出；本文件是**按我们约束裁剪**的可执行提炼。*

## 0. 一个诚实更正（要告诉 owner）
研究**没能**在任何可检索来源找到「胡言乱语」其人或《中国诗词山河卷》/诗词地图2.0——全网搜索、B站、X、GitHub 皆空（内容大概率在小红书，登录墙挡住）。找到的最接近技术类比是 GitHub `waysguo-rgb/shici-shanhe`（Vue3+Three.js，Claude 协作），但**无法证明**与「胡言乱语」有关。
→ **对我们无影响**：owner 直接给了 6 张真实截图，那才是我们对标的**视觉地面真值**。研究只能给"通用技法+反套路"，不能替代截图。"如何造的"是从类比 repo 推断，非确证。

## 1. 关键约束再确认
单文件 · 离线 · 无 CDN · vanilla CSS/JS/SVG · 系统字体或**内嵌子集字体**。研究反复确认：**离线零依赖本身就是这个美学的加分项**（"随处能展开的古卷"感）。

## 2. 视觉技法速查（全部纯 CSS/SVG，离线可用）— 来自 finding #3/#5
| 目标 | 技法 |
|---|---|
| 宣纸/绢本纹理 | SVG `feTurbulence`(fractalNoise, baseFreq 0.02–0.2, octaves≤5) → `feDiffuseLighting`(surfaceScale 2, distantLight az45 el60)，`filter:url(#paper)` |
| 墨渗边缘 | `filter: blur(1px) url(#threshold)`；threshold = `feComponentTransfer/feFuncA discrete tableValues="0 1 1 1"` |
| 毛笔不规则边 | `feTurbulence` + `feDisplacementMap`(scale 10–50) 扭曲干净矩形/路径边 |
| 青绿层峦 | 3–5 层**平涂矿物色带**剪影 + `mix-blend-mode:multiply`(墨)/`screen`(雾) + `mask-image:linear-gradient` 渐隐。**用平涂色带，不要平滑渐变**（渐变=扁平图标味） |
| 手卷横向展开 | CSS scroll-driven animation (`animation-timeline: scroll()/view()`) + IntersectionObserver 兜底(Safari/FF) |
| 灯火暖光 | 叠层 `box-shadow`(多层暖色，核→环) + `radial-gradient` + 轻微 `brightness/opacity` 闪烁 |
| 印章 | `radial-gradient`+粗边框 + turbulence/displacement 边缘 + `rotate(-3°~3°)` + 白文(白字红底)/朱文(红字白底) |
| 书法"写出"动画 | SVG mask + `stroke-dashoffset`（笔画切成不重叠段，按笔顺揭示） |

## 3. 颜色（矿物/朱砂真值）— finding #3/#5
- **朱砂/印章红**：橙偏红，非 `#FF0000`。用 `#B23A28`~`#9E3327`（做旧印）或 `#E34234`(朱紅)。研究点名 `#FF0000/#E74C3C` 是"品牌红"套路。
- **石青/石绿**：研究**警告**色卡工具给的 `#0BDA51`(霓虹绿)是**错的**——真矿物色**发暗**。我从截图取的 `#2E5A6E`(石青) / `#3E7359`(石绿) 是发暗的，**以截图为准**。
- **基调**：墨/沉香米色为主；青绿/朱砂/琥珀只作**稀疏点缀**。
- **边缘积墨**（boundary 处颜色变深）= "最像水墨"的单一最强技巧，优先于堆细节。

## 4. 字体（离线，硬约束）— finding #5
- macOS 系统 CJK（离线零下载）：**行楷 Xingkai SC / 魏碑 Weibei SC**（标题，克制用）· **宋体 Songti SC / STFangsong**（正文，"刻本"register）· **楷体 Kaiti SC/STKaiti**（引文/注）· **Hannotate SC**（手写体→朱批）· **PingFang SC**（chrome）。
- **跨机风险**：Kaggle 评委/GitHub Pages 观众可能是 Win/Linux，无这些字。→ **标题**用**内嵌子集字体**（LXGW 文楷，SIL OFL 免费商用；`pyftsubset` 只留我们用到的 ~30 字：管寧華歆割席世說新語德行… → 几 KB → base64 内嵌）；正文退化到 `Songti SC, STSong, SimSun, "Noto Serif SC", serif` 可接受。
- Latin（英文读本）：系统衬线 `"Iowan Old Style", Palatino, Georgia, serif`（离线）。

## 5. 交互（考据像"注疏"，不是表格）— finding #6
- 提供层要**可选、分层、点击触发**（非 hover）；**绝不**用打断滚动的模态框。
- 考据面板 = **传统眉批/注疏**风：小字、墨灰、衬线，与正文**排版区分**；**不要** app 卡片/徽章/表格外观（← 正是 v1 被否的病根）。
- 参考模式：ctext.org 段旁"图标栏"点开来源；识典古籍 opt-in 叠层（释义/白话/底本对照/实体高亮）。
- 手卷方向：正统**右→左**展开；若左→右须是**明示**的设计选择。

## 6. 反套路清单（"一眼假"）— 综合
- ✗ 霓虹翡翠绿+金 "奇幻武侠" 配色（不对应真矿物色）。
- ✗ 完美平滑矢量山 + drop-shadow（=扁平图标）。
- ✗ 红灯笼/龙/祥云 clipart 贴在现代 UI 上。
- ✗ 居中对称 hero（真山水=非对称、对角走势）。
- ✗ 完美圆/方的清爽印章（真印有渗墨、错位、微旋）。
- ✗ 玻璃拟态/新拟物 混进水墨。
- ✗ 滚动劫持/激进视差（毁掉手卷的静观节奏）。
- ✗ AI 生成画面内的中文字/印（结构错=一眼假）——我们的字全是真数据，天然规避。
- ✗ 满屏堆特效（花瓣+粒子+视差+印章脉动同时）——留白 60–80%，一次一个主导动作。

## 7. 背景资产（青绿山水底）— finding #4
两条离线路径：
- **A 纯 CSS**（finding #3 层峦技法）：零资产、极小、真离线；但要靠 turbulence 边缘破"扁平"感才不 slop。
- **B 公有领域真迹**：王希孟《千里江山图》——Wikimedia Commons `Category:A_Thousand_Li_of_Rivers_and_Mountains`（14 文件，PD 可直接用）/ 书格 / Met CC0 / 台北故宫 CC BY。裁一条 crop 作绢底，base64 内嵌→单文件离线。**陷阱**：大陆故宫"名画记" minghuaji.dpm.org.cn = **仅浏览、不可下载**，绕开。
- **我的建议**：**v1 先用 A（CSS 底，最快出可玩原型）**，把 B（真迹 crop）作为**可选增强**——契合你"分步可改、原型上改比空想快"。真迹底能瞬间锁死青绿观感，需要我去 Wikimedia 拉一张 PD crop（自动化，非手动）。

## 8. 本次 demo 的构件映射（山河卷语法 → 忠实）
- **灯火**（原义:诗篇多少）→ **已核实之光**：亮琥珀灯 = 此句已核实。
- **考据**（原义:诗人与城的记忆）→ **忠实溯源**：点句 → 文言短语高亮 + 已核实 claim + 印章「✓出自《世說新語》·Fxx」。
- **印章**（authentication）→ 信任徽章（事实层）。
- **朱批**（correction）→「如果没有闸门」假句的朱笔勾去 + 拦截理由。
- **册页/注疏** → 考据面板的排版语言。
- **留白 + 右→左手卷** → 整体布局与节奏。
