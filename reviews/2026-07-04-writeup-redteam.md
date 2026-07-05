# Red-Team Review — Kaggle capstone writeup (`docs/capstone_writeup.md`)

VERIFIED_AGAINST: fix/g01-perception-claim @ HEAD · 2026-07-04 · claims re-verified vs repo

**Artifact calibration.** Kaggle submission writeup = persuasion (primary) × claim-integrity (critical secondary — the whole thesis is claim-honesty). Not scored for statistical rigor; every factual claim held to account.

## Verdict
Strong, thorough draft (~1,850 words). Content, structure, and honesty are submission-grade. Only two classes of finding, both now handled: (1) a verb-consistency defect vs the finalized video, (2) unfilled links.

## Findings

**[HIGH — FIXED] "publish" vocabulary contradicts the finalized video + the engine's actual gate.**
The video was standardized this cycle to *hand over* (hero) / *export* (mechanism); the writeup still said "publish/published" in 4 places (lines 6, 31, 62, 129). On a claim-precision-themed submission, the writeup and video must use the same verb for the same promise, and the engine's gate is `export_bundle`, not "publish". → Fixed: line 6 hero → "hand over" (matches video S1); lines 31/62/129 → "export" (matches engine + video S2/S3/S6). 0 "publish" remain.

**[HIGH — PENDING owner] Four unfilled placeholders.**
- GitHub repo (line 212) → **FIXED**: https://github.com/surahli123/guwen-reactor (verified PUBLIC via gh).
- Demo (line 213) → needs a live URL. Recommend enabling GitHub Pages (docs/ source) → `surahli123.github.io/guwen-reactor/demo/`, or htmlpreview fallback. Owner decision.
- Video (line 214) → YouTube link, blocked on owner's upload of `guwen-draft.mp4`.
- Cover (lines 9, 215) → `cover-kaggle.png` exists in the video repo; needs to be copied into this repo to embed, or uploaded via the Kaggle platform. Owner decision.

## Claims re-verified (accurate — no change)
- "131 passing tests, part of a 136-test suite (pytest evals/)": `pytest evals/` collects **136** ✓; 131 = engine subset (−5 MCP wrapper), consistent with README + video.
- In-browser checker = "small subset… same facts, same forbidden list, simplified matching" (lines 126-128, 179-181): matches `docs/demo/index.html` (`gateCheck` = 2 rules over verbatim canon_gold). Honestly disclosed — stronger than the video's audio phrasing.
- G01 perception fix, honest tiering (3/10), MCP metadata-only, concept-coverage honesty (lines 187-191): all consistent with repo + video.

## Remaining to finalize (owner)
1. Upload `guwen-draft.mp4` to YouTube → paste link (line 214).
2. Decide demo hosting (GitHub Pages recommended — can enable now) → line 213.
3. Decide cover hosting (copy into repo + embed, or Kaggle-platform upload) → lines 9, 215.
