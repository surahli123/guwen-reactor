# Scout: Novel → Comic / Video / 吐槽 — Product Hunt + GitHub + Bilibili
Date: 2026-06-20 | Window: last ~30 days primary, widened to year for sparse signals

---

## Summary: Crowded vs. Gap

| Layer | Crowded? | Gap? |
|---|---|---|
| Generic text→comic (any prompt) | YES — Anifusion, Dashtoon, Adobe Firefly, Elser AI, Canva | Personalization on *user's reading list* absent |
| Chinese 网文→AI漫剧 (B站, Douyin) | YES — 180k新剧 Q1-2026 alone, industrial scale | Per-user "books I read" framing absent |
| 三国/古文 吐槽解说 videos | YES — 特级盘点师 700k+ views per episode | AI-*automated* 吐槽 pipeline from novel text = open |
| Personalized novel→comic (your reading) | NO EXISTING TOOL FOUND | Clear whitespace |
| Personalized novel→short video (your reading) | NO EXISTING TOOL FOUND | Clear whitespace |
| Auto-吐槽 script generator from novel text | NO EXISTING TOOL FOUND | Clear whitespace |

---

## Signals

### 1. B站 AI 网文→漫剧 全教程 (novel→video pipeline, industrial)
- **Video:** 【AI漫剧】目前B站最全最细的AI漫剧制作零基础到精通教程 (BV1kiEu65E48)
- **Author:** AI视频轻松学
- **Engagement:** 46,149 views · 510 弹幕 · 3,049 favorites · published 2026-06-08 (12 days ago)
- **URL:** https://www.bilibili.com/video/BV1kiEu65E48
- **Signal:** Active demand for step-by-step "novel→AI video" tutorials right now; 46-part series, 591-min runtime. Audience is creators who want to monetize web novel IP as short dramas. The pipeline is: novel text → scene breakdown → AI image/video generation → voiceover. No personalization on *reader's* library — it's supply-side (content creators), not reader-side.

### 2. B站 吐槽新三国 系列 — 702k views per episode
- **Video:** B站吐槽新三国001 (BV1JpH1e3ECo)
- **Author:** 特级盘点师
- **Engagement:** 702,889 views · 3,809 弹幕 · 15,794 likes · 6,700 favorites
- **URL:** https://www.bilibili.com/video/BV1JpH1e3ECo
- **Signal:** 吐槽/commentary on classical Chinese novels (三国 = Romance of the Three Kingdoms) is a massive genre. This single episode: 700k views. The creator recruited 12+ other UP主 to co-吐槽. Format = group sarcasm+reaction on novel adaptation. No AI automation — entirely human written. Whitespace: an AI pipeline that reads *the novel you finished* and generates a 吐槽 script tuned to your reading notes.

### 3. B站 万古史官 — 5.35M views, 114k favorites (novel解说)
- **Video:** 《万古史官》01：三国演艺被老师说成垃圾 (BV12z4y1x7v1)
- **Author:** 晚轩推书
- **Engagement:** 5,351,565 views · 5,610 弹幕 · 47,906 likes · 114,546 favorites
- **URL:** https://www.bilibili.com/video/BV12z4y1x7v1
- **Signal:** 解说/book-commentary style video on Chinese classics = proven mass market (5M+ views). This is essentially "I read Romance of the Three Kingdoms and here's my commentary." 114k favorites = very high save rate (people re-watch). The gap: no AI tool takes *your* reading and generates a script in this 解说 style.

### 4. B站 假如古代有Deepseek — 6.17M views (AI × 古文 humor)
- **Video:** 假如古代有Deepseek，诗人会集体失业吗？(BV1dgfPYZEJV)
- **Author:** -古人云-
- **Engagement:** 6,169,169 views · 602 弹幕 · 62,958 likes · 88,351 favorites
- **URL:** https://www.bilibili.com/video/BV1dgfPYZEJV
- **Signal:** AI × classical Chinese literature humor = 6M views in <3 months. Proves Chinese audience deeply responds to AI-meets-classical-literature format. This is a 2.5-min short-form riff. Gap: systematic AI tool to generate this type of content from novels the user has read.

### 5. B站 三国:讨董 AI电影 — solo creator, 75k views, 2026-06-06
- **Video:** 《三国：讨董》126分钟，90天，一个人制作 (BV1dh7m6MEtz)
- **Author:** 泺仁制作
- **Engagement:** 75,694 views · 660 弹幕 · 3,524 likes · 2,545 favorites
- **URL:** https://www.bilibili.com/video/BV1dh7m6MEtz
- **Signal:** Solo creator used AI (Seedance 2.0) + 90 days → 126-min historically faithful novel adaptation. Shows the upper bound of what's possible with current tools. The demand signal: comments show audience wants *more* of this. The pain: 90 days for one creator. An agent that does this for a novel you finished, in hours, = the gap.

### 6. B站 AI漫剧 市场数据 (industry scale)
- **Source:** 大洋网/DataEye report via Bilibili search (2026-02)
- **Engagement:** 阅文 (Tencent literature) 10 works crossed 100M plays; 100 works crossed 10M plays in 2026
- **URL:** https://news.dayoo.com/gzrbrmt/202602/11/170636_54927937.htm
- **Signal:** Chinese AI-manga-drama market grew 12x YoY in H1 2025. Q1 2026: 180k new 漫剧 launched. Market size projected 240B yuan 2026. This is industrial-scale 网文→video. Whitespace is the *reader-facing* (not creator-facing) personal adaptation layer.

### 7. Reddit r/ProgressionFantasy — wuxia/xianxia cultural guide: 1,594 upvotes
- **Post:** "I grew up in China on wuxia novels. Here's everything I wish Western readers knew..." (1rzpm3n)
- **Author:** No-Ride-3370
- **Engagement:** 1,594 upvotes · 296 comments · r/ProgressionFantasy
- **URL:** https://www.reddit.com/r/ProgressionFantasy/comments/1rzpm3n/
- **Signal:** Western readers of xianxia/wuxia novels have massive appetite for content that helps them process what they read. The post got 1,594 upvotes as a *guide* — meaning readers want deeper engagement with what they finished, not just the novel itself. An AI that generates personalized 解说/commentary/visual summary of the novels they've read maps directly onto this need.

### 8. Reddit r/comicbooks — Valiant AI animated adaptation launch: 222 upvotes
- **Post:** "Valiant is planning to launch a new service that uses generative AI videos to create 'animated adaptations' of their comic series" (1tkl0z0)
- **Author:** WhyPlaySerious
- **Engagement:** 222 upvotes · 110 comments
- **URL:** https://www.reddit.com/r/comicbooks/comments/1tkl0z0/
- **Signal:** Major publisher (Valiant) launching AI video adaptation of their IP, monetized behind coins. Proves the commercial model (novel/comic IP → AI animated episodes → paywall) is being validated by professional players. Individual reader-facing version = gap.

### 9. GitHub: AI Comic Factory (jbilcke-hf) — 1,329 stars
- **Repo:** github.com/jbilcke-hf/ai-comic-factory
- **Stars:** 1,329 | last commit 2026-06-18 (actively maintained)
- **Description:** Generate comic panels using LLM + SDXL. Powered by Hugging Face.
- **Signal:** Most-starred open-source text→comic tool. Input = text prompt → comic panels. No novel ingestion, no reading-list personalization, no Chinese classical style, no 吐槽 mode. Proves OSS demand exists but functionality is generic. Gap: fork/wrapper that accepts novel chapters + reader annotations → styled comic + commentary.

### 10. Elser AI — PH viral, text→anime/comic/short film
- **Source:** Elser AI Blog + search results (2026)
- **Engagement:** "climbed to the top of Product Hunt" (specific vote count unavailable — PH page requires login for historical data)
- **URL:** https://www.elser.ai/blog/best-ai-comic-generator-in-2026-create-stunning-comics-in-minutes
- **Signal:** All-in-one AI anime/comic/short film generator went viral on Product Hunt 2026. Confirms PH market responds to text→visual tools. Still generic prompt-based, not novel-input or reading-list aware.

### 11. Anifusion — ranked #1 AI manga generator 2026
- **Source:** Anifusion.ai product page + comparison article
- **Engagement:** Product rating 5.0 on Product Hunt (3 reviews; small sample)
- **URL:** https://anifusion.ai
- **Signal:** Leading commercial manga-from-prompt tool. Character consistency across panels is now solved ("seed locking, lightweight fine-tuning"). Closes the art quality gap that blocked earlier text→comic tools. Still: input is free-form prompt, not a novel the user read. No classical Chinese or 网文 style presets mentioned.

### 12. Chinese AI漫剧 cost signal — 6万元 per episode (validation of economics)
- **Source:** 澎湃新闻 / thepaper.cn (2025)
- **URL:** https://m.thepaper.cn/newsDetail_forward_32221141
- **Signal:** One AI漫剧 episode costs ~¥60,000 (~$8,300) to produce, vs. traditional animation 5-10x that. "AI救活了网文" (AI revived web novels that couldn't get traditional adaptation). This is the creator-side economics. Reader-facing personal adaptation at near-zero cost = the gap this project could fill.

---

## Whitespace Summary

**What does NOT exist (as of 2026-06):**

1. **Personalized novel→comic** — "I finished 《天道图书馆》, make me a comic of the chapters I loved" — no tool does this. All existing tools (Anifusion, Dashtoon, AI Comic Factory) require manual prompting of individual panels.

2. **Personalized novel→short video** — "I just read 《红楼梦》chapters 1-20, give me a 5-min cinematic video summary in my style" — no tool. Wavel.ai/Medeo do generic book trailers, not reading-list-aware.

3. **Auto-吐槽 pipeline from novel text** — "I finished 《三国演义》, generate a 吐槽解说 script in the style of 特级盘点师, tuned to the moments I highlighted" — no tool. Human creators like 特级盘点师 write these scripts manually. An LLM pipeline (novel chapters + reader highlights → 吐槽 script → TTS + AI image) would be novel.

**What IS crowded:**
- Generic text→panel comic generators
- Industrial 网文→漫剧 B2B production pipelines
- Manual 吐槽 channels on Bilibili (human-written, no AI pipeline)
- Novel translation AI tools (language-focused, not visual)

---

## Sources
- Bilibili API via opencli
- Reddit search via opencli
- GitHub via gh CLI
- WebSearch results (WebFetch budget reached mid-session)
- Industry reports: DataEye Q1-2026, 大洋网 2026-02, 澎湃新闻 2025
