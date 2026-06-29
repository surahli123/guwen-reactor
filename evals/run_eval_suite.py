"""Task 4a.4 — evaluate_run suite assembler (Contract E / fix F2).

Orchestrates the offline eval pipeline against a committed run fixture:
  load claims + gold -> validate_claims (4a.1) -> evaluate_claims (4a.2)
  -> beat_coverage (4a.3) -> stage-aware export status via export_requires_met (Contract F).

DEFINED BEFORE the drift suite (4b) and the CLI import it — this kills the forward dependency.

Stage-aware status (review #2): the canonical export_gate (specs/eval_plan.yaml) legitimately
includes human_approved + aigc_label_manifest_bound, which are produced LATER (approval/export,
4b.4). At eval time they default False, so we classify `missing`:
  - any CONTENT gate missing  -> export_status = BLOCKED
  - only approval/manifest    -> export_status = READY_FOR_APPROVAL  (content is clean)
This uses the single canonical gate (no duplicate list — Contract F preserved).
Safety (4b.2) + workflow-integrity (4b.6) default to pass with a TODO until their steps land.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from app.policy_gate import export_requires_met
from guwen_core.claim_validator import validate_claims
from guwen_core.coverage import beat_coverage
from guwen_core.schema_validator import CanonScene, StructuredClaim
from guwen_core.structural_audit import evaluate_claims

_REPO_ROOT = Path(__file__).parent.parent
_GOLD_PATH = _REPO_ROOT / "data" / "gold" / "canon_gold.yaml"

# Gates produced at approval/export (4b.4), not at eval time — see module docstring.
APPROVAL_GATES = {"human_approved", "aigc_label_manifest_bound"}


def _find_scenes(node):
    """Robustly locate the list of scenes regardless of the gold's top-level key."""
    if isinstance(node, dict):
        for v in node.values():
            if isinstance(v, list) and v and isinstance(v[0], dict) and "scene_id" in v[0]:
                return v
            found = _find_scenes(v)
            if found:
                return found
    return None


def _load_scene(scene_id: str) -> CanonScene:
    doc = yaml.safe_load(_GOLD_PATH.read_text(encoding="utf-8"))
    scenes = _find_scenes(doc) or []
    raw = next(s for s in scenes if s["scene_id"] == scene_id)
    return CanonScene.model_validate(raw)


def evaluate_run(run_dir: str | Path) -> dict:
    run_dir = Path(run_dir)
    doc = yaml.safe_load((run_dir / "structured_claims.yaml").read_text(encoding="utf-8"))
    scene = _load_scene(doc["scene_id"])
    claims = [StructuredClaim.model_validate(c) for c in doc.get("claims", [])]

    validated = validate_claims(claims, scene)
    audit = evaluate_claims(validated, scene)
    cov_str, cov_val = beat_coverage(audit.supported_fact_ids, scene)

    rep: dict = dict(audit.counts)                       # the 5 zero-count keys
    rep["required_beat_coverage"] = cov_val
    rep["coverage_fraction"] = cov_str
    rep["factual_precision"] = audit.factual_precision
    # Upstream/stage bools — default-pass with a TODO until their real steps land.
    rep["source_policy_valid"] = True                    # TODO(4b/source): wire source_guard meta
    rep["source_sanitized"] = True                       # claim_text sanitized in validate_claims (Contract H)
    rep["safety_pass"] = True                            # TODO(S7 / 4b.2): wire safety_eval
    rep["workflow_integrity_pass"] = True                # TODO(S9 / 4b.6): wire workflow_integrity
    rep["human_approved"] = False                        # set at approval (S10 / 4b.4)
    rep["aigc_label_manifest_bound"] = False             # set at export (S10 / 4b.4)

    ok, missing = export_requires_met(rep)
    # A coverage failure arrives as "required_beat_coverage>=0.85"; strip the comparator.
    content_missing = [m for m in missing if m.split(">=")[0] not in APPROVAL_GATES]
    rep["export_status"] = "BLOCKED" if content_missing else "READY_FOR_APPROVAL"
    rep["missing"] = missing
    rep["labels"] = [c.label.value for c in audit.labeled_claims]
    return rep
