"""
Task 4b.4 — TDD tests for approve_run + export_bundle.

Three required cases:
  (a) gate-passed + approved=True  → exports; manifest has sha256 + AIGC label.
  (b) gate-passed + approved=False → PermissionError.
  (c) content-gate-FAILED + approved=True → PermissionError (never export a blocked run).
"""
from __future__ import annotations

import pathlib
import shutil

import pytest

from app.approval import AIGC_LABEL, approve_run
from evals.run_eval_suite import evaluate_run
from guwen_core.export_bundle import export_bundle

_DEMO_CLEAN = pathlib.Path("runs/demo_clean")
_DEMO_DRIFT = pathlib.Path("runs/demo_drift")


# ── (a) gate-passed + approved=True → exports ─────────────────────────────────

def test_gate_passed_and_approved_exports(tmp_path):
    """Clean run + approved=True → manifest.yaml written; sha256 + AIGC label present."""
    # Copy fixture so committed runs/ dir stays clean.
    run_dir = tmp_path / "demo_clean"
    shutil.copytree(_DEMO_CLEAN, run_dir)

    rep = evaluate_run(run_dir)
    assert rep["export_status"] == "READY_FOR_APPROVAL", (
        f"precondition failed: expected READY_FOR_APPROVAL, got {rep['export_status']}"
    )

    manifest = export_bundle(run_dir, rep, approved=True)

    # Top-level AIGC label must be the exact spec wording.
    assert manifest["aigc_label"] == AIGC_LABEL

    # Every artifact entry must carry sha256 + per-artifact AIGC label.
    assert len(manifest["artifacts"]) > 0, "manifest must list at least one artifact"
    for name, info in manifest["artifacts"].items():
        assert "sha256" in info, f"missing sha256 for artifact {name!r}"
        assert len(info["sha256"]) == 64, f"sha256 must be 64 hex chars for {name!r}"
        assert info.get("aigc_label") == AIGC_LABEL, (
            f"aigc_label missing or wrong for {name!r}"
        )

    # manifest.yaml physically present in the run dir.
    assert (run_dir / "manifest.yaml").exists()


def test_manifest_sha256_changes_when_artifact_tampered(tmp_path):
    """Tampering an artifact yields a different sha256 on the next export."""
    run_dir = tmp_path / "demo_clean"
    shutil.copytree(_DEMO_CLEAN, run_dir)

    rep = evaluate_run(run_dir)
    manifest_before = export_bundle(run_dir, rep, approved=True)

    # Tamper adaptation.yaml.
    adaptation = run_dir / "adaptation.yaml"
    adaptation.write_text(
        adaptation.read_text(encoding="utf-8") + "\n# TAMPERED\n",
        encoding="utf-8",
    )

    manifest_after = export_bundle(run_dir, rep, approved=True)

    sha_before = manifest_before["artifacts"]["adaptation.yaml"]["sha256"]
    sha_after = manifest_after["artifacts"]["adaptation.yaml"]["sha256"]
    assert sha_before != sha_after, "tampered artifact must produce a different sha256"


# ── (b) gate-passed + approved=False → raises ─────────────────────────────────

def test_gate_passed_not_approved_raises():
    """Clean run + approved=False → PermissionError before any I/O."""
    rep = evaluate_run(_DEMO_CLEAN)
    assert rep["export_status"] == "READY_FOR_APPROVAL"

    with pytest.raises(PermissionError, match="approved=False"):
        export_bundle(_DEMO_CLEAN, rep, approved=False)


# ── (c) content-gate-FAILED + approved=True → raises ──────────────────────────

def test_content_gate_failed_approved_raises():
    """Drift run (BLOCKED) + approved=True → PermissionError; never exports."""
    rep = evaluate_run(_DEMO_DRIFT)
    assert rep["export_status"] == "BLOCKED", (
        f"precondition: expected BLOCKED, got {rep['export_status']}"
    )

    with pytest.raises(PermissionError, match="content gates not met"):
        export_bundle(_DEMO_DRIFT, rep, approved=True)


# ── approve_run unit tests ─────────────────────────────────────────────────────

def test_approve_run_clean_returns_human_approved():
    """Clean run eval_report → approve_run returns human_approved=True + AIGC label."""
    rep = evaluate_run(_DEMO_CLEAN)
    result = approve_run(_DEMO_CLEAN, rep)

    assert result["human_approved"] is True
    assert result["aigc_label"] == AIGC_LABEL
    assert result["content_gates_passed"] is True


def test_approve_run_blocked_raises():
    """Blocked run → approve_run raises PermissionError."""
    rep = evaluate_run(_DEMO_DRIFT)

    with pytest.raises(PermissionError, match="content gates still failing"):
        approve_run(_DEMO_DRIFT, rep)
