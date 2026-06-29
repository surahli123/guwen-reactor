"""guwen_core/trace.py — OTel-style JSONL trace emitter (Task 4b.6).

Orchestrator emits spans/events to runs/<id>/trace.jsonl.
The EMITTER_EVENTS set is the single authoritative vocabulary;
specs/eval_plan.yaml workflow_integrity.required_events must match it exactly
(asserted by test_workflow_integrity.py conformance test — review #6).
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

# Canonical event vocabulary — must equal specs/eval_plan.yaml workflow_integrity.required_events.
# Rename here + update the YAML; the conformance test will fail if they diverge.
EMITTER_EVENTS: frozenset[str] = frozenset(
    [
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
)


def emit(
    run_dir: str | Path,
    event: str,
    span_type: str = "EVENT",
    **kv: Any,
) -> None:
    """Append one OTel-named JSONL record to runs/<id>/trace.jsonl.

    Args:
        run_dir: path to the run directory (trace.jsonl lives here).
        event: one of EMITTER_EVENTS; raises ValueError if unknown.
        span_type: OTel span kind label (default "EVENT").
        **kv: extra key/value pairs merged into the record.

    Raises:
        ValueError: if event is not in EMITTER_EVENTS.
    """
    if event not in EMITTER_EVENTS:
        raise ValueError(
            f"Unknown trace event {event!r}. "
            f"Must be one of: {sorted(EMITTER_EVENTS)}"
        )
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp_ns": time.time_ns(),
        "span_type": span_type,
        "event": event,
        **kv,
    }
    trace_path = run_dir / "trace.jsonl"
    with trace_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_events(run_dir: str | Path) -> list[str]:
    """Return ordered list of event names from a run's trace.jsonl."""
    trace_path = Path(run_dir) / "trace.jsonl"
    if not trace_path.exists():
        return []
    events: list[str] = []
    for line in trace_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            record = json.loads(line)
            events.append(record["event"])
    return events
