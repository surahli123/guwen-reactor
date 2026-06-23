# Guwen Reactor — Capstone Writeup

> **Status:** draft — fill as the build lands.
> Target: ≤ 2,500 words. Track: Agents for Good.
> Outline lives in `specs/writeup_outline.md`. Follow section word budgets there.

---

## Problem

[PLACEHOLDER — expand from `specs/product_spec.md §1–2`]

Educators need classroom-trustworthy adaptations of unfamiliar classical texts.
They are accountable for accuracy, so they need visible source grounding,
hallucination detection, and a human approval gate before using AI-generated
material with learners.

Primary user: English-speaking educators, teaching assistants, and curriculum builders.
Learners are the beneficiaries, not the primary build user.

---

## Solution

[PLACEHOLDER — expand from `specs/product_spec.md §3–4`]

Given a public-domain Classical Chinese scene, Guwen Reactor produces: English story
card, cultural decoder, teaching pack, 8 text storyboard panels, source-grounded
evaluation report, human approval diff, cached HTML run canvas, and local export bundle.

Primary eval claim (D3=C locked): *source-grounded PLOT fidelity for classroom-safe
adaptation.* Interpretation is advisory, never export-blocking.

---

## Architecture

[PLACEHOLDER — fill after `docs/architecture.md` is written; include diagram]

```
Original Chinese source
→ source / copyright guard
→ canon gold / source memory
→ structured claim generation (assertion_type + hedging fields)
→ structural audit gate (deterministic, rule-order per Contract B)
→ safety gate
→ human approval
→ manifest-bound cached export
```

Key contracts (locked):
- D1: generator emits structured claims; gate audits structure (no keyword heuristics).
- D3=C: plot hard-gated; interpretation advisory only.
- Contract H: `sanitize(claim_text)` on GENERATED content before `build_judge_prompt`.
- Contract G: specificity test — valid hedged interpretation must NOT block.

---

## The Eval Story

[PLACEHOLDER — fill after `docs/measured_results.md` is written with actual numbers]

Drift suite (D1–D6):
- D1 obvious contradiction → BLOCKED
- D2 non-forbidden unsupported detail → BLOCKED
- D3 subtle invented motive → BLOCKED (structural rule: assertion_type=motive, hedging=asserted)
- D4 coverage omission → BLOCKED (required_beat_coverage < 0.85)
- D5 citation spoof → BLOCKED (structural audit ignores self-reported ids as primary evidence)
- D6 judge-prompt injection → BLOCKED (PROMPT_INJECTION_ATTEMPT, first gate step)

> ILLUSTRATIVE — replace with measured run output:
> Clean run: 42/45 supported factual claims, 3/3 required beats covered, 0 critical labels.
> Baseline B1 fail rate: ~35% (pre-registered band: 30–40%).

---

## The Build Journey

[PLACEHOLDER — fill from `docs/build_log.md` daily entries]

High-level arc:
- v1 adversarial review: scope cut, eval-first order enforced, cached demo made primary.
- v3 deep review: keyword gate → structural audit; LLM judge demoted to advisory;
  injection now gates export; fact-id validity + generated-content sanitization added.
- Tooling: Antigravity (primary IDE), Claude Code + Codex (implementation/review),
  pytest (gate). Built spec-first; no MCP/ADK before pure-Python eval core was green.

[PLACEHOLDER — add specific day-by-day moments and surprises from build_log.md]

---

## Links

- GitHub repo: [PLACEHOLDER]
- Cached demo (no API key required): [PLACEHOLDER — `docs/demo/index.html` via GitHub Pages]
- Video: [PLACEHOLDER]
- Cover image: `docs/cover_image.png`
