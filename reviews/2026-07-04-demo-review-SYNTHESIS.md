# Demo Design + Storyboard Review — 4-lens SYNTHESIS + fix plan

VERIFIED_AGAINST: docs/demo/index.html @ origin/main 0dd5f29 · 2026-07-04
Lenses: OMC designer · OMC code-reviewer · OMC critic (Opus, adversarial) · Codex open-design-critique-theater · + impeccable narrative critique (2026-07-04-demo-narrative-impeccable.md). Every finding re-anchored to file:line.

## Unanimous verdict: FAILS a 90-second cold read by a non-Chinese judge. NOT submission-ready as-is.
Codex critique.score **2.0/5**; critic **REJECT**; designer + impeccable concur. The engine + story are genuinely strong; the failure is **placement, order, and language-surfacing — not writing quality**. Every fix below is copy/CSS/one-line-JS, not a rebuild. The Chinese source stays Chinese (that's the point); we wrap an **English scaffold** around it.

## CONSENSUS BLOCKERS (multiple lenses agree — high-confidence must-fix)

**B1 — No English orientation on landing (all 4).** First thing a foreign judge sees = "a pretty Chinese map." Giant Chinese title (`.title-vert` :538), Chinese-only tabs (:544-546), Chinese status (:541), and a dev-label squatting the prime tagline slot (:548). They can't state what this is in 5s. → Add an English hero line.

**B2 — The WOW shows the WEAK proof and hides the differentiator (critic, verified — the killer finding).** `GATE_CASES` (:812-816) defaults to case A (`gateCaseIdx=0`, run at :1185): "slips the gold into his sleeve and keeps it" → F04 CONTRADICTION — reads to a skeptical engineer as **keyword/fact diffing**. Case B — the motive-smuggle ("Guan Ning cuts the mat because he envies Hua Xin's ambition", all events pass, only the invented motive blocked :814-815/:850-854/:1156-1160) — is THE "not keyword matching" proof and is hidden behind "Try another fabrication ↻" (:1188), absent from all 4 storyboard frames. → **Reorder GATE_CASES so case B leads** (one-line) + explicit English contrast line.

**B3 — The WOW is buried / no self-guiding path (all 4).** Gate-flip is a small bottom-left corner card (`#gateCard` :551-555) sharing its column with a competing seal stamp; its one dynamic cue `pulse` fires **once ever per browser** (localStorage `gw_gatecard_seen` :1362-1368) — dead for any judge whose profile previewed the page. No sequence puts the judge on frame 1→2→3→4. → Make **"▶ Flip the gate — watch a fabrication get caught"** the single hero CTA, routed via existing `goGateDemo` (:1266-1277), static (not pulse-once).

**B4 — Dev-scaffolding leak (all 4).** `原型 D · 多篇中心站(真投影舆图+篇目榜) · LXGW 文楷内嵌` (proto-tag :548, `.proto-tag` :190-195) top-center on every frame + same in `<title>` (:6). Unprofessional; occupies the English-tagline slot. → Delete both.

**B5 — The "3 of 10 verified" trust beat is invisible / misreads as "unfinished" (Codex, designer, critic).** `已核实 3/10 篇` renders at 10.5px, dimmest ink, Chinese-only (:541); the framing that makes it a *strength* ("7 dark on purpose") is 3 clicks deep in the Method panel (:1297). A foreigner defaults to "they finished 3 of 10" — turning the honesty thesis into evidence *against* the project. → English gloss on landing: "3 of 10 verified · 7 left dark on purpose — we don't light a lamp we haven't checked."

## CONSENSUS CONCERNS
- **C1 tabs no English/sequence** (all 4) → ① Stories · ② How it's checked · ③ Flip the gate (bilingual, numbered). `btnGate` aria is already EN but invisible to a sighted judge.
- **C2 English station names collide** (all 4) → see the DIVERGENCE below.
- **C3 intro-animation skip is Chinese-only** (designer, :560 "点击任意处跳过展卷") → bilingual "Click anywhere to skip". A judge burns ~4% of 90s not knowing they can skip.
- **C4 "export BLOCKED" jargon** (critic, :1173/:1178) → "REJECTED — would not ship" (no antecedent for "export" to a cold judge).
- **C5 problem beat + target-user (educator) never stated on-surface** (critic) → covered by the B1 hero line.

## DIVERGENCE — overlap fix (owner call)
Root cause (code-reviewer, HIGH): **two label layers, two scaling laws** — HTML `%`-positioned stations vs SVG `viewBox`+`preserveAspectRatio:slice` place-names (:461/:1371). Cross-layer drift at any non-authored aspect ratio. **Geometry, not CSS — do NOT chase by moving coords.** But the station-to-station English collision IS pure CSS (`.st-en` :127 is an unconstrained flex item → long names balloon → lap neighbors).
- **Option A (code-reviewer, recommended): bound `.st-en`** `max-width:~92px; white-space:normal; line-height:1.1` — edit ONLY :127. LOW risk. **Keeps English visible on the map** (foreign judges need it).
- **Option C (designer): hide `.st-en` by default, reveal on hover/focus.** Declutters fully, but **hides the only English a foreigner can read on the map** — worse for the foreign-judge goal.
→ **Recommend A** (bounded-visible) + ensure English is also in the index panel + hero line. A judge keeps a readable map.

## SAFE-IMPLEMENTATION MAP (code-reviewer — obey these)
- English names ALREADY exist in data (`title_en`/`men_en`, :576-768) — reuse only, no authoring.
- All chrome elements are id/class-anchored, one per line → surgical: title :538, status :541, tabs :544-546, proto-tag :548, footer :556, hint :549 (already bilingual — replicate its pattern).
- **FROZEN — do not touch:** SVG place-name layer (:1524-1564), `GEO` const **:1371** (one ~30KB line — prior slicing accident lives here; NEVER byte-offset edit near it), station geometry tables (`station.x/y` % ⟷ `GEO.PTS` ⟷ `STATION_OFFSETS` :1567 ⟷ `POFF` :1528).
- 4 twin-prefix EN classes — name the right one: `st-en`(map :127/885) · `p-title-en`(panel :925) · `idx-en`(index :1071) · `gc-en`(gate card :553).
- `node --check` FAILS on .html (ESM) — verify JS by extracting the `<script>` body to a `.js` then `node --check`. Anchor every edit to a unique string, never a byte offset.

## Fix plan, ordered by leverage
**Tier 1 (highest payoff, cheap):**
1. **Reorder `GATE_CASES` → motive-smuggle (case B) first** + English contrast line (B2). One-line array + a caption string.
2. **English hero line** at top-center, replacing the deleted proto-tag: "Visible Faithfulness — Classical Chinese → English, every sentence checked against the source · 3 of 10 verified, 7 left dark on purpose." (B1 + B5 + C5).
3. **Hero CTA** "▶ Flip the gate — watch a fabrication get caught" → `goGateDemo`, static (B3).
4. **Delete proto-tag (:548) + fix `<title>` (:6)** (B4).

**Tier 2 (cheap, clear):**
5. Tabs → ① Stories · ② How it's checked · ③ Flip the gate (C1).
6. Overlap: bound `.st-en` :127 (Option A) (C2).
7. Bilingual intro-skip (:560) (C3).

**Tier 3 (polish, if time):**
8. "export BLOCKED" → "REJECTED — would not ship" (C4).
9. Dim Chinese place-name layer opacity (declutter) — CSS only, not coords.

## Method of implementation
Incremental: one fix → `browse` screenshot → verify → next. Nothing near :1371 / SVG layer. Verify JS edits via extracted-`.js` `node --check`. Full set done → owner reviews the rebuilt storyboard → then commit + push (updates live Pages).
