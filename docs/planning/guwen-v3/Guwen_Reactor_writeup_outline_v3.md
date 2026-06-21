# Guwen Reactor — Kaggle Writeup Outline v3

Target: <= 2,500 words.
Track: Agents for Good.

## 1. Title and one-line pitch — 120 words
**Guwen Reactor: A Source-Grounded Agentic Engine for Classroom-Trustworthy Cross-Cultural Story Adaptation**

One-line pitch: turns public-domain Classical Chinese scenes into educator-friendly English story cards, cultural decoders, teaching packs, and storyboards, while measuring fidelity and blocking hallucinated claims before export.

## 2. Problem and users — 250 words
Primary user: educators. Learners are beneficiaries.
Problem: cross-cultural teaching needs accuracy, context, and trust, not only translation.

## 3. Why agents are necessary — 300 words
Explain why one-shot ChatGPT is insufficient: no source guard, no canon gold, no claim-vs-source eval, no safety gate, no approval artifact.

## 4. Architecture — 350 words
Pure-Python core first.
MCP wrapper.
Skills.
Optional ADK Builder/Critic boundary.
Cached HTML run canvas as primary judged link.

## 5. Evaluation harness — 550 words
This is the centerpiece.
- Unsupported critical claims count gate.
- Aggregated precision with denominator.
- Calibrated contradiction judge or advisory fallback.
- Subtle motivation drift.
- Citation spoof.
- Required beat coverage.
- Interpretive rubric.
- Safety pass.
- Baseline failure-mode breakdown.

## 6. Security — 250 words
Source/judge prompt injection, fenced untrusted data, Unicode normalization, path confinement, DoW cap, AIGC manifest binding.

## 7. Demo — 250 words
Two-beat video: recognition scene + trust proof.
Show value first, then drift-blocking climax.

## 8. Project journey — 250 words
Mention C1-C10 adversarial review and v3 deep review: scope was cut, eval moved first, cached demo made primary, educator wedge clarified.

## 9. Course concepts — 200 words
MCP, skills, security, deployability, Antigravity, optional ADK.

## 10. Limitations and next work — 180 words
Gold set small, human labels limited, no image generation, no commercial creator workflow in V1.

## 11. Links — 50 words
GitHub repo, cached demo, video, cover image.
