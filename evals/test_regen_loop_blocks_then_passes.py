"""Task 4b.3 — TDD tests for run_with_regen (Denial-of-Wallet cap).

Two scenarios (specs/eval_plan.yaml session_convergence):
  (a) evaluate_fn returns BLOCKED twice, then READY_FOR_APPROVAL → converges within 3 attempts.
  (b) evaluate_fn always returns BLOCKED → fail-closed after exactly 3 attempts, converged=False.

No live model required: both generate_fn and evaluate_fn are injected stubs.
"""
from __future__ import annotations

import pytest

from guwen_core.regen_loop import run_with_regen


# ---------------------------------------------------------------------------
# Scenario (a): BLOCKED × 2, then READY_FOR_APPROVAL → converges in 3 attempts
# ---------------------------------------------------------------------------

def test_converges_on_third_attempt():
    """Generator yields BLOCKED twice then READY_FOR_APPROVAL; must converge."""
    eval_results = [
        {"export_status": "BLOCKED"},
        {"export_status": "BLOCKED"},
        {"export_status": "READY_FOR_APPROVAL"},
    ]
    generate_calls = {"n": 0}
    evaluate_calls = {"n": 0}

    def generate_fn():
        generate_calls["n"] += 1
        return {}  # stub artifact — content irrelevant

    def evaluate_fn(artifact):
        idx = evaluate_calls["n"]
        evaluate_calls["n"] += 1
        return eval_results[idx]

    result = run_with_regen(generate_fn, evaluate_fn, max_total_attempts=3)

    # Convergence
    assert result["converged"] is True, "must converge when READY_FOR_APPROVAL reached"
    assert result["fail_closed"] is False

    # Exactly 3 total attempts (1 initial + 2 retries)
    assert generate_calls["n"] == 3, "generate_fn must be called exactly 3 times"
    assert evaluate_calls["n"] == 3, "evaluate_fn must be called exactly 3 times"

    # regenerate_rounds == retries == 2 (attempt indices 0, 1, 2 → passed on index 2)
    assert result["regenerate_rounds"] == 2

    # Final status matches the passing eval
    assert result["export_status"] == "READY_FOR_APPROVAL"
    assert result["final_eval"]["export_status"] == "READY_FOR_APPROVAL"


# ---------------------------------------------------------------------------
# Scenario (b): always BLOCKED → fail-closed after exactly 3 attempts
# ---------------------------------------------------------------------------

def test_fail_closed_after_max_attempts():
    """Generator always returns BLOCKED; must fail-closed after max_total_attempts."""
    generate_calls = {"n": 0}
    evaluate_calls = {"n": 0}

    def generate_fn():
        generate_calls["n"] += 1
        return {}

    def evaluate_fn(artifact):
        evaluate_calls["n"] += 1
        return {"export_status": "BLOCKED"}

    result = run_with_regen(generate_fn, evaluate_fn, max_total_attempts=3)

    # Fail-closed, never converged
    assert result["converged"] is False, "must NOT converge when always BLOCKED"
    assert result["fail_closed"] is True, "must fail-closed after cap exhausted"

    # Exactly 3 total attempts — no more, no less
    assert generate_calls["n"] == 3, "must attempt exactly max_total_attempts times"
    assert evaluate_calls["n"] == 3, "evaluate_fn must be called exactly max_total_attempts times"

    # Status stays BLOCKED; never exported
    assert result["export_status"] == "BLOCKED"
    assert result["regenerate_rounds"] == 2  # all retries consumed


# ---------------------------------------------------------------------------
# Bonus: cap is respected even with a custom max_total_attempts value
# ---------------------------------------------------------------------------

def test_respects_custom_max_attempts():
    """Cap is enforced at the caller-supplied value (not hardcoded to 3)."""
    calls = {"n": 0}

    def generate_fn():
        return {}

    def evaluate_fn(artifact):
        calls["n"] += 1
        return {"export_status": "BLOCKED"}

    result = run_with_regen(generate_fn, evaluate_fn, max_total_attempts=5)

    assert calls["n"] == 5
    assert result["converged"] is False
    assert result["fail_closed"] is True
    assert result["regenerate_rounds"] == 4


# ---------------------------------------------------------------------------
# Bonus: cost + token telemetry accumulated across attempts
# ---------------------------------------------------------------------------

def test_cost_and_token_telemetry_accumulated():
    """cost_to_converge_usd and tokens_to_converge are summed across all attempts."""
    call_count = {"n": 0}

    def generate_fn():
        return {}

    def evaluate_fn(artifact):
        call_count["n"] += 1
        if call_count["n"] == 3:
            return {"export_status": "READY_FOR_APPROVAL", "cost_usd": 0.005, "tokens": 200}
        return {"export_status": "BLOCKED", "cost_usd": 0.002, "tokens": 100}

    result = run_with_regen(generate_fn, evaluate_fn, max_total_attempts=3)

    assert result["converged"] is True
    assert abs(result["cost_to_converge_usd"] - 0.009) < 1e-9   # 0.002 + 0.002 + 0.005
    assert result["tokens_to_converge"] == 400                   # 100 + 100 + 200
