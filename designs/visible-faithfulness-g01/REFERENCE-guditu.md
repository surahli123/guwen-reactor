# 古舆图研究 → SVG 底图落地规范

- **来源:** Codex 研究 session(web search + LOC/Wikimedia 实爬,2026-07-02;首轮 10min 超时,次轮基于自身日志收尾)。原始日志:session tasks `b507aikzh`/`bf58xlbo6`。
- **用途:** 青绿舆图(map-lab / proto-d)的美学升级参照;标注 "from knowledge" 的条目未经页面核实。

## 1. 视觉语法表(五图)

| 图 | 可抄的绘图语法 | 证据页 |
|---|---|---|
| 禹迹图(1136) | 石刻拓片质感;精确方格网(计里画方);密集水系;海岸线笃定连续;小字刻名。山不是主角,地形用疏笔线符。 | loc.gov/item/2021668264 |
| 华夷图(1136) | 同拓片底,更重意象:山形符号、江湖、400+ 政区名、大段释文;密黑线,无比例逻辑。 | loc.gov/item/gm71005081 |
| 广舆图(1579) | 木刻图册页:分幅网格、竖排标注、细水路、省域小panel、图说——"地图作模块图册"的最好范本。 | loc.gov/item/2021666327 |
| 康熙皇舆全览图 | 测绘感:经纬/分幅网格、干净海岸水系、细晕滃、克制标注——"古图皮下的地理可信度"。 | loc.gov/item/74650033 |
| 彩绘绢本·延绥东路地理图本 | **青绿直接参照**:绢底设色、彩绘山/城/河/堡,地名写在贴上去的褐纸签上(paperLabelSlip!)。 | loc.gov/item/2021666330 |

## 2. SVG 可执行 tokens(12)
1. `jiliGrid` 方格网 1px,opacity .04-.09(禹迹图/广舆图)→ **已落地 proto-d**
2. `stoneRubbingFilter` 拓片质感(feTurbulence 位移)
3. `riverStroke` 单笔墨色蜿蜒 + 淡蓝衬笔;textPath 沿河标名
4. `coastStroke` 笃定连续海岸,不做现代水面填充
5. `mountainGlyph` 三瓣/锯齿山符簇,深脚 + 淡绿衬晕(山形词汇多样化的方向)
6. `atlasTile` 广舆图式分幅 panel(册页/凡例牌可借)
7. `paperLabelSlip` 褐纸签地名牌(延绥图本)——**签牌样式的史源背书**
8. `walledCity` 套矩形/圆 + 门齿 = 城池符
9. `verticalLabels` 竖排,按 都/郡/故事点 分级
10. `kangxiSurveyLayer` 隐藏经纬脚手架 + 淡格网定位(= 我们的 Albers 方案,史有先例)
11. `qinglüPalette` 石绿/石青/赭纸/朱砂
12. `denseButQuiet` 标注多而低对比;唯故事锚点用朱点/印

## 3. PD 素材直链(高清)
- 禹迹图 9849×10117 PD: upload.wikimedia.org/wikipedia/commons/3/35/Yu_ji_tu._LOC_gm71005080.tif
- 华夷图 9441×9493 PD: .../9/95/Hua_yi_tu._LOC_gm71005081.tif
- 广舆图页 4420×4658 PD: .../3/31/Guang_yu_tu_-_er_juan_LOC_2008623187-52.tif
- 康熙耶稣会图幅 12186×9694 PD: .../e/e5/Der_Jesuiten-Atlas_der_Kanghsi-Zeit_-_China_und_die_Aussenlaender_LOC_74650033-12.tif
- 坤舆万国全图全幅 14982×6862 PD: .../2/20/Kunyu_Wanguo_Quantu_by_Matteo_Ricci_All_panels.jpg
- 延绥东路图本 IIIF 5207×4837(权利未明,商用前核):tile.loc.gov/.../wdl_07096

## 4. 地点考订(册页锚点行已采用)
- **管寧**:《三國志·卷11》「管寧字幼安,北海朱虛人也」→ 朱虛(今山东临朐-安丘间)~118.8E,36.5N,precision medium。
- **王戎**:《晉書·卷43》琅邪臨沂人 → 118.35E,35.05N。
- **詠雪**:《世說新語·言語》仅「謝太傅寒雪日內集」,**地点史文未明** → 以建康烏衣巷(118.78E,32.04N)作接受史/門第地理锚点,非事发实址;会稽东山留给"东山再起",不作詠雪默认点。凡例口径已按此写。

## 5. 现代复刻技法(标注:from knowledge,未逐一核页)
真实地理作隐形脚手架+轻微手卷形变 · DEM/晕滃量化成墨脊+青绿罩染 · 高密度竖排标注分级低对比、唯故事锚点着色 · 古图panel×故事pin(线程路由/印点/短竖注) · 动效克制(墨晕显现/慢平移/河光,拒绝现代 marker 弹跳)
