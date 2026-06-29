"""evals/test_drift_injection.py — Task 4b.1: D1–D6 block proof.

Table-driven over all 6 drift types: inject a clean run, evaluate it, assert
export_status == BLOCKED and the expected blocking counter is non-zero (or
coverage drops below threshold for the omission case).
"""
import pytest

from guwen_core.drift_injector import inject
from evals.run_eval_suite import evaluate_run


@pytest.mark.parametrize("drift,expect_key", [
    ("forbidden_contradiction", "contradicted_claims"),
    ("unsupported_detail", "unsupported_critical_claims"),
    ("subtle_motivation_spoof", "unsupported_motivation_claims"),
    ("omission", "required_beat_coverage"),
    ("citation_spoof", "invalid_fact_id_claims"),
    ("judge_prompt_injection", "prompt_injection_attempts"),
])
def test_each_drift_blocks_export(tmp_path, drift, expect_key):
    d = inject("runs/demo_clean", tmp_path / "drift", drift)
    rep = evaluate_run(d)
    assert rep["export_status"] == "BLOCKED", (
        f"drift={drift!r}: expected BLOCKED, got {rep['export_status']!r}; "
        f"missing={rep.get('missing')}"
    )
    if expect_key == "required_beat_coverage":
        assert rep["required_beat_coverage"] < 0.85, (
            f"drift={drift!r}: coverage {rep['required_beat_coverage']} not < 0.85"
        )
    else:
        assert rep[expect_key] >= 1, (
            f"drift={drift!r}: expected {expect_key} >= 1, got {rep[expect_key]}"
        )
