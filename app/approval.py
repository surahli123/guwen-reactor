"""
app/approval.py — Human-approval step for Guwen Reactor (Task 4b.4).

approve_run checks that a run's eval_report has cleared all CONTENT gates
(export_status == READY_FOR_APPROVAL) before recording human approval.
Approval is refused if any content gate is still failing (BLOCKED).
"""
from __future__ import annotations

from pathlib import Path

from evals.run_eval_suite import APPROVAL_GATES

# Exact wording required by spec (Contract D / C7).
AIGC_LABEL = (
    "AI-generated adaptation. "
    "No existing English translation was provided to the generator."
)


def approve_run(run_dir: str | Path, eval_report: dict) -> dict:
    """
    Record human approval for a run.

    Returns a dict with ``human_approved=True`` and an approval summary.

    Raises
    ------
    PermissionError
        If any CONTENT gate (i.e. any gate that is *not* in APPROVAL_GATES)
        is still failing — i.e. the run is BLOCKED rather than
        READY_FOR_APPROVAL.

    Parameters
    ----------
    run_dir:
        Path to the run directory.  Used only for the run_id in the summary;
        nothing is written by this function.
    eval_report:
        The eval report dict returned by evaluate_run().
    """
    run_dir = Path(run_dir)
    missing: list[str] = eval_report.get("missing", [])

    # Strip the ">=<threshold>" suffix that coverage uses before comparing.
    content_missing = [
        m for m in missing if m.split(">=")[0] not in APPROVAL_GATES
    ]
    if content_missing:
        raise PermissionError(
            f"approval refused: content gates still failing: {content_missing}"
        )

    return {
        "human_approved": True,
        "run_id": run_dir.name,
        "aigc_label": AIGC_LABEL,
        "content_gates_passed": True,
        "approval_summary": (
            f"Run '{run_dir.name}' passed all content gates. {AIGC_LABEL}"
        ),
    }
