"""Task 4a.2 — the deterministic structural-audit gate (Contract B). THE heart.

Labels are derived ONLY from the declared structural fields (assertion_type, hedging,
source_fact_ids) + injection detection + forbidden-claim normalization. There is NO
keyword/semantic matching (D1 / fix F1 — all `_supported_by_fact` heuristics removed).

Rule order is Contract B, FIRST MATCH WINS:
  B.1 injection -> PROMPT_INJECTION_ATTEMPT
  B.2 invalid fact-id (cited id absent from gold) -> INVALID_FACT_ID
  B.3 forbidden delta (normalized match) -> CONTRADICTED
  B.4 unhedged motive/emotion -> UNSUPPORTED_MOTIVATION
  B.5 unsupported asserted event -> UNSUPPORTED_DETAIL (critical). STRENGTHENED per
      review #4 / decisions-locked rule 5: an action/visual claim is unsupported when its
      source_fact_ids are EMPTY *or* a cited id does not belong to the claim's DECLARED
      beat (cross-beat / valid-but-irrelevant citation). Such an id never boosts coverage.
  B.6 hedged interpretation / else -> VALID_HEDGED_INTERPRETATION / SUPPORTED (no block)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from guwen_core.claim_validator import ValidatedClaims
from guwen_core.schema_validator import (
    StructuredClaim, ClaimLabel, CanonScene, AssertionType, Hedging,
)
from guwen_core.safe_prompt import detect_injection

_PLOT = (AssertionType.ACTION, AssertionType.VISUAL)
_SOFT = (AssertionType.INTERPRETATION, AssertionType.MOTIVE, AssertionType.EMOTION)


def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", "".join(c for c in s.casefold() if c.isalnum() or c.isspace())).strip()


@dataclass
class AuditResult:
    labeled_claims: list[StructuredClaim]
    counts: dict = field(default_factory=dict)
    supported_fact_ids: set = field(default_factory=set)
    factual_precision: str = "0/0"


def evaluate_claims(validated: ValidatedClaims, scene: CanonScene) -> AuditResult:
    forbidden = {_normalize(f) for f in scene.forbidden_claims}
    invalid_ids = set(validated.invalid_fact_id_claim_ids)
    beat_facts = {b.beat_id: set(b.fact_ids) for b in scene.required_beats}
    all_beat_facts = set().union(*beat_facts.values()) if beat_facts else set()

    def aligned_ids(c: StructuredClaim) -> set:
        """The cited ids that actually belong to the claim's declared beat (empty if no/unknown beat)."""
        return set(c.source_fact_ids) & beat_facts.get(c.beat_id, set())

    def unsupported_event(c: StructuredClaim) -> bool:
        # B.5 strengthened: empty ids, OR any cited id outside the declared beat (review #4).
        ids = set(c.source_fact_ids)
        if not ids:                                                     # (a) cites nothing
            return True
        if c.beat_id is not None and not ids <= beat_facts.get(c.beat_id, set()):
            return True                                                 # (b) cites outside its declared beat
        if c.beat_id is None and (ids & all_beat_facts):
            return True                                                 # (c) beat-less but cites a beat-owned fact (eval-core review)
        return False

    counts = {"unsupported_critical_claims": 0, "contradicted_claims": 0,
              "unsupported_motivation_claims": 0, "invalid_fact_id_claims": 0,
              "prompt_injection_attempts": 0}
    labeled: list[StructuredClaim] = []
    supported_fact_ids: set = set()
    supported = total_factual = 0

    for c in validated.claims:
        text = c.claim_text.strip()
        if detect_injection(text):                                      # B.1
            label, critical = ClaimLabel.PROMPT_INJECTION_ATTEMPT, True
            counts["prompt_injection_attempts"] += 1
        elif c.claim_id in invalid_ids:                                 # B.2 (fix C3)
            label, critical = ClaimLabel.INVALID_FACT_ID, True
            counts["invalid_fact_id_claims"] += 1
        elif _normalize(text) in forbidden:                             # B.3 (fix C5)
            label, critical = ClaimLabel.CONTRADICTED, True
            counts["contradicted_claims"] += 1
        elif c.assertion_type in (AssertionType.MOTIVE, AssertionType.EMOTION) \
                and c.hedging == Hedging.ASSERTED:                      # B.4 subtle drift
            label, critical = ClaimLabel.UNSUPPORTED_MOTIVATION, True
            counts["unsupported_motivation_claims"] += 1
        elif c.assertion_type in _PLOT and unsupported_event(c):        # B.5 strengthened (review #4)
            label, critical = ClaimLabel.UNSUPPORTED_DETAIL, True       # asserted new/misattributed event = critical
        elif c.hedging == Hedging.HEDGED and c.assertion_type in _SOFT:  # B.6 hedged-valid
            label, critical = ClaimLabel.VALID_HEDGED_INTERPRETATION, False
        else:                                                           # B.6 supported
            label, critical = ClaimLabel.SUPPORTED, False
            if c.assertion_type in _PLOT:                               # only PLOT claims cover plot beats (review MINOR #1)
                supported_fact_ids.update(aligned_ids(c))               # beat-aligned ids only
            supported += 1

        if critical:
            counts["unsupported_critical_claims"] += 1
        if label in (ClaimLabel.SUPPORTED, ClaimLabel.UNSUPPORTED_DETAIL, ClaimLabel.CONTRADICTED,
                     ClaimLabel.UNSUPPORTED_MOTIVATION, ClaimLabel.INVALID_FACT_ID):
            total_factual += 1
        labeled.append(c.model_copy(update={"label": label}))

    return AuditResult(labeled, counts, supported_fact_ids, f"{supported}/{total_factual}")
