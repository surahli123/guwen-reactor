"""evals/test_workflow_integrity.py — TDD for trace emitter + workflow integrity (Task 4b.6).

Three test groups:
  (a) correct order -> passed=True
  (b) out-of-order or missing event -> passed=False with reason string
  (c) conformance: trace.EMITTER_EVENTS == yaml required_events set (review #6)
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from guwen_core.trace import EMITTER_EVENTS, emit, read_events
from guwen_core.workflow_integrity import _load_required_events, check_order

_REPO_ROOT = Path(__file__).parent.parent
_EVAL_PLAN = _REPO_ROOT / "specs" / "eval_plan.yaml"

# Canonical required sequence loaded once for the module.
REQUIRED = [
    "source_policy_checked",
    "source_sanitized",
    "artifact_written",
    "claims_validated",
    "structural_audited",
    "coverage_computed",
    "safety_checked",
    "eval_completed",
    "approval_requested",
    "export_written",
]


# ---------------------------------------------------------------------------
# (a) Correct order -> passed
# ---------------------------------------------------------------------------


def test_exact_order_passes():
    passed, reason = check_order(REQUIRED, required=REQUIRED)
    assert passed is True
    assert reason == "ok"


def test_extra_events_between_required_pass():
    """Extra non-required events interspersed are OK."""
    emitted = []
    for ev in REQUIRED:
        emitted.append("some_internal_span")
        emitted.append(ev)
    passed, reason = check_order(emitted, required=REQUIRED)
    assert passed is True, reason


def test_duplicate_required_events_pass_when_first_in_order():
    """Duplicate occurrences of a required event are allowed if first is in order."""
    emitted = list(REQUIRED) + list(REQUIRED)  # whole sequence twice
    passed, reason = check_order(emitted, required=REQUIRED)
    assert passed is True, reason


def test_empty_required_always_passes():
    passed, reason = check_order(["some_event"], required=[])
    assert passed is True


# ---------------------------------------------------------------------------
# (b) Out-of-order or missing -> passed=False with informative reason
# ---------------------------------------------------------------------------


def test_missing_event_fails():
    emitted = [e for e in REQUIRED if e != "claims_validated"]
    passed, reason = check_order(emitted, required=REQUIRED)
    assert passed is False
    assert "claims_validated" in reason


def test_out_of_order_fails():
    """Swap structural_audited before claims_validated -> out of order."""
    emitted = list(REQUIRED)
    idx_cv = emitted.index("claims_validated")
    idx_sa = emitted.index("structural_audited")
    emitted[idx_cv], emitted[idx_sa] = emitted[idx_sa], emitted[idx_cv]
    passed, reason = check_order(emitted, required=REQUIRED)
    assert passed is False
    assert reason  # non-empty reason


def test_empty_emitted_fails():
    passed, reason = check_order([], required=REQUIRED)
    assert passed is False
    assert "source_policy_checked" in reason


def test_partial_emitted_fails():
    passed, reason = check_order(REQUIRED[:3], required=REQUIRED)
    assert passed is False
    assert "claims_validated" in reason


def test_reason_names_first_missing_event():
    """Reason should mention the first event that cannot be found."""
    emitted = ["source_policy_checked", "source_sanitized"]
    passed, reason = check_order(emitted, required=REQUIRED)
    assert passed is False
    assert "artifact_written" in reason


# ---------------------------------------------------------------------------
# (c) Conformance: trace.EMITTER_EVENTS == yaml required_events (review #6)
# ---------------------------------------------------------------------------


def test_emitter_vocabulary_matches_yaml_required_events():
    """The trace emitter's EMITTER_EVENTS set must equal the YAML required_events.

    This is the conformance test (review #6): a rename in either place will fail
    this test before it can silently break workflow_integrity.
    """
    doc = yaml.safe_load(_EVAL_PLAN.read_text(encoding="utf-8"))
    yaml_events: set[str] = set(doc["workflow_integrity"]["required_events"])
    assert EMITTER_EVENTS == yaml_events, (
        f"MISMATCH between trace.EMITTER_EVENTS and yaml required_events.\n"
        f"  In EMITTER_EVENTS only: {EMITTER_EVENTS - yaml_events}\n"
        f"  In YAML only: {yaml_events - EMITTER_EVENTS}"
    )


def test_yaml_required_events_matches_load_helper():
    """_load_required_events() returns the same list as the YAML (no transformation)."""
    doc = yaml.safe_load(_EVAL_PLAN.read_text(encoding="utf-8"))
    yaml_list = list(doc["workflow_integrity"]["required_events"])
    assert _load_required_events() == yaml_list


# ---------------------------------------------------------------------------
# emit() + read_events() integration (trace.py API)
# ---------------------------------------------------------------------------


def test_emit_writes_jsonl_record(tmp_path):
    emit(tmp_path, "source_policy_checked", span_type="EVENT", status="ok")
    records = (tmp_path / "trace.jsonl").read_text().splitlines()
    assert len(records) == 1
    rec = json.loads(records[0])
    assert rec["event"] == "source_policy_checked"
    assert rec["span_type"] == "EVENT"
    assert rec["status"] == "ok"
    assert "timestamp_ns" in rec


def test_emit_appends_multiple_records(tmp_path):
    for ev in REQUIRED:
        emit(tmp_path, ev)
    lines = (tmp_path / "trace.jsonl").read_text().splitlines()
    assert len(lines) == len(REQUIRED)


def test_emit_rejects_unknown_event(tmp_path):
    with pytest.raises(ValueError, match="Unknown trace event"):
        emit(tmp_path, "not_a_real_event")


def test_read_events_returns_ordered_names(tmp_path):
    for ev in REQUIRED:
        emit(tmp_path, ev)
    assert read_events(tmp_path) == REQUIRED


def test_read_events_empty_when_no_trace(tmp_path):
    assert read_events(tmp_path) == []


def test_emit_creates_run_dir(tmp_path):
    run_dir = tmp_path / "runs" / "test_run_001"
    assert not run_dir.exists()
    emit(run_dir, "source_policy_checked")
    assert (run_dir / "trace.jsonl").exists()


def test_full_trace_passes_check_order(tmp_path):
    """End-to-end: emit all required events then check_order from YAML defaults."""
    for ev in REQUIRED:
        emit(tmp_path, ev)
    emitted = read_events(tmp_path)
    passed, reason = check_order(emitted)  # uses YAML default
    assert passed is True, reason
