"""MCP server wrapper tests.

These call the tool functions directly so the suite stays offline and does not
depend on an MCP client process.
"""
from pathlib import Path

import pytest

from app.mcp_server import check_source_policy, get_source, run_eval_suite


def test_run_eval_suite_wraps_clean_fixture():
    report_path = Path("runs/demo_clean/eval_report.yaml")
    try:
        result = run_eval_suite("demo_clean")
        assert result == {
            "eval_report_uri": "runs/demo_clean/eval_report.yaml",
            "passed": True,
            "hard_gate_status": "READY_FOR_APPROVAL",
        }
        assert report_path.exists()
    finally:
        report_path.unlink(missing_ok=True)


def test_run_eval_suite_rejects_traversal():
    with pytest.raises(ValueError):
        run_eval_suite("../demo_clean")


def test_check_source_policy_uses_existing_policy_gate():
    result = check_source_policy("fixture_unclear_license")
    assert result["allowed"] is False
    assert result["source_mode"] == "unclear_license"
    assert result["reasons"] == ["source_mode='unclear_license'"]


def test_get_source_returns_metadata_only():
    result = get_source("shishuo_xinyu_de_xing_guan_ning")
    source_path = Path("data/sources/guan_ning_cuts_mat/source.zh.txt")
    source_text = source_path.read_text(encoding="utf-8")

    assert result == {
        "source_id": "shishuo_xinyu_de_xing_guan_ning",
        "char_count": len(source_text),
        "source_uri": source_path.as_posix(),
        "metadata_uri": "data/sources/guan_ning_cuts_mat/source_metadata.yaml",
    }
    assert "text" not in result
    assert source_text not in str(result)


def test_unknown_source_id_raises():
    with pytest.raises(FileNotFoundError):
        get_source("missing_source")
