"""
Task 2.3 — Policy gate tests.
TDD order: write failing tests first, then implement.
"""
import pytest
from app.policy_gate import validate_run_id, safe_path, source_guard, export_requires_met, load_export_gate


# ── run-id / path confinement ──────────────────────────────────────────────

def test_run_id_accepts_clean():
    assert validate_run_id("demo_clean")


def test_run_id_rejects_traversal():
    assert validate_run_id("demo_clean")
    with pytest.raises(ValueError):
        safe_path("../../etc", "x.yaml")


def test_run_id_rejects_empty():
    with pytest.raises(ValueError):
        validate_run_id("")


def test_run_id_rejects_slash():
    with pytest.raises(ValueError):
        validate_run_id("foo/bar")


def test_safe_path_rejects_dotdot_name():
    with pytest.raises(ValueError):
        safe_path("demo_clean", "../secret.yaml")


def test_safe_path_rejects_slash_name():
    with pytest.raises(ValueError):
        safe_path("demo_clean", "sub/dir.yaml")


# ── source guard ───────────────────────────────────────────────────────────

def test_source_guard_allows_public_domain():
    ok, reasons = source_guard({"source_mode": "public_domain_original", "english_translation_ingested": False})
    assert ok is True and reasons == []


def test_source_guard_blocks_translation_ingested():
    ok, reasons = source_guard({"source_mode": "public_domain_original", "english_translation_ingested": True})
    assert ok is False and any("translation" in r for r in reasons)


def test_source_guard_blocks_non_public_domain():
    ok, reasons = source_guard({"source_mode": "unclear_license", "english_translation_ingested": False})
    assert ok is False and any("source_mode" in r for r in reasons)


def test_source_guard_blocks_both():
    ok, reasons = source_guard({"source_mode": "unclear_license", "english_translation_ingested": True})
    assert ok is False and len(reasons) == 2


# ── export gate helpers ────────────────────────────────────────────────────

def _clean_report(**overrides):
    """All gates satisfied; override individual keys to test blocking."""
    rep = {
        "unsupported_critical_claims": 0,
        "contradicted_claims": 0,
        "unsupported_motivation_claims": 0,
        "invalid_fact_id_claims": 0,
        "prompt_injection_attempts": 0,
        "required_beat_coverage": 1.0,
        "safety_pass": True,
        "workflow_integrity_pass": True,
        "human_approved": True,
        "aigc_label_manifest_bound": True,
        "source_policy_valid": True,
        "source_sanitized": True,
    }
    rep.update(overrides)
    return rep


def test_clean_report_passes():
    ok, missing = export_requires_met(_clean_report())
    assert ok is True and missing == []


def test_export_blocked_until_human_approved():
    ok, missing = export_requires_met(_clean_report(human_approved=False))
    assert ok is False and "human_approved" in missing


def test_injection_blocks_export():  # fix C2 — now gated
    ok, missing = export_requires_met(_clean_report(prompt_injection_attempts=1))
    assert ok is False and "prompt_injection_attempts" in missing


def test_invalid_fact_id_blocks_export():  # fix C3 — now gated
    ok, missing = export_requires_met(_clean_report(invalid_fact_id_claims=1))
    assert ok is False and "invalid_fact_id_claims" in missing


def test_coverage_below_min_blocks_export():
    ok, missing = export_requires_met(_clean_report(required_beat_coverage=0.80))
    assert ok is False and any("required_beat_coverage" in m for m in missing)


def test_unsupported_critical_claims_blocks():
    ok, missing = export_requires_met(_clean_report(unsupported_critical_claims=1))
    assert ok is False and "unsupported_critical_claims" in missing


def test_contradicted_claims_blocks():
    ok, missing = export_requires_met(_clean_report(contradicted_claims=2))
    assert ok is False and "contradicted_claims" in missing


def test_source_policy_invalid_blocks():
    ok, missing = export_requires_met(_clean_report(source_policy_valid=False))
    assert ok is False and "source_policy_valid" in missing


# ── integration: load_export_gate reads real specs/eval_plan.yaml (Contract F) ──

def test_load_export_gate_reads_real_yaml():
    """Contract F — single canonical gate; no hardcoded duplicates."""
    gate = load_export_gate()
    assert "bool_gates" in gate
    assert "zero_count_gates" in gate
    assert "coverage_gate" in gate
    assert "human_approved" in gate["bool_gates"]
    assert "prompt_injection_attempts" in gate["zero_count_gates"]   # fix C2
    assert "invalid_fact_id_claims" in gate["zero_count_gates"]       # fix C3
    cov = gate["coverage_gate"]
    assert cov["metric"] == "required_beat_coverage"
    assert cov["min"] == 0.85


def test_integration_clean_report_against_real_gate():
    """Integration: export_requires_met with real gate from specs/eval_plan.yaml."""
    ok, missing = export_requires_met(_clean_report())
    assert ok is True and missing == []


# ── FIX 3: symlink + empty-name + dots-in-filename ────────────────────────

def test_safe_path_rejects_symlinked_run_dir(tmp_path, monkeypatch):
    """runs/<id> symlink to external dir must raise ValueError (escapes repo)."""
    import app.policy_gate as pg
    fake_root = tmp_path / "repo"
    (fake_root / "runs").mkdir(parents=True)
    external = tmp_path / "external"
    external.mkdir()
    run_id = "run_symlinked"
    (fake_root / "runs" / run_id).symlink_to(external)
    monkeypatch.setattr(pg, "_REPO_ROOT", fake_root)
    with pytest.raises(ValueError):
        pg.safe_path(run_id, "output.yaml")


def test_safe_path_rejects_empty_name():
    """Empty name returns the dir itself — must raise ValueError."""
    with pytest.raises(ValueError):
        safe_path("demo_clean", "")


def test_safe_path_allows_dots_in_filename():
    """Dots INSIDE a filename component (v1..2.yaml) are legal — must NOT raise."""
    result = safe_path("run01", "v1..2.yaml")
    assert result.name == "v1..2.yaml"
