"""Task 4a.3 — required-beat coverage (Contract C / fix C4).

A beat is "covered" iff ALL of its fact_ids are in supported_fact_ids — and
supported_fact_ids comes only from VALIDATED, beat-aligned SUPPORTED claims
(produced by the structural audit, 4a.2). Never self-reported, never keyword-matched.
"""
from __future__ import annotations

from guwen_core.schema_validator import CanonScene


def beat_coverage(supported_fact_ids: set, scene: CanonScene) -> tuple[str, float]:
    total = len(scene.required_beats)
    covered = sum(
        1 for b in scene.required_beats
        if set(b.fact_ids) <= set(supported_fact_ids)   # ALL beat facts supported
    )
    return (f"{covered}/{total}", covered / total if total else 0.0)
