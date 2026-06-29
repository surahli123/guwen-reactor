"""Task 4b.5 — end-to-end CLI test (the non-cuttable DoD).

Runs the real CLI on tmp copies of the committed fixtures (so the fixtures are never
dirtied): demo_clean --approve exports a manifest; demo_drift is BLOCKED with no export;
demo_clean without --approve halts at READY_FOR_APPROVAL."""
import pathlib
import shutil

from typer.testing import CliRunner

from app.cli import app

runner = CliRunner()


def _copy(tmp_path, name):
    dst = tmp_path / name
    shutil.copytree(pathlib.Path("runs") / name, dst)
    return dst


def test_clean_run_exports(tmp_path):
    dst = _copy(tmp_path, "demo_clean")
    res = runner.invoke(app, ["run", str(dst), "--approve"])
    assert res.exit_code == 0, res.stdout
    assert "EXPORTED" in res.stdout
    assert (dst / "manifest.yaml").exists()


def test_drift_run_is_blocked(tmp_path):
    dst = _copy(tmp_path, "demo_drift")
    res = runner.invoke(app, ["run", str(dst)])
    assert res.exit_code == 1
    assert "BLOCKED" in res.stdout
    assert not (dst / "manifest.yaml").exists()      # a blocked run must never export


def test_clean_without_approve_does_not_export(tmp_path):
    dst = _copy(tmp_path, "demo_clean")
    res = runner.invoke(app, ["run", str(dst)])
    assert res.exit_code == 0
    assert "READY_FOR_APPROVAL" in res.stdout
    assert not (dst / "manifest.yaml").exists()
