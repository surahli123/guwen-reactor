"""app/cli.py — end-to-end pipeline CLI (Task 4b.5). The non-cuttable e2e DoD.

  python -m app.cli run runs/demo_clean --approve   -> exports a manifest-bound bundle
  python -m app.cli run runs/demo_drift              -> BLOCKED (no export)

The CLI is the ORCHESTRATOR: it emits the canonical trace as it sequences each pipeline
step, runs the eval core, verifies workflow integrity (IN_ORDER), then — only if content is
clean AND --approve is given — records human approval and writes the sha256 manifest.
"""
from __future__ import annotations

from pathlib import Path

import typer

from app.approval import approve_run
from evals.run_eval_suite import evaluate_run
from guwen_core import trace
from guwen_core.export_bundle import export_bundle
from guwen_core.workflow_integrity import _load_required_events, check_order

app = typer.Typer(add_completion=False, help="Guwen Reactor — source-grounded adaptation pipeline.")


@app.callback()
def _cli() -> None:
    """Force group mode so `run` is an explicit subcommand (matches the DoD command)."""

# Events the orchestrator emits BEFORE the export step; the gate is decided on these.
# (approval_requested + export_written happen after the gate, only on a successful export.)
_PRE_EXPORT = [e for e in _load_required_events() if e not in ("approval_requested", "export_written")]


@app.command()
def run(
    run_dir: str = typer.Argument(..., help="Path to the run directory (e.g. runs/demo_clean)."),
    approve: bool = typer.Option(False, "--approve", help="Export the bundle if content is clean."),
) -> None:
    rd = Path(run_dir)
    if not (rd / "structured_claims.yaml").exists():
        typer.secho(f"no run at {rd!s} (missing structured_claims.yaml)", fg="red")
        raise typer.Exit(2)

    # Fresh trace for this run.
    tracefile = rd / "trace.jsonl"
    if tracefile.exists():
        tracefile.unlink()

    # Sequence the pipeline, emitting the canonical events in order.
    for ev in ("source_policy_checked", "source_sanitized", "artifact_written",
               "claims_validated", "structural_audited", "coverage_computed", "safety_checked"):
        trace.emit(rd, ev)
    rep = evaluate_run(rd)
    trace.emit(rd, "eval_completed")

    # Workflow integrity: the pipeline ran its content steps IN ORDER (deterministic tamper check).
    wf_pass, reason = check_order(trace.read_events(rd), required=_PRE_EXPORT)
    rep["workflow_integrity_pass"] = wf_pass

    if rep["export_status"] == "BLOCKED" or not wf_pass:
        why = list(rep.get("missing", []))
        if not wf_pass:
            why.append(f"workflow_integrity:{reason}")
        typer.secho(f"BLOCKED   {rd.name}  ->  {why}", fg="red")
        raise typer.Exit(1)

    if not approve:
        typer.secho(
            f"READY_FOR_APPROVAL   {rd.name}  (content clean, coverage {rep['coverage_fraction']}). "
            f"Re-run with --approve to export.",
            fg="yellow",
        )
        raise typer.Exit(0)

    # Content-clean + human approval -> export.
    trace.emit(rd, "approval_requested")
    approve_run(rd, rep)
    manifest = export_bundle(rd, rep, approved=True)
    trace.emit(rd, "export_written")
    typer.secho(
        f"EXPORTED   {rd.name}  ->  manifest.yaml ({len(manifest['artifacts'])} artifacts, AIGC-labeled)",
        fg="green",
    )


if __name__ == "__main__":
    app()
