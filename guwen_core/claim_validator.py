"""
guwen_core/claim_validator.py — Task 4a.1: Claim structure validator (D1 / fix F1, C3).

SCOPE: structure check + sanitize claim_text (Contract H) + flag invalid fact-ids (fix C3).
NOT IN SCOPE: audit labels, forbidden-match, coverage, beat-alignment — those are Task 4a.2+.

Why this file exists:
  D1 replaced free-form claim extraction with constrained StructuredClaim generation.
  This validator is the first-pass gate: it confirms every claim is schema-valid (Pydantic
  already enforced this at parse time), sanitizes claim_text to strip invisible payloads
  before any downstream judgment (Contract H), and flags any source_fact_ids that are not
  present in the scene's atomic_facts (fix C3 — the INVALID_FACT_ID blocking label is
  assigned by the structural audit in Task 4a.2, not here).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from guwen_core.schema_validator import CanonScene, StructuredClaim
from guwen_core.source_sanitizer import sanitize


@dataclass
class ValidatedClaims:
    """Output of validate_claims; consumed by evaluate_claims (Task 4a.2)."""
    claims: list[StructuredClaim]
    # claim_ids whose source_fact_ids contain at least one id absent from the scene.
    # The audit (4a.2) will assign INVALID_FACT_ID label; we surface the set here so
    # the audit does not need to re-derive it.
    invalid_fact_id_claim_ids: list[str] = field(default_factory=list)


def validate_claims(
    claims: list[StructuredClaim],
    scene: CanonScene,
) -> ValidatedClaims:
    """
    Validate and sanitize a list of StructuredClaims against a CanonScene.

    Steps per claim (in order):
      1. Sanitize claim_text — NFKC + zero-width strip (Contract H / fix F5).
         This must happen before any downstream judge or audit sees the text.
      2. Flag any source_fact_ids not present in scene.atomic_facts (fix C3).
         A single unknown id is enough to flag the whole claim.

    No keyword matching, no label assignment, no forbidden-claim checking here —
    those are Contract B (Task 4a.2 / structural_audit.py).
    """
    # Build the valid id set once — O(1) lookups below
    valid_ids: set[str] = {f.id for f in scene.atomic_facts}

    out: list[StructuredClaim] = []
    invalid: list[str] = []

    for claim in claims:
        # Contract H: sanitize before any downstream use
        clean_text = sanitize(claim.claim_text).clean_text
        claim = claim.model_copy(update={"claim_text": clean_text})

        # fix C3: flag claims that cite ids unknown to this scene
        if any(fid not in valid_ids for fid in claim.source_fact_ids):
            invalid.append(claim.claim_id)

        out.append(claim)

    return ValidatedClaims(claims=out, invalid_fact_id_claim_ids=invalid)
