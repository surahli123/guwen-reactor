"""MCP stdio server for the Guwen Reactor faithfulness gate."""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml
from mcp.server.fastmcp import FastMCP

from app.policy_gate import safe_path, source_guard, validate_run_id
from evals.run_eval_suite import evaluate_run

# MCP Python SDK verified against mcp==1.28.1 stable v1.x README/API:
# FastMCP, @mcp.tool(), and mcp.run(transport="stdio").
mcp = FastMCP("Guwen Reactor")

_REPO_ROOT = Path(__file__).parent.parent
_RUNS_ROOT = _REPO_ROOT / "runs"
_SOURCES_ROOT = _REPO_ROOT / "data" / "sources"
_VALID_SOURCE_ID = re.compile(r"^[a-zA-Z0-9_-]{1,128}$")


def _repo_uri(path: Path) -> str:
    return path.relative_to(_REPO_ROOT).as_posix()


def _run_dir_for(run_id: str) -> Path:
    validate_run_id(run_id)
    claims_path = safe_path(run_id, "structured_claims.yaml")
    run_dir = claims_path.parent
    runs_root = Path(os.path.realpath(_RUNS_ROOT))
    if not run_dir.is_relative_to(runs_root):
        raise ValueError(f"run_id escapes runs root: {run_id!r}")
    if not claims_path.exists():
        raise FileNotFoundError(f"unknown run_id: {run_id!r}")
    return run_dir


def _validate_source_id(source_id: str) -> None:
    if not _VALID_SOURCE_ID.match(source_id or ""):
        raise ValueError(f"invalid source_id: {source_id!r}")


def _load_source_metadata(source_id: str) -> tuple[Path, dict[str, Any]]:
    _validate_source_id(source_id)
    for metadata_path in sorted(_SOURCES_ROOT.glob("*/source_metadata.yaml")):
        meta = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) or {}
        if source_id in {metadata_path.parent.name, meta.get("source_id")}:
            return metadata_path.parent, meta
    raise FileNotFoundError(f"unknown source_id: {source_id!r}")


@mcp.tool()
def run_eval_suite(run_id: str) -> dict[str, Any]:
    """Run the deterministic eval suite for runs/<run_id>."""
    run_dir = _run_dir_for(run_id)
    rep = evaluate_run(run_dir)

    report_path = safe_path(run_id, "eval_report.yaml")
    report_path.write_text(yaml.safe_dump(rep, allow_unicode=True, sort_keys=False), encoding="utf-8")

    hard_gate_status = rep["export_status"]
    return {
        "eval_report_uri": _repo_uri(report_path),
        "passed": hard_gate_status != "BLOCKED",
        "hard_gate_status": hard_gate_status,
    }


@mcp.tool()
def check_source_policy(source_id: str) -> dict[str, Any]:
    """Check source metadata with the existing policy gate."""
    _, meta = _load_source_metadata(source_id)
    allowed, reasons = source_guard(meta)
    return {
        "allowed": allowed,
        "source_mode": meta.get("source_mode"),
        "reasons": reasons,
    }


@mcp.tool()
def get_source(source_id: str) -> dict[str, Any]:
    """Return source metadata pointers without exposing source text."""
    source_dir, meta = _load_source_metadata(source_id)
    source_path = source_dir / "source.zh.txt"
    metadata_path = source_dir / "source_metadata.yaml"
    if not source_path.exists():
        raise FileNotFoundError(f"missing source text for source_id: {source_id!r}")

    source_text = source_path.read_text(encoding="utf-8")
    # Deliberately metadata-only: callers get pointers and char_count, never raw
    # source text, because source content is untrusted and may contain injection.
    return {
        "source_id": meta.get("source_id", source_id),
        "char_count": len(source_text),
        "source_uri": _repo_uri(source_path),
        "metadata_uri": _repo_uri(metadata_path),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
