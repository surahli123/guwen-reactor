from __future__ import annotations
from enum import Enum
from pathlib import Path
import yaml
from pydantic import BaseModel, field_validator


class ClaimLabel(str, Enum):
    SUPPORTED = "SUPPORTED"
    VALID_HEDGED_INTERPRETATION = "VALID_HEDGED_INTERPRETATION"
    CREATIVE_SAFE_FILLER = "CREATIVE_SAFE_FILLER"
    UNSUPPORTED_DETAIL = "UNSUPPORTED_DETAIL"
    UNSUPPORTED_MOTIVATION = "UNSUPPORTED_MOTIVATION"
    CONTRADICTED = "CONTRADICTED"
    INVALID_FACT_ID = "INVALID_FACT_ID"          # fix C3 — cited id absent from canon_gold
    AMBIGUOUS_REVIEW = "AMBIGUOUS_REVIEW"
    PROMPT_INJECTION_ATTEMPT = "PROMPT_INJECTION_ATTEMPT"


class AssertionType(str, Enum):
    ACTION = "action"
    MOTIVE = "motive"
    EMOTION = "emotion"
    INTERPRETATION = "interpretation"
    VISUAL = "visual"


class Hedging(str, Enum):
    ASSERTED = "asserted"
    HEDGED = "hedged"


# Labels that count toward unsupported_critical_claims (fix C1: critical UNSUPPORTED_DETAIL
# is added at audit time, not by enum membership — see structural_audit.py).
CRITICAL_LABELS = {
    ClaimLabel.UNSUPPORTED_MOTIVATION,
    ClaimLabel.CONTRADICTED,
    ClaimLabel.INVALID_FACT_ID,
    ClaimLabel.PROMPT_INJECTION_ATTEMPT,
}


class SourceChunk(BaseModel):
    chunk_id: str
    text_zh: str


class AtomicFact(BaseModel):
    id: str
    text: str
    source_chunk_ids: list[str]                  # Contract D: REQUIRED anchor to Chinese chunk

    @field_validator("source_chunk_ids")
    @classmethod
    def non_empty_anchor(cls, v):
        if not v:
            raise ValueError("atomic_fact must anchor to >=1 source_chunk_id")
        return v


class RequiredBeat(BaseModel):
    beat_id: str
    fact_ids: list[str]
    description: str


class CanonScene(BaseModel):
    scene_id: str
    title_en: str
    title_zh: str
    source_id: str
    source_chunks: list[SourceChunk]
    atomic_facts: list[AtomicFact]
    required_beats: list[RequiredBeat]
    forbidden_claims: list[str] = []

    @field_validator("source_chunks", "atomic_facts", "required_beats")
    @classmethod
    def non_empty(cls, v):
        if not v:
            raise ValueError("must be non-empty")
        return v


class StructuredClaim(BaseModel):
    """Contract A: emitted by the generator; the gate ASSIGNS the label from structure."""
    claim_id: str
    beat_id: str | None = None                   # which required beat (null = non-beat claim)
    claim_text: str
    source_fact_ids: list[str] = []              # ids the claim asserts it is grounded in
    assertion_type: AssertionType
    hedging: Hedging
    artifact_path: str
    label: ClaimLabel = ClaimLabel.AMBIGUOUS_REVIEW   # pre-audit default; gate overwrites


def load_yaml_as(model: type[BaseModel], path: str | Path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return model.model_validate(data)
