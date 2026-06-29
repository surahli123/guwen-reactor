"""Task 4a.5 — specificity / over-block guard (Contract G / fix F7, non-negotiable).

Proves the gate does NOT over-block: a VALID hedged interpretation on an otherwise clean
run must not flip export_status to BLOCKED. Pairs with the drift suite (4b.1, proves it DOES
block bad claims). Together they show the gate is neither too loose nor too tight."""
import pathlib
import shutil

import yaml

from evals.run_eval_suite import evaluate_run


def test_valid_hedged_interpretation_does_not_block(tmp_path):
    src = pathlib.Path("runs/demo_clean")
    dst = tmp_path / "spec"
    shutil.copytree(src, dst)
    doc = yaml.safe_load((dst / "structured_claims.yaml").read_text())
    doc["claims"].append({
        "claim_id": "SPEC1", "beat_id": "B03",
        "claim_text": "Perhaps Guan Ning prized integrity over status.",
        "source_fact_ids": ["F08"], "assertion_type": "interpretation",
        "hedging": "hedged", "artifact_path": "cultural_decoder.note"})
    (dst / "structured_claims.yaml").write_text(yaml.safe_dump(doc))

    rep = evaluate_run(dst)
    assert rep["export_status"] != "BLOCKED"          # over-block guard
    assert rep["unsupported_critical_claims"] == 0
