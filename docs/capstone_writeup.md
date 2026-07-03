# Guwen Reactor — A Source-Grounded Engine for Classroom-Trustworthy Cultural Adaptation

*Kaggle "AI Agents: Intensive — Vibe Coding" capstone · Track: Agents for Good*

**One line:** Guwen Reactor turns public-domain Classical Chinese scenes into English
story cards for educators, then refuses to publish any sentence it cannot trace back
to a committed fact in the original Chinese source.

> [PLACEHOLDER: cover image]

---

## The problem: trust is the product, not translation

An English-speaking teacher wants to bring 《世說新語》 (*Shishuo Xinyu*, a 5th-century
collection of anecdotes) into a classroom. Machine translation is not the hard part.
The hard part is that the teacher is *accountable*: they stake their classroom
reputation on every sentence they hand a student. A single fabricated motive — "Guan
Ning cut the mat because he envied his friend's ambition" — is not a small error. It is
the teacher, unknowingly, teaching something the source never said.

General chat models cannot give that teacher what they need, because a fluent paragraph
carries no evidence. There is no denominator, no citation to the original, and no place
where a hallucination is stopped before it reaches a learner. Our user is the educator;
the learner is the beneficiary who, unable to read the source, cannot personally check
fidelity. So the trust has to be built into the tool.

Guwen Reactor's promise is narrow on purpose: **source-grounded plot fidelity for a
classroom-safe adaptation.** We do not claim the adaptation is interpretively
"correct" — that stays advisory. We claim, and can prove, that every plot sentence we
publish is grounded in the original Chinese.

---

## The deterministic gate: ordinary code, not an AI judge

The core of the project is a faithfulness gate written in plain Python. It is not a
model grading a model. It is a set of deterministic rules — the engine itself backed
by **131 passing tests**, part of a **136-test** suite (`pytest evals/`, verified
2026-07-02) — that decides whether a run may be exported.

Every English sentence is emitted as a *structured claim* — not free prose — carrying
its own `assertion_type` (action, motive, emotion, interpretation, visual), a `hedging`
flag, and the `source_fact_ids` it says it rests on. The gate audits that structure,
applying rules in a fixed order where the first match wins (`structural_audit.py`):

1. **Injection** in the claim text → blocked.
2. **Invalid fact id** (a citation to a fact not in the gold set) → blocked.
3. **Forbidden delta** — the claim matches a documented misreading, or contradicts a
   covered fact → blocked.
4. **Unhedged motive or emotion** — an asserted inner state with no hedge → blocked.
   This is the subtle-drift catch, and it is structural: no keyword guessing.
5. **Unsupported asserted event** — an action or visual claim whose cited facts do not
   structurally *cover* it (empty, cross-beat, or a beat-less claim citing a
   beat-owned fact) → blocked.

Coverage is computed only from *validated* fact ids: a required beat counts as covered
only when all of its facts are actually supported, never from self-reported citations.
The export gate then requires `unsupported_critical_claims == 0`, coverage ≥ 0.85,
plus source-policy, safety, and human approval.

The chain a judge can walk is **claim → fact → 古文 chunk**: every published sentence
points to an `atomic_fact`, and every fact is anchored to a specific phrase in the
committed Chinese text. Running the engine today on the demo scene 管寧割席 (Guan Ning
Cuts the Mat) returns `factual_precision 9/9`, `coverage 3/3`, zero unsupported,
contradicted, or motivation claims, and `export_status: READY_FOR_APPROVAL`. The same
scene with one planted fabrication returns `BLOCKED`. Those are engine outputs, not
prose.

---

## Two independent gates — and the drift they caught in opposite directions

A deterministic engine can only check what a human first anchored. So content passes
through **two** gates: the engine, and an independent human review where the author and
the reviewer are deliberately separate contexts. The strongest evidence that this
separation earns its keep is that, across two scenes, review caught real drift running
in **opposite directions** — exactly the two failure modes a single author cannot
reliably self-catch.

**G01 管寧割席 — added, unsupported.** The author's own faithfulness self-check had
already pulled back several embellishments. An independent critic still caught one the
author had missed: the draft line *"Their blades turn up a glint of gold."* The source
fact F02 is 見地有片金 — *perception*: they **see** gold in the ground. "Blades turn
up" silently promotes the hoe to the agent that **dug the gold up** — a new action
asserted as fact. That is precisely the perception-to-action smuggle the gate exists to
stop, arriving through prose the engine never sees. Fixed to a perception frame ("a
piece of gold catches their eye"); reviewed → PASS.

**G02 詠雪 — deleted, supported.** Here the drift ran the other way. Trying to avoid
having the narrator *endorse* a comparison, the author over-neutralized the elder
brother's daughter's line to a bland "offers hers." But the comparative judgment 未若
柳絮因風起 — "**not as good as** willow catkins on the wind" — is something the character
literally *says*. Flattening it deleted supported content and dulled the anecdote's whole
point. The independent reviewer (Codex, Round 1) failed the draft; the fix restored the
comparison inside the quotation, attributed to the speaker, narrator still neutral;
Round 2 passed.

One review caught an **addition of the unsupported**; the other caught a **deletion of
the supported**. An author checking their own work tends to guard one direction and miss
the other. That is the empirical case for author ≠ reviewer, and it is on the record in
`content-retelling.md` and `content-retelling-g02.md` (under
`designs/visible-faithfulness-g01/`), not asserted in the abstract.

---

## A trust UX judges can falsify

Trust claims are cheap; the demo is built so a skeptic does not have to take our word.
The primary judged artifact is a single self-contained HTML page (`docs/demo/index.html`,
zero external requests, LXGW font embedded) styled as a 《山河卷》 handscroll.

Its signature move is the **gate you flip yourself**. A prepared fabricated sentence
sits in the scene; you throw the gate, and a rule subset of the real engine runs
**live in your browser** — checking the fabrication against the ten committed facts and
the forbidden list, then striking it through in vermilion with the reason. The animation
is honest: it computes the verdict first, then reveals the ledger row by row. There is
no fake "scanning…" progress bar.

Three prepared fabrications rotate, and one is deliberately the hard case: *"Guan Ning
cuts the mat because he envies Hua Xin's ambition."* Every factual event in it is true —
it cites real facts that all pass — and it is **still** blocked, by the unhedged-motive
rule. That single case demonstrates the engine is not keyword matching: it caught an
invented *reason* wrapped around true *events*.

The honest boundary is stated on the page itself: the in-browser checker is a small
subset of the full engine — same facts, same forbidden list, simplified matching, three
prepared cases — while the full suite runs in the build pipeline and every verdict shown
for the *published* text is a committed record, not a live generation. (The method page
cites the engine's 131 tests; the full suite is 136 including 5 MCP-server wrapper tests.)

---

## Honest tiering: three lamps of ten

The map shows ten scenes. **Three lamps are lit; seven are dark — and that is the
thesis, not a shortfall.** A lamp lights only after a scene clears *both* gates: engine
`READY_FOR_APPROVAL` and independent human review PASS. Today G01 管寧割席, G02 詠雪, and
G03 道旁苦李 are lit, each at engine `9/9` supported claims with full beat coverage.

The dark seven are not hidden or faked to look finished. Clicking one opens an honest
card that says, plainly, what "not yet verified" looks like. In a field full of tools
that present everything as equally trustworthy, showing the unverified majority *as
unverified* is the point. The lamp is binary by design — lit or unlit, never a
confidence score — because a graded trust meter invites exactly the over-trust we are
trying to prevent.

---

## Architecture and how it runs

The system is eval-first: a pure-Python core was made green before anything was wrapped
around it.

- **Faithfulness core** — structured-claim schema, structural-audit gate, coverage,
  safety deny-list, regeneration loop (fail-closed at three attempts), approval and
  manifest-bound export. A single canonical gate definition lives in
  `specs/eval_plan.yaml`; nothing duplicates it.
- **MCP server** (`app/mcp_server.py`) — a local stdio server exposing three offline
  tools: `run_eval_suite`, `check_source_policy`, `get_source`. Source access is
  metadata-only; export trust comes from the gate, never model self-report.
- **Security** — NFKC + zero-width normalization on both ingested source *and* generated
  content before judging; a fenced judge prompt; an injection detector that gates
  export; path confinement; a denial-of-wallet cap; and an AIGC label bound by SHA-256
  on every exported artifact.
- **Deployability** — the cached offline HTML demo needs no API key in the judged path,
  and the repo ingests **only public-domain original Chinese**, generating its own
  English; no copyrighted translation is stored or reproduced.

The handoff discipline throughout is file-reference, not blobs: paths plus hashes.

---

## Limitations, stated plainly

- **Single-annotator gold.** The fact sets were authored and adversarially self-audited
  by one annotator. An independent Chinese-literate denotation check is disclosed as
  pending; inter-annotator agreement is future work, not a measured number.
- **The in-browser engine is a rule subset.** Two of the engine's rules, faithfully
  reproduced, run in the page; the full rule set and the engine's 131 tests run in the
  build pipeline. This is stated on the demo's method page.
- **The LLM contradiction judge is advisory only.** No calibration study was feasible in
  the timebox, so it never gates export — the deterministic structural audit is the hard
  gate.
- **Interpretation is advisory, not gated.** We defend plot fidelity, not that a
  reading is "correct."
- **Concept coverage is honest about what shipped.** MCP, security, evaluation, and
  deployability are built and tested. Agent-skills packaging and an ADK multi-agent
  builder/critic split were planned but are **not** in the repo today; the author≠reviewer
  separation was realized with independent AI/human review during the build, not an
  in-repo agent.

---

## Future work

The tier-1 promotion pipeline that lit G01–G03 is defined and repeatable, and the
runway is already laid. Seven more scenes (G04–G10) are source-committed and were
verified character-by-character against the 《四部叢刊初編》 base edition of 《世說新語》 on
ctext.org (two variant characters aligned, 捨→舍 and 儁→俊; punctuation differences
accepted as editorial convention). They are deliberately kept **out** of the engine's
gold set until they clear both gates, so an unverified scene can never quietly earn a
lamp. Promoting each is the same loop: author the grounded retelling, run the engine to
`READY_FOR_APPROVAL`, pass independent review, light the lamp. Beyond that: an
independent denotation check to retire the single-annotator caveat, an IAA study, and V2
verticals — museums, language-learning platforms, diaspora education.

---

## Links

- GitHub repository: [PLACEHOLDER]
- Cached demo (no API key required): [PLACEHOLDER — `docs/demo/index.html` via GitHub Pages]
- Video (≤5 min): [PLACEHOLDER]
- Cover image: [PLACEHOLDER]
