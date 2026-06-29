"""
guwen_core/export_bundle.py — Manifest-bound export for Guwen Reactor (Task 4b.4).

export_bundle writes a manifest.yaml containing the sha256 of each artifact
and the AIGC label string.  It refuses unless BOTH:
  (a) the full export gate passes after setting human_approved=True and
      aigc_label_manifest_bound=True, AND
  (b) approved is explicitly True.

Path confinement: validate_run_id() on the run dir name (the same traversal /
unsafe-char check that safe_path performs).  In production the CLI always
passes a path that is already under runs/<id>/.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from app.approval import AIGC_LABEL
from app.policy_gate import export_requires_met, validate_run_id
from guwen_core.artifact_store import write_artifact

# Extensions treated as exportable artifacts; manifest.yaml is excluded to
# avoid circular sha256 (we skip it explicitly below).
_ARTIFACT_EXTS = frozenset({".yaml", ".json", ".txt", ".md", ".html"})


def export_bundle(
    run_dir: str | Path,
    eval_report: dict,
    approved: bool,
) -> dict:
    """
    Write ``manifest.yaml`` to *run_dir* and return the manifest dict.

    Parameters
    ----------
    run_dir:
        Directory that contains the adaptation artifacts.
    eval_report:
        Eval report returned by ``evaluate_run()``.  Must already have all
        content gates passing (export_status == READY_FOR_APPROVAL).
    approved:
        Must be ``True``; passing ``False`` raises immediately before any I/O.

    Returns
    -------
    dict
        The manifest dict written to ``run_dir/manifest.yaml``.

    Raises
    ------
    PermissionError
        If *approved* is ``False`` OR the full export gate is not met after
        accounting for human_approved + aigc_label_manifest_bound.
    ValueError
        If *run_dir*'s name is not a valid run_id (traversal / unsafe chars).
    """
    run_dir = Path(run_dir).resolve()
    run_id = run_dir.name

    # Security: validate run_id — same traversal / unsafe-char check as safe_path.
    validate_run_id(run_id)

    # Gate (b): explicit human sign-off must be True before any I/O.
    if not approved:
        raise PermissionError(
            "export refused: approved=False — human approval required"
        )

    # Gate (a): evaluate the full gate with approval flags set.
    rep = dict(eval_report)
    rep["human_approved"] = True
    rep["aigc_label_manifest_bound"] = True
    ok, missing = export_requires_met(rep)
    if not ok:
        raise PermissionError(
            f"export refused: content gates not met: {missing}"
        )

    # Compute sha256 for each artifact (skip manifest.yaml to avoid circularity).
    artifacts: dict[str, dict] = {}
    for f in sorted(run_dir.iterdir()):
        if (
            f.is_file()
            and f.suffix in _ARTIFACT_EXTS
            and f.name != "manifest.yaml"
        ):
            content = f.read_text(encoding="utf-8")
            sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
            artifacts[f.name] = {"sha256": sha, "aigc_label": AIGC_LABEL}

    manifest: dict = {
        "run_id": run_id,
        "aigc_label": AIGC_LABEL,
        "artifacts": artifacts,
    }

    # Write manifest — confined to run_dir (production: always under runs/<id>/).
    manifest_path = run_dir / "manifest.yaml"
    write_artifact(
        manifest_path,
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
    )

    return manifest
