# Independent denotation-check notes (Contract D / D2)

Tracks how each scene's canon gold was checked for **denotation fidelity** (English fact = literal
denotation of its anchored Chinese chunk; zero motive/evaluation). Method per
`docs/plan/gold-cross-validation-protocol.md`; guardrails per `docs/plan/annotation-guardrails.md`.

**Disclosure (current):** gold is **single-annotator** (AI Reader-A draft + machine audit + owner check).
**No inter-annotator agreement (IAA) yet** — second human reader pending (non-blocking, per protocol).
This limitation is also disclosed in `docs/measured_results.md` when results are reported.

---

## G01 — 管寧割席 (Shishuo Xinyu · De Xing #11)

**Checks run:**
1. **AI Reader-A draft** — transcribed from `Build_Ready_Spec_v3` §3.5 (already chunk-anchored).
2. **Machine adversarial audit** — 3 blind lenses (denotation / anchoring+segmentation / completeness+forbidden)
   + merge, run `2026-06-24` (workflow `w7vzvp4p4`). Verdict: `needs_fix_before_human_check` → fixed below.
3. **Human denotation check** — ⏳ PENDING (owner, as independent checker).
4. **Second-reader cross-validation** — ⏳ PENDING (fills `agreement_pct`).

**Machine-audit fixes applied (before human check):**
| Change | Type | Reason |
|---|---|---|
| F03 `treats the gold like debris` → `keeps hoeing and handles the gold no differently from tile or stone` | BLOCKING | "treats like" = disposition frame → risked smuggling evaluation; 揮鋤與瓦石不異 is pure action (guardrail A.2). All 3 lenses flagged. |
| forbidden_claims 4 → 7 (added C02 motive traps + editorial-evaluation trap) | BLOCKING | C02 (华歆慕荣) had no forbidden anchor → drift suite (§C) had nothing to block there; gate calibration was half-empty. |
| F05 `prestigious carriage` → `someone in an official's carriage` | advisory (applied) | "prestigious" = evaluative gloss + narrowed referent 人→车; restored person as referent. |
| F10 added: `sitting on the same mat while reading` [C02] | advisory (applied) | 同席 was unanchored yet is the literal antecedent of B03 割席; closes the denotation chain. |
| F04 "picks up AND throws away co-present to credit" | DEFERRED → Phase 4a eval_plan | a scoring contract, not a gold edit. |

**Per-fact machine verdict (post-fix):** F01 clean · F02 clean · F03 fixed→clean · F04 clean (one-fact, anti-`keeps`) ·
F05 fixed→clean · F06 clean · F07 clean (C02 motive now fenced by forbidden_claims) · F08 clean · F09 clean (speech-act, A.1) · F10 clean.
Confirmed-good (do not regress): F09 speech-act framing; subject-locking on F03/F06/F07/F08; all anchors in-chunk; beats no dangling refs.

**Human check result:** _(to fill: for each F0x, does the English say only what the anchored Chinese chunk literally says? note any disagreement.)_

---

## G02 — 詠雪 (Shishuo Xinyu · Yan Yu)

**Checks run:** AI Reader-A draft (authored from 原文, not spec) → 3-lens machine audit (workflow `w3hx36mm0`,
verdict `needs_fix_before_human_check`) → ⏳ human denotation check PENDING.

**Machine-audit fixes applied:**
| Change | Type | Reason |
|---|---|---|
| F02: removed parenthetical "(his sons, daughters, the children of the household)" | BLOCKING | member-disambiguation inference + **factually wrong** (answerers are 兄子/兄女, not Xie's own children). |
| F04/F07: dropped the "(Grand Tutor Xie)" anaphora gloss | advisory (applied) | keep atomic_fact text to the chunk's denotation; 公 = the Lord (identity set in F01). |
| F08 split → F08 (daughter of Wuyi) + F09 (wife of Wang Ningzhi) | advisory (applied) | atomicity: 同席-aside bundled two independent identity facts. |
| forbidden_claims 8 → 10 (added 亲生子女 trap + 差可拟 narrator-misread) | BLOCKING + advisory | gives the drift suite a target for the member-disambiguation contamination. |

**Held-good (do not regress):** 稱謂 discipline (本名 谢安/谢朗/谢道韫 only in forbidden, never in facts);
切分 = speaker-turn; F07 公大笑樂 recorded with no cause/addressee/preference.
**Human check result:** _(to fill)_

## G03 — 道旁苦李 (Shishuo Xinyu · Ya Liang) — the highest-risk scene (inference trap)

**Checks run:** AI Reader-A draft → 3-lens machine audit (workflow `w3hx36mm0`,
verdict `needs_fix_before_human_check`) → ⏳ human denotation check PENDING.

**Machine-audit fixes applied:**
| Change | Type | Reason |
|---|---|---|
| F03/F04: merged the subjectless 看 into F03 (open subject), dropped the duplicate tree description | BLOCKING | draft backfilled C04's 諸兒 as subject of C03's subjectless 看 (A.5 subject-locking) + double-counted the tree (S). |
| F06: trimmed "(about why he did not move)" → "Someone asked Wang Rong." | BLOCKING | 人問之 only asserts a question occurred; its content is unstated (tie-break: uncertain → out of literal gold). |
| F08: position-locked "Afterward the plums were picked (by an unspecified party)." | advisory (applied) | distinguishes the 2nd 取之 from F04's 取; subject kept open (not Wang Rong, who 不動). |

**Held-good (do not regress):** 「此必苦李」kept as a **speech-act** (F07: "Wang Rong answered that …"),
NOT "the plums are bitter"; 「信然」(F09) = "outcome matched his claim", not over-extended to causation/tasting;
2nd 取之 subject open; 折枝 = weighed-down (not snapped). 10 forbidden_claims target every inference trap.
**Human check result:** _(to fill)_
