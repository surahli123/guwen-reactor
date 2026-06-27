"""
app/policy_gate.py — Policy gate for Guwen Reactor.

Implements:
  validate_run_id   – rejects traversal / unsafe run-ids
  safe_path         – confines artifact writes to runs/<run_id>/
  source_guard      – blocks english_translation_ingested and non-public-domain sources
  load_export_gate  – reads THE single canonical gate from specs/eval_plan.yaml (Contract F)
  export_requires_met – evaluates an eval report against the canonical gate

No gate constants are hardcoded here; everything is loaded from specs/eval_plan.yaml.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

# Alphanumeric + underscore/hyphen, 1-64 chars; rejects traversal and shell chars.
VALID_RUN_ID = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")

# Resolve the repo root relative to this file so load_export_gate works from any cwd.
_REPO_ROOT = Path(__file__).parent.parent
_DEFAULT_GATE_PATH = _REPO_ROOT / "specs" / "eval_plan.yaml"


def validate_run_id(run_id: str) -> bool:
    """Raise ValueError if run_id contains traversal or unsafe characters."""
    if not VALID_RUN_ID.match(run_id or ""):
        raise ValueError(f"invalid run_id: {run_id!r}")
    return True


def safe_path(run_id: str, name: str) -> Path:
    """
    Return an absolute path under runs/<run_id>/<name>.
    Raises ValueError if run_id is invalid or name tries to escape the allowed root.
    """
    validate_run_id(run_id)
    # Reject slash, backslash, or .. in the artifact name component.
    if "/" in name or "\\" in name or ".." in name:
        raise ValueError(f"illegal artifact name: {name!r}")
    p = (_REPO_ROOT / "runs" / run_id / name).resolve()
    root = (_REPO_ROOT / "runs" / run_id).resolve()
    if not str(p).startswith(str(root)):
        raise ValueError(f"path escapes allowed root: {p}")
    return p


def source_guard(meta: dict) -> tuple[bool, list[str]]:
    """
    Block sources that are not public-domain originals or that ingested an English
    translation (Copyright rule: 'No existing English translation was provided to
    the generator.').

    Returns (allowed: bool, reasons: list[str]).
    """
    reasons: list[str] = []
    if meta.get("english_translation_ingested") is True:
        reasons.append("english_translation_ingested")
    if meta.get("source_mode") != "public_domain_original":
        reasons.append(f"source_mode={meta.get('source_mode')!r}")
    return (not reasons, reasons)


def load_export_gate(path: str | Path | None = None) -> dict:
    """
    Load the single canonical export gate from specs/eval_plan.yaml (Contract F / fix F4).
    No other module should define or duplicate the gate lists.
    """
    gate_path = Path(path) if path is not None else _DEFAULT_GATE_PATH
    raw = yaml.safe_load(gate_path.read_text(encoding="utf-8"))
    return raw["export_gate"]


def export_requires_met(
    rep: dict,
    gate: dict | None = None,
) -> tuple[bool, list[str]]:
    """
    Evaluate an eval report dict against the canonical export gate.

    Uses the ACTUAL specs/eval_plan.yaml schema (coverage_gate.metric / coverage_gate.min),
    NOT the plan's erroneous gate["min_coverage"] key.

    Returns (ok: bool, missing: list[str]).
    """
    gate = gate or load_export_gate()

    missing: list[str] = []

    # bool_gates — each must be True
    for g in gate["bool_gates"]:
        if rep.get(g) is not True:
            missing.append(g)

    # zero_count_gates — each must == 0
    for g in gate["zero_count_gates"]:
        if rep.get(g, 1) != 0:
            missing.append(g)

    # coverage_gate — metric must be >= min (fix: use coverage_gate, not min_coverage)
    cov = gate["coverage_gate"]
    metric: str = cov["metric"]
    cmin: float = cov["min"]
    if rep.get(metric, 0) < cmin:
        missing.append(f"{metric}>={cmin}")

    return (not missing, missing)
