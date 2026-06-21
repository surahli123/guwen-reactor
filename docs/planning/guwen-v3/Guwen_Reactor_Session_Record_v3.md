# Guwen Reactor — Session Record v3

## Context

The project is for Kaggle's AI Agents Intensive / Vibe Coding capstone. The selected track remains Agents for Good.

## Project evolution

1. Original idea: turn read Classical Chinese novels into comics, short videos, or reaction/roast videos.
2. First narrowing: public-domain Classical Chinese → English-friendly explanation, cultural decoder, storyboard, and evaluation.
3. v2 adversarial review: scope cut to walking skeleton, original-Chinese-only copyright plan, planted-drift eval climax, cached output artifacts.
4. v3 deep review: sharpened the evaluation harness and product wedge.

## v3 product decision

Primary user changed from generic learner/creator to **educator**. Learners remain beneficiaries.

Reason: the source-grounded apparatus protects the person accountable for accuracy. The educator can perceive and value fidelity, while a learner who cannot read Chinese mostly sees output quality.

## v3 technical decisions

- Build pure-Python eval core first.
- Keep local stdio MCP server as non-cuttable.
- Keep skills, but test triggers and cut from 5 to 3 if needed.
- ADK Builder/Critic wrapper remains targeted but not allowed to block the core.
- Cached static HTML is the primary judged project link.
- Live Streamlit is optional.
- No image generation in V1.

## v3 evaluation decisions

- Do not trust BuilderAgent self-reported source fact IDs.
- Extract claims from generated prose.
- Judge claim-vs-source entailment.
- Calibrate contradiction judge before it can gate export.
- If not calibrated, demote the LLM judge to advisory.
- Keep `unsupported_critical_claims == 0` as headline hard gate.
- Report precision with denominators across 3–5 scenes.
- Add interpretive rubric for `why_it_matters` and `modern_analogy`.
- Add subtle non-forbidden drift, citation spoof, omission drift, and judge-prompt injection tests.

## v3 demo decision

Use a two-beat video:

1. Recognition/value beat: show an iconic scene preview if ready.
2. Trust beat: use Guan Ning Cuts the Mat for the measured eval proof.

If the iconic preview risks scope, cut it and use Guan Ning only.

## Deliverables generated in this update

- `Guwen_Reactor_Build_Ready_Spec_v3.md`
- `Guwen_Reactor_threat_model.md`
- `Guwen_Reactor_eval_plan_v3.yaml`
- `Guwen_Reactor_behavior.feature`
- `Guwen_Reactor_writeup_outline_v3.md`
- `Guwen_Reactor_rater_label_sheet_v3.md`
- `Guwen_Reactor_AGENTS_v3.md`
- `Guwen_Reactor_v3_File_Manifest.md`
- `Guwen_Reactor_v3_Spec_and_Related_Files.zip`
