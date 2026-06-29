"""
evals/test_claim_validator.py — TDD tests for guwen_core/claim_validator.py (Task 4a.1).

Coverage:
  (a) Clean runs/demo_clean fixture → zero invalid fact-ids
  (b) Claim citing bogus id (F99) → flagged in invalid_fact_id_claim_ids  [from plan Step 1]
  (c) claim_text containing zero-width char → stripped (sanitized) before output  [Contract H]
  (d) Valid fact-id (F08 in a scene that defines F08) → NOT flagged  [from plan Step 1]
"""
from __future__ import annotations

from pathlib import Path

import yaml

from guwen_core.claim_validator import validate_claims
from guwen_core.schema_validator import (
    AssertionType,
    CanonScene,
    Hedging,
    StructuredClaim,
    load_yaml_as,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REPO = Path(__file__).parent.parent


def _minimal_scene() -> CanonScene:
    """Small inline scene used by unit tests — defines only F08 in beat B03."""
    return CanonScene.model_validate({
        "scene_id": "G01",
        "title_en": "x",
        "title_zh": "管寧割席",
        "source_id": "s",
        "source_chunks": [{"chunk_id": "C03", "text_zh": "寧割席分坐"}],
        "atomic_facts": [
            {"id": "F08", "text": "Guan Ning cuts the mat.", "source_chunk_ids": ["C03"]}
        ],
        "required_beats": [{"beat_id": "B03", "fact_ids": ["F08"], "description": "mat"}],
        "forbidden_claims": ["Hua Xin keeps the gold."],
    })


# ---------------------------------------------------------------------------
# Test (b): bogus fact-id is flagged (fix C3)
# ---------------------------------------------------------------------------

def test_flags_unknown_fact_id():
    """A claim citing F99 (not in scene) must appear in invalid_fact_id_claim_ids."""
    claims = [
        StructuredClaim(
            claim_id="c1",
            beat_id="B03",
            claim_text="cuts the mat",
            source_fact_ids=["F99"],
            assertion_type=AssertionType.ACTION,
            hedging=Hedging.ASSERTED,
            artifact_path="p",
        )
    ]
    result = validate_claims(claims, _minimal_scene())
    assert "c1" in result.invalid_fact_id_claim_ids


# ---------------------------------------------------------------------------
# Test (d): valid fact-id is NOT flagged
# ---------------------------------------------------------------------------

def test_valid_fact_id_not_flagged():
    """A claim citing F08 (defined in scene) must NOT be in invalid_fact_id_claim_ids."""
    claims = [
        StructuredClaim(
            claim_id="c2",
            beat_id="B03",
            claim_text="cuts the mat",
            source_fact_ids=["F08"],
            assertion_type=AssertionType.ACTION,
            hedging=Hedging.ASSERTED,
            artifact_path="p",
        )
    ]
    result = validate_claims(claims, _minimal_scene())
    assert result.invalid_fact_id_claim_ids == []


# ---------------------------------------------------------------------------
# Test: mixed valid + invalid ids — only the bad one is flagged
# ---------------------------------------------------------------------------

def test_mixed_ids_flags_only_invalid():
    """A claim citing [F08, F99] is flagged (F99 is unknown) but F08 alone is fine."""
    bad_claim = StructuredClaim(
        claim_id="bad",
        beat_id="B03",
        claim_text="cuts the mat somehow",
        source_fact_ids=["F08", "F99"],
        assertion_type=AssertionType.ACTION,
        hedging=Hedging.ASSERTED,
        artifact_path="p",
    )
    good_claim = StructuredClaim(
        claim_id="good",
        beat_id="B03",
        claim_text="cuts the mat",
        source_fact_ids=["F08"],
        assertion_type=AssertionType.ACTION,
        hedging=Hedging.ASSERTED,
        artifact_path="p",
    )
    result = validate_claims([bad_claim, good_claim], _minimal_scene())
    assert "bad" in result.invalid_fact_id_claim_ids
    assert "good" not in result.invalid_fact_id_claim_ids


# ---------------------------------------------------------------------------
# Test (c): zero-width char in claim_text is sanitized before output  [Contract H]
# ---------------------------------------------------------------------------

def test_zero_width_char_sanitized():
    """
    A claim_text containing a zero-width space (U+200B) must be stripped by sanitize()
    before the claim lands in the ValidatedClaims output.
    """
    # U+200B = zero-width space — invisible to the judge, caught by source_sanitizer
    dirty_text = "cuts​ the mat"
    claims = [
        StructuredClaim(
            claim_id="c_zw",
            beat_id="B03",
            claim_text=dirty_text,
            source_fact_ids=["F08"],
            assertion_type=AssertionType.ACTION,
            hedging=Hedging.ASSERTED,
            artifact_path="p",
        )
    ]
    result = validate_claims(claims, _minimal_scene())
    # Zero-width char must be absent from the output claim_text
    assert "​" not in result.claims[0].claim_text
    # The clean text is the stripped version
    assert result.claims[0].claim_text == "cuts the mat"
    # Not flagged for invalid id — sanitization is separate from id-validity
    assert result.invalid_fact_id_claim_ids == []


# ---------------------------------------------------------------------------
# Test (a): clean runs/demo_clean fixture → zero invalid ids against real G01 gold
# ---------------------------------------------------------------------------

def test_demo_clean_fixture_zero_invalid_ids():
    """
    The committed clean fixture (runs/demo_clean/structured_claims.yaml) must produce
    zero invalid_fact_id_claim_ids when validated against the real G01 gold scene.

    This is the integration smoke-test: if the fixture or gold drifts, this catches it.
    """
    # Load the real G01 scene from canon_gold.yaml
    gold_path = _REPO / "data" / "gold" / "canon_gold.yaml"
    raw = yaml.safe_load(gold_path.read_text(encoding="utf-8"))
    # canon_gold has a top-level `scenes:` list; G01 is first
    scene = CanonScene.model_validate(raw["scenes"][0])
    assert scene.scene_id == "G01"

    # Load the structured claims fixture
    fixture_path = _REPO / "runs" / "demo_clean" / "structured_claims.yaml"
    fixture_raw = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    claims = [StructuredClaim.model_validate(c) for c in fixture_raw["claims"]]

    result = validate_claims(claims, scene)

    # All 10 claims are returned
    assert len(result.claims) == 10
    # No fact-id violations in the clean fixture
    assert result.invalid_fact_id_claim_ids == [], (
        f"Expected zero invalid ids, got: {result.invalid_fact_id_claim_ids}"
    )


# ---------------------------------------------------------------------------
# Test: empty source_fact_ids is valid (no ids to be wrong)
# ---------------------------------------------------------------------------

def test_empty_source_fact_ids_not_flagged():
    """A claim with no cited ids cites nothing invalid — not flagged by id-check."""
    claims = [
        StructuredClaim(
            claim_id="c_empty",
            beat_id=None,
            claim_text="An interpretive aside.",
            source_fact_ids=[],
            assertion_type=AssertionType.INTERPRETATION,
            hedging=Hedging.HEDGED,
            artifact_path="p",
        )
    ]
    result = validate_claims(claims, _minimal_scene())
    assert result.invalid_fact_id_claim_ids == []
