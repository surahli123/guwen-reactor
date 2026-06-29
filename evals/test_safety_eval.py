"""
Tests for guwen_core/safety_eval.py — Task 4b.2.

TDD order: write failing tests first, then implement, then verify all pass.
Tests cover:
  - demo_clean fixture (must pass — gate precondition)
  - each deny-list category catches an injected phrase
  - multiple categories reported together
  - NFKC normalisation bypass attempt blocked
  - SafetyResult is a pydantic model
  - semantic stub raises NotImplementedError (advisory, never reached offline)
"""
from __future__ import annotations
import pytest
import yaml
from pathlib import Path

from guwen_core.safety_eval import SafetyResult, safety_check, safety_check_semantic_stub
from guwen_core.schema_validator import StructuredClaim


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DEMO_CLEAN_PATH = Path("runs/demo_clean/structured_claims.yaml")


def _load_demo_clean_claims() -> list[StructuredClaim]:
    data = yaml.safe_load(_DEMO_CLEAN_PATH.read_text(encoding="utf-8"))
    return [StructuredClaim(**c) for c in data["claims"]]


def _make_claim(text: str) -> StructuredClaim:
    """Minimal StructuredClaim with only claim_text varied."""
    return StructuredClaim(
        claim_id="TEST_SAFETY",
        claim_text=text,
        assertion_type="action",
        hedging="asserted",
        artifact_path="test.path",
    )


# ---------------------------------------------------------------------------
# Core contract: clean fixture passes
# ---------------------------------------------------------------------------

def test_demo_clean_claims_pass():
    """All demo_clean claims must produce passed=True (gate precondition)."""
    claims = _load_demo_clean_claims()
    result = safety_check(claims)
    assert result.passed is True
    assert result.violations == []


# ---------------------------------------------------------------------------
# Deny-list: each category catches an injected phrase
# ---------------------------------------------------------------------------

def test_gore_phrase_triggers_violation():
    """Claim injected with graphic gore → passed=False, category in violations."""
    claim = _make_claim(
        "In this adaptation the character's entrails spill out in graphic violence."
    )
    result = safety_check([claim])
    assert result.passed is False
    assert "gore_not_in_source" in result.violations


def test_severed_limb_triggers_gore():
    """Another gore variant: severed limb."""
    claim = _make_claim("The battle leaves severed limbs across the road.")
    result = safety_check([claim])
    assert result.passed is False
    assert "gore_not_in_source" in result.violations


def test_sexualized_framing_triggers_violation():
    """Sexualized phrase → passed=False."""
    claim = _make_claim(
        "The scene depicts an erotic encounter between the two scholars."
    )
    result = safety_check([claim])
    assert result.passed is False
    assert "sexualized_framing" in result.violations


def test_hate_triggers_violation():
    """Hate phrase → passed=False."""
    claim = _make_claim("All subhuman enemies of the state must be eliminated.")
    result = safety_check([claim])
    assert result.passed is False
    assert "hate_or_harassment" in result.violations


def test_wrongdoing_instructions_triggers_violation():
    """Wrongdoing-instructions phrase → passed=False."""
    claim = _make_claim(
        "This scene illustrates how to make a bomb using common materials."
    )
    result = safety_check([claim])
    assert result.passed is False
    assert "wrongdoing_instructions" in result.violations


# ---------------------------------------------------------------------------
# Multiple categories both reported
# ---------------------------------------------------------------------------

def test_multiple_categories_all_reported():
    """Two unsafe claims in one batch → both categories appear in violations."""
    claims = [
        _make_claim("The warrior's severed head was displayed at the gate."),
        _make_claim("The manuscript contains erotic imagery."),
    ]
    result = safety_check(claims)
    assert result.passed is False
    assert "gore_not_in_source" in result.violations
    assert "sexualized_framing" in result.violations


# ---------------------------------------------------------------------------
# Normalisation: fullwidth-char bypass blocked
# ---------------------------------------------------------------------------

def test_unicode_normalised_before_check():
    """Fullwidth 'g' (U+FF47) normalises to ASCII 'g' → deny-list still fires."""
    # U+FF47 ｇ  →  NFKC  →  g
    claim = _make_claim("The adaptation shows ｇore and mutilation added by the writer.")
    result = safety_check([claim])
    assert result.passed is False
    assert "gore_not_in_source" in result.violations


# ---------------------------------------------------------------------------
# SafetyResult is a pydantic model
# ---------------------------------------------------------------------------

def test_safety_result_is_pydantic_model():
    """SafetyResult must be a pydantic BaseModel with passed + violations fields."""
    r = SafetyResult(passed=True, violations=[])
    assert r.passed is True
    assert r.violations == []

    r2 = SafetyResult(passed=False, violations=["gore_not_in_source"])
    assert r2.passed is False
    assert "gore_not_in_source" in r2.violations


# ---------------------------------------------------------------------------
# Semantic stub: advisory / [CONTRACT] — never called offline
# ---------------------------------------------------------------------------

def test_semantic_stub_raises_not_implemented():
    """Semantic stub must always raise NotImplementedError (never reached offline)."""
    with pytest.raises(NotImplementedError):
        safety_check_semantic_stub("some adaptation text")
