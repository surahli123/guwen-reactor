"""guwen_core/workflow_integrity.py — IN_ORDER workflow gate (Task 4b.6).

check_order verifies that every required event appears in the emitted list
in the exact order specified by specs/eval_plan.yaml workflow_integrity.required_events
(Contract F / single source of truth).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

_REPO_ROOT = Path(__file__).parent.parent
_EVAL_PLAN = _REPO_ROOT / "specs" / "eval_plan.yaml"


def _load_required_events() -> list[str]:
    """Load required_events from specs/eval_plan.yaml (single source of truth)."""
    doc = yaml.safe_load(_EVAL_PLAN.read_text(encoding="utf-8"))
    return list(doc["workflow_integrity"]["required_events"])


def check_order(
    emitted_events: list[str],
    required: Optional[list[str]] = None,
) -> tuple[bool, str]:
    """Check that required events appear in emitted_events in the required order.

    Mode: IN_ORDER — each required event must appear, and their relative order
    in emitted_events must match the required sequence.  Extra events between
    required events are allowed; duplicates of required events are accepted as
    long as the first occurrence is in order.

    Args:
        emitted_events: ordered list of event names from trace.jsonl.
        required: sequence to check; defaults to specs/eval_plan.yaml
                  workflow_integrity.required_events.

    Returns:
        (True, "ok") when all required events appear in order.
        (False, reason_str) otherwise — reason names the first violation.
    """
    if required is None:
        required = _load_required_events()

    cursor = 0  # position in emitted_events
    for req_event in required:
        # Find req_event in emitted_events starting from cursor.
        found_at = None
        for i in range(cursor, len(emitted_events)):
            if emitted_events[i] == req_event:
                found_at = i
                break
        if found_at is None:
            return (
                False,
                f"required event {req_event!r} not found in emitted events "
                f"(searched from position {cursor})",
            )
        cursor = found_at + 1  # next required event must come after this one

    return (True, "ok")
