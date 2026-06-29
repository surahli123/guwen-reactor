"""Task 4b.3 — Regenerate loop + Denial-of-Wallet cap (Contract F / specs/eval_plan.yaml).

Implements the deterministic regen-loop control plane.  The actual model call is
[CONTRACT] and is injected via `evaluate_fn`, keeping this module fully testable with
no live model.

Canonical config (specs/eval_plan.yaml session_convergence):
    max_total_attempts: 3      # initial + 2 retries
    fail_closed_after_max_attempts: true
    log: [regenerate_rounds, converged, cost_to_converge_usd, tokens_to_converge]
"""
from __future__ import annotations

from typing import Any, Callable


def run_with_regen(
    generate_fn: Callable[[], Any],
    evaluate_fn: Callable[[Any], dict],
    max_total_attempts: int = 3,
) -> dict:
    """Run generate→evaluate loop with a hard attempt cap (Denial-of-Wallet guard).

    Args:
        generate_fn: Callable[[], Any] — produces a new candidate artifact each call.
            Receives no arguments; called once per attempt.
        evaluate_fn: Callable[[Any], dict] — evaluates the artifact returned by
            generate_fn.  Must return a dict with at least:
                export_status: str  ("BLOCKED" | "READY_FOR_APPROVAL")
            Optional cost-tracking keys (summed across attempts, default 0):
                cost_usd: float
                tokens: int
        max_total_attempts: int — hard cap including the initial attempt (default 3,
            matching specs/eval_plan.yaml).  After this many attempts without
            export_status != "BLOCKED", the loop fails-closed.

    Returns dict with keys (specs/eval_plan.yaml session_convergence.log):
        converged: bool              — True iff export_status != "BLOCKED" was reached
        fail_closed: bool            — True iff cap exhausted without convergence
        regenerate_rounds: int       — number of *extra* attempts after the initial one
                                       (0 = passed on first try; max max_total_attempts-1)
        cost_to_converge_usd: float  — sum of eval_fn-reported cost_usd across attempts
        tokens_to_converge: int      — sum of eval_fn-reported tokens across attempts
        export_status: str           — export_status from the final evaluation
        final_eval: dict             — the full dict returned by the last evaluate_fn call
    """
    total_cost: float = 0.0
    total_tokens: int = 0
    last_eval: dict = {}

    for attempt in range(max_total_attempts):
        artifact = generate_fn()
        last_eval = evaluate_fn(artifact)

        # Accumulate cost/token telemetry if the stub or real caller emits them.
        total_cost += float(last_eval.get("cost_usd", 0.0))
        total_tokens += int(last_eval.get("tokens", 0))

        if last_eval.get("export_status") != "BLOCKED":
            # Converged — export is READY_FOR_APPROVAL (or any non-BLOCKED status).
            return {
                "converged": True,
                "fail_closed": False,
                "regenerate_rounds": attempt,          # attempt 0 → 0 retries; attempt 2 → 2 retries
                "cost_to_converge_usd": total_cost,
                "tokens_to_converge": total_tokens,
                "export_status": last_eval["export_status"],
                "final_eval": last_eval,
            }

    # Cap exhausted — fail-closed: NEVER export, return BLOCKED status.
    return {
        "converged": False,
        "fail_closed": True,
        "regenerate_rounds": max_total_attempts - 1,   # all retries used
        "cost_to_converge_usd": total_cost,
        "tokens_to_converge": total_tokens,
        "export_status": "BLOCKED",
        "final_eval": last_eval,
    }
