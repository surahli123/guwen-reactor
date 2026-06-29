"""Adaptation generator interface (Task 3.1).

Two paths, deliberately separated so the eval core has ZERO live-model dependency:

1. `load_committed_adaptation()` — OFFLINE. Reads a committed run fixture
   (e.g. runs/demo_clean/). This is what Phase 4a/4b and the CLI exercise. No API key.

2. `generate_adaptation()` — LIVE, `[CONTRACT]`. The real Gemini call that emits
   StructuredClaim records (Contract A). NOT implemented here: per "don't invent API
   syntax," the exact google-genai Developer-API signature is the unverified `G_GEMINI`
   gate (see build_log.md) and is wired only at Phase 5 / S13, after the signature is
   confirmed against current docs. The eval core never imports this path.
"""
from __future__ import annotations

from pathlib import Path

import yaml


def load_committed_adaptation(run_dir: str | Path) -> dict:
    """Load a committed run fixture: {adaptation, claims, scene_id}.

    The offline entry point for the eval core. `claims` is the raw list of
    StructuredClaim mappings (validated downstream by the structure validator, S1),
    kept as plain dicts here so this loader stays schema-agnostic.
    """
    run_dir = Path(run_dir)
    adaptation = yaml.safe_load((run_dir / "adaptation.yaml").read_text(encoding="utf-8"))
    claims_doc = yaml.safe_load((run_dir / "structured_claims.yaml").read_text(encoding="utf-8"))
    return {
        "scene_id": claims_doc.get("scene_id"),
        "adaptation": adaptation,
        "claims": claims_doc.get("claims", []),
    }


def generate_adaptation(scene: dict, *args, **kwargs) -> dict:  # pragma: no cover
    """LIVE generation via Gemini (`[CONTRACT]`, G_GEMINI). Wired at S13, not before.

    Must emit StructuredClaim records directly (Contract A) — beat-anchored fields,
    not free prose. Intentionally unimplemented so nothing in the offline eval core
    can accidentally depend on a live model or an unverified API signature.
    """
    raise NotImplementedError(
        "Live generation is the G_GEMINI [CONTRACT] gate — implement at Phase 5/S13 "
        "after confirming the google-genai Developer-API call signature against current docs."
    )
