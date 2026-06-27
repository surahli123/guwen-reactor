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
import os
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

    Raises ValueError if:
    - run_id is invalid (traversal / unsafe chars)
    - name is empty, ".", "..", or contains any path separator
      NOTE: dots inside a component are allowed (e.g. "v1..2.yaml")
    - runs/<run_id> exists and is a symlink (would escape confinement)
    - the realpath of the result escapes the real runs/ root
    """
    validate_run_id(run_id)
    # Reject empty name and exact "." / ".." components; also reject any separator
    # characters.  Dots *inside* a name component (e.g. "v1..2.yaml") are fine.
    if name in {"", ".", ".."} or os.sep in name or "/" in name or "\\" in name:
        raise ValueError(f"illegal artifact name: {name!r}")

    # Anchor to the REAL runs root (symlinks in _REPO_ROOT itself resolved here).
    runs_root = (_REPO_ROOT / "runs").resolve()
    run_dir = runs_root / run_id

    # Reject if the run directory is itself a symlink — resolving through it would
    # let writes land outside the repo (the attack vector described in FIX 3).
    if run_dir.is_symlink():
        raise ValueError(f"run directory is a symlink: {run_dir}")

    # Final confinement check: resolve every remaining symlink via os.path.realpath
    # and confirm the result is still under runs_root.
    p = run_dir / name
    p_real = Path(os.path.realpath(p))
    if not p_real.is_relative_to(runs_root):
        raise ValueError(f"path escapes allowed root: {p_real}")
    return p_real


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
