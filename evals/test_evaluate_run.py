"""Task 4a.4 — evaluate_run suite assembler (Contract E / fix F2).
Defined BEFORE the drift suite so 4b + CLI import it. TDD: written before the impl.
Proves both directions: a clean fixture is READY_FOR_APPROVAL; a content failure is BLOCKED;
and the review-#2 staging holds (an unapproved-but-clean run is NOT blocked)."""
import pathlib
import shutil

import yaml

from evals.run_eval_suite import evaluate_run

_COUNT_KEYS = ("unsupported_critical_claims", "contradicted_claims",
               "unsupported_motivation_claims", "invalid_fact_id_claims",
               "prompt_injection_attempts", "required_beat_coverage")


def test_clean_fixture_not_blocked():
    rep = evaluate_run("runs/demo_clean")
    # review #2: content-clean but unapproved -> READY_FOR_APPROVAL, NOT blocked
    assert rep["export_status"] == "READY_FOR_APPROVAL"
    for k in _COUNT_KEYS:
        assert k in rep
    assert rep["required_beat_coverage"] == 1.0
    assert rep["unsupported_critical_claims"] == 0


def test_content_failure_blocks(tmp_path):
    src = pathlib.Path("runs/demo_clean")
    dst = tmp_path / "bad"
    shutil.copytree(src, dst)
    doc = yaml.safe_load((dst / "structured_claims.yaml").read_text())
    doc["claims"].append({  # a forbidden claim -> CONTRADICTED -> content gate fails
        "claim_id": "BAD", "claim_text": "Hua Xin keeps the gold.",
        "source_fact_ids": [], "assertion_type": "action", "hedging": "asserted",
        "artifact_path": "p"})
    (dst / "structured_claims.yaml").write_text(yaml.safe_dump(doc))
    rep = evaluate_run(dst)
    assert rep["export_status"] == "BLOCKED"
    assert rep["contradicted_claims"] == 1


def test_approval_gates_are_real_bool_gates():   # review MINOR #2 — catch APPROVAL_GATES drifting from the YAML
    from app.policy_gate import load_export_gate
    from evals.run_eval_suite import APPROVAL_GATES
    assert APPROVAL_GATES <= set(load_export_gate()["bool_gates"])
