"""Task 5.2 — Cached run canvas renderer.

Generates docs/demo/index.html — a fully self-contained static demo page showing
the deterministic faithfulness gate in action for G01 管寧割席 (Guan Ning Cuts the Mat).

Usage:
    from app.render_canvas import render
    render()                            # writes docs/demo/index.html
    render(out_path="some/other.html")  # relative → resolved from repo root
    render(out_path=Path("/tmp/x.html"))  # absolute path used as-is

SELF-CONTAINMENT CONSTRAINT (verified by evals/test_canvas.py):
  - All CSS is in an inline <style> block.
  - No external resources: no http/https URLs, no src= attributes, no CDN, no fetch(),
    no <script src, no @import url(), no <link href= pulling external assets.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from evals.run_eval_suite import evaluate_run

_REPO_ROOT = Path(__file__).parent.parent

# Gates produced at approval/export time — not content gates, never block.
_APPROVAL_GATES = {"human_approved", "aigc_label_manifest_bound"}

# Beat colour tokens — applied consistently to source chunks, panels, and claim rows.
_BEAT_COLORS: dict[str, dict[str, str]] = {
    "B01": {"bg": "#EFF6FF", "border": "#2563EB", "text": "#1D4ED8"},
    "B02": {"bg": "#F5F3FF", "border": "#7C3AED", "text": "#6D28D9"},
    "B03": {"bg": "#FFF1F2", "border": "#BE123C", "text": "#9F1239"},
}

# Map source chunks to beats (G01-specific, fixed by the source structure).
_CHUNK_BEAT: dict[str, str] = {"C01": "B01", "C02": "B02", "C03": "B03"}

# Visual metadata for each claim label.
_LABEL_META: dict[str, dict[str, str]] = {
    "SUPPORTED": {
        "bg": "#F0FDF4", "border": "#16A34A", "text": "#15803D", "icon": "✓",
    },
    "VALID_HEDGED_INTERPRETATION": {
        "bg": "#ECFDF5", "border": "#059669", "text": "#065F46", "icon": "✓ hedged",
    },
    "UNSUPPORTED_MOTIVATION": {
        "bg": "#FFF1F2", "border": "#E11D48", "text": "#BE123C", "icon": "✗",
    },
    "UNSUPPORTED_DETAIL": {
        "bg": "#FFF1F2", "border": "#E11D48", "text": "#BE123C", "icon": "✗",
    },
    "CONTRADICTED": {
        "bg": "#FFF1F2", "border": "#E11D48", "text": "#BE123C", "icon": "✗",
    },
    "INVALID_FACT_ID": {
        "bg": "#FFF1F2", "border": "#E11D48", "text": "#BE123C", "icon": "✗",
    },
    "PROMPT_INJECTION_ATTEMPT": {
        "bg": "#FFF1F2", "border": "#E11D48", "text": "#BE123C", "icon": "✗",
    },
    "CREATIVE_SAFE_FILLER": {
        "bg": "#F9FAFB", "border": "#D1D5DB", "text": "#6B7280", "icon": "~",
    },
}

_DEFAULT_LABEL_META = {"bg": "#F9FAFB", "border": "#D1D5DB", "text": "#6B7280", "icon": "~"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _esc(s: str) -> str:
    """Minimal HTML entity escaping."""
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _zip_labels(claims: list[dict], labels: list[str]) -> list[dict]:
    """Attach an eval label to each claim dict."""
    return [
        {**c, "label": labels[i] if i < len(labels) else "AMBIGUOUS_REVIEW"}
        for i, c in enumerate(claims)
    ]


def _content_missing(rep: dict) -> list[str]:
    """Return gate keys that are missing and are NOT approval-only gates."""
    return [m for m in rep.get("missing", []) if m.split(">=")[0] not in _APPROVAL_GATES]


# ---------------------------------------------------------------------------
# HTML fragment builders
# ---------------------------------------------------------------------------

def _source_chunk_html(chunk: dict) -> str:
    cid: str = chunk["chunk_id"]
    beat_id = _CHUNK_BEAT.get(cid, "B01")
    bc = _BEAT_COLORS[beat_id]
    return f"""
        <div class="source-chunk" style="background:{bc['bg']};border-left:4px solid {bc['border']};">
            <div class="chunk-header">
                <span class="mono-tag">{_esc(cid)}</span>
                <span class="beat-pill" style="background:{bc['border']};">{_esc(beat_id)}</span>
            </div>
            <p class="zh-text">{_esc(chunk['text_zh'])}</p>
        </div>"""


def _panel_html(panel: dict) -> str:
    bid = panel.get("beat_id", "")
    bc = _BEAT_COLORS.get(bid, {"bg": "#F9FAFB", "border": "#9CA3AF", "text": "#6B7280"})
    return f"""
            <div class="panel-card" style="border-left:3px solid {bc['border']};">
                <div class="panel-header">
                    <span class="mono-tag dim">{_esc(panel['id'])}</span>
                    <span class="beat-pill" style="background:{bc['border']};">{_esc(bid)}</span>
                </div>
                <p class="panel-caption">{_esc(panel['caption_en'])}</p>
            </div>"""


def _claim_row_html(claim: dict) -> str:
    label: str = claim.get("label", "AMBIGUOUS_REVIEW")
    meta = _LABEL_META.get(label, _DEFAULT_LABEL_META)
    is_bad = label not in ("SUPPORTED", "VALID_HEDGED_INTERPRETATION", "CREATIVE_SAFE_FILLER")
    bid = claim.get("beat_id") or "—"
    cid = _esc(claim.get("claim_id", ""))
    atype = _esc(claim.get("assertion_type", ""))
    hedge = _esc(claim.get("hedging", ""))
    facts = _esc(", ".join(str(f) for f in claim.get("source_fact_ids", [])))
    text = _esc(str(claim.get("claim_text", "")))
    label_esc = _esc(label)
    icon_esc = _esc(meta["icon"])

    row_extra = (
        f'style="background:{meta["bg"]};border-left:3px solid {meta["border"]};"'
        if is_bad else ""
    )
    badge_style = (
        f'style="background:{meta["bg"]};color:{meta["text"]};'
        f'border:1px solid {meta["border"]};"'
    )
    return f"""
            <div class="claim-row" {row_extra}>
                <div class="claim-meta-row">
                    <span class="mono-tag">{cid}</span>
                    <span class="meta-pill">beat:{_esc(str(bid))}</span>
                    <span class="meta-pill">type:{atype}</span>
                    <span class="meta-pill">hedging:{hedge}</span>
                    <span class="meta-pill facts-tag">facts:{facts}</span>
                </div>
                <p class="claim-text">{text}</p>
                <span class="label-badge" {badge_style}>{icon_esc}&nbsp;{label_esc}</span>
            </div>"""


def _gate_rows_html(rep: dict) -> str:
    """Build the per-gate checklist rows for one run."""
    cm = _content_missing(rep)

    def _is_missing(key: str) -> bool:
        # Match exact key OR coverage-gate key (e.g. "required_beat_coverage" in "required_beat_coverage>=0.85")
        return any(key == m or key == m.split(">=")[0] for m in cm)

    rows = [
        ("unsupported_critical_claims",   str(rep.get("unsupported_critical_claims", "?")), "== 0"),
        ("contradicted_claims",           str(rep.get("contradicted_claims", "?")),          "== 0"),
        ("unsupported_motivation_claims", str(rep.get("unsupported_motivation_claims", "?")), "== 0"),
        ("invalid_fact_id_claims",        str(rep.get("invalid_fact_id_claims", "?")),        "== 0"),
        ("prompt_injection_attempts",     str(rep.get("prompt_injection_attempts", "?")),      "== 0"),
        ("required_beat_coverage",        rep.get("coverage_fraction", "?"),                  ">= 0.85"),
        ("safety_pass",                   str(rep.get("safety_pass", False)),                  "= true"),
    ]

    parts: list[str] = []
    for key, val, req in rows:
        missing = _is_missing(key)
        row_bg = "#FFF1F2" if missing else "#F0FDF4"
        icon_color = "#BE123C" if missing else "#15803D"
        icon = "✗" if missing else "✓"
        parts.append(f"""
            <div class="gate-row" style="background:{row_bg};">
                <span class="gate-icon" style="color:{icon_color};">{icon}</span>
                <span class="gate-key">{_esc(key)}</span>
                <span class="gate-val">{_esc(val)}</span>
                <span class="gate-req">{_esc(req)}</span>
            </div>""")
    return "".join(parts)


def _missing_block_html(rep: dict) -> str:
    """Red call-out box listing the content gates that block export."""
    cm = _content_missing(rep)
    if not cm:
        return ""
    items = "".join(f"<li><code>{_esc(m)}</code></li>" for m in cm)
    return f"""
            <div class="missing-block">
                <div class="missing-label">Content gates not met — export BLOCKED</div>
                <ul class="missing-list">{items}</ul>
            </div>"""


def _run_card_html(
    run_label: str,
    run_subtitle: str,
    rep: dict,
    labeled_claims: list[dict],
) -> str:
    status = rep.get("export_status", "UNKNOWN")
    is_blocked = status == "BLOCKED"
    status_bg = "#FFF1F2" if is_blocked else "#F0FDF4"
    status_border = "#E11D48" if is_blocked else "#16A34A"
    status_text = "#BE123C" if is_blocked else "#15803D"

    cov = _esc(rep.get("coverage_fraction", "?"))
    prec = _esc(rep.get("factual_precision", "?"))
    gate_rows = _gate_rows_html(rep)
    missing = _missing_block_html(rep)
    claims_html = "".join(_claim_row_html(c) for c in labeled_claims)
    n = len(labeled_claims)

    return f"""
        <div class="run-card">
            <div class="run-card-header">
                <span class="run-id-label">{_esc(run_label)}</span>
                <span class="run-subtitle">{_esc(run_subtitle)}</span>
            </div>

            <div class="status-badge"
                 style="background:{status_bg};border:2px solid {status_border};color:{status_text};">
                {_esc(status)}
            </div>

            <div class="coverage-line">
                Beat coverage: <strong>{cov}</strong>
                &nbsp;&middot;&nbsp;
                Factual precision: <strong>{prec}</strong>
            </div>

            <div class="gate-grid-rows">{gate_rows}</div>

            {missing}

            <div class="claims-heading">Claims ({n})</div>
            <div class="claims-list">{claims_html}</div>
        </div>"""


# ---------------------------------------------------------------------------
# CSS (fully inline — no @import, no url() calls, no external fonts)
# ---------------------------------------------------------------------------

def _css() -> str:
    return """
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
        --bg:             #F8F9FA;
        --surface:        #FFFFFF;
        --border:         #E5E7EB;
        --text-primary:   #111827;
        --text-secondary: #6B7280;
        --text-muted:     #9CA3AF;
        --accent-red:     #991B1B;
        --mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
        --serif: Georgia, "Times New Roman", serif;
        --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    }

    body {
        font-family: var(--sans);
        background: var(--bg);
        color: var(--text-primary);
        line-height: 1.6;
        font-size: 15px;
    }

    .container {
        max-width: 980px;
        margin: 0 auto;
        padding: 0 28px;
    }

    /* ---- Header ---- */
    header {
        background: #0F172A;
        color: #F1F5F9;
        padding: 52px 0 44px;
        border-bottom: 4px solid var(--accent-red);
    }

    .project-label {
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #64748B;
        margin-bottom: 20px;
    }

    .scene-zh {
        font-family: var(--serif);
        font-size: 52px;
        font-weight: 400;
        letter-spacing: 0.14em;
        color: #F1F5F9;
        line-height: 1.2;
        margin-bottom: 10px;
    }

    .scene-en {
        font-size: 22px;
        font-weight: 300;
        color: #94A3B8;
        margin-bottom: 18px;
        letter-spacing: 0.01em;
    }

    .source-ref {
        font-size: 13px;
        color: #475569;
        font-style: italic;
    }

    /* ---- Sections ---- */
    .section {
        padding: 52px 0;
        border-bottom: 1px solid var(--border);
    }

    .section-eyebrow {
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 6px;
    }

    .section-title {
        font-family: var(--serif);
        font-size: 26px;
        font-weight: 400;
        color: var(--text-primary);
        margin-bottom: 28px;
    }

    /* ---- Source chunks ---- */
    .source-chunks { display: grid; gap: 12px; }

    .source-chunk {
        padding: 16px 20px;
        border-radius: 6px;
    }

    .chunk-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }

    .zh-text {
        font-family: var(--serif);
        font-size: 20px;
        letter-spacing: 0.06em;
        line-height: 1.75;
        color: var(--text-primary);
    }

    /* ---- Shared pill/tag styles ---- */
    .mono-tag {
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 700;
        color: var(--text-secondary);
    }

    .mono-tag.dim { color: var(--text-muted); font-weight: 400; }

    .beat-pill {
        font-family: var(--mono);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.06em;
        padding: 2px 7px;
        border-radius: 3px;
        color: #FFFFFF;
    }

    .meta-pill {
        font-family: var(--mono);
        font-size: 10px;
        color: var(--text-muted);
        background: #F3F4F6;
        padding: 1px 5px;
        border-radius: 3px;
    }

    .facts-tag { color: #6B7280; }

    /* ---- Storyboard ---- */
    .beat-group { margin-bottom: 32px; }

    .beat-group-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border);
    }

    .beat-group-id {
        font-family: var(--mono);
        font-size: 12px;
        font-weight: 700;
    }

    .beat-group-desc {
        font-size: 13px;
        color: var(--text-secondary);
        font-style: italic;
    }

    .panels-grid { display: grid; gap: 8px; }

    .panel-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 12px 16px;
    }

    .panel-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    .panel-caption {
        font-size: 14px;
        color: var(--text-primary);
        line-height: 1.55;
    }

    .cultural-note {
        background: #FFFBEB;
        border: 1px solid #FCD34D;
        border-left: 4px solid #F59E0B;
        border-radius: 4px;
        padding: 14px 18px;
        margin-top: 16px;
    }

    .cultural-note-label {
        font-family: var(--mono);
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #92400E;
        display: block;
        margin-bottom: 6px;
    }

    .cultural-note-text {
        font-size: 14px;
        color: #78350F;
        font-style: italic;
        line-height: 1.55;
    }

    /* ---- Gate section ---- */
    .gate-explanation {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 4px solid #0284C7;
        border-radius: 6px;
        padding: 18px 22px;
        margin-bottom: 32px;
        font-size: 14px;
        color: #0C4A6E;
        line-height: 1.7;
    }

    .gate-explanation strong { font-weight: 600; }

    .gate-columns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px;
    }

    @media (max-width: 720px) {
        .gate-columns { grid-template-columns: 1fr; }
    }

    /* ---- Run card ---- */
    .run-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 22px;
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .run-card-header {
        display: flex;
        align-items: baseline;
        gap: 10px;
        padding-bottom: 14px;
        margin-bottom: 14px;
        border-bottom: 1px solid var(--border);
    }

    .run-id-label {
        font-family: var(--mono);
        font-size: 14px;
        font-weight: 700;
        color: var(--text-primary);
    }

    .run-subtitle {
        font-size: 12px;
        color: var(--text-secondary);
    }

    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 6px;
        font-family: var(--mono);
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 12px;
        align-self: flex-start;
    }

    .coverage-line {
        font-size: 13px;
        color: var(--text-secondary);
        margin-bottom: 14px;
    }

    .coverage-line strong { color: var(--text-primary); }

    /* ---- Gate checklist rows ---- */
    .gate-grid-rows { display: grid; gap: 4px; margin-bottom: 12px; }

    .gate-row {
        display: grid;
        grid-template-columns: 20px 1fr auto auto;
        align-items: center;
        gap: 6px;
        padding: 5px 8px;
        border-radius: 3px;
        font-size: 12px;
    }

    .gate-icon { font-weight: 700; text-align: center; font-size: 13px; }

    .gate-key {
        font-family: var(--mono);
        font-size: 11px;
        color: var(--text-secondary);
        word-break: break-all;
    }

    .gate-val {
        font-family: var(--mono);
        font-size: 12px;
        font-weight: 600;
        color: var(--text-primary);
        white-space: nowrap;
        text-align: right;
        padding: 0 4px;
    }

    .gate-req {
        font-family: var(--mono);
        font-size: 11px;
        color: var(--text-muted);
        white-space: nowrap;
    }

    /* ---- Missing block ---- */
    .missing-block {
        background: #FFF1F2;
        border: 1px solid #FECDD3;
        border-radius: 5px;
        padding: 12px 16px;
        margin-bottom: 14px;
    }

    .missing-label {
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #BE123C;
        margin-bottom: 8px;
    }

    .missing-list { list-style: none; display: grid; gap: 4px; }

    .missing-list li {
        font-size: 12px;
        color: #9F1239;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .missing-list li::before { content: "✗"; color: #E11D48; font-weight: 700; }

    code {
        font-family: var(--mono);
        font-size: 11px;
        background: #FEE2E2;
        padding: 1px 5px;
        border-radius: 2px;
        color: #BE123C;
    }

    /* ---- Claims list ---- */
    .claims-heading {
        font-family: var(--mono);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        margin-bottom: 8px;
        margin-top: 16px;
    }

    .claims-list { display: grid; gap: 6px; }

    .claim-row {
        background: #F9FAFB;
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 10px 12px;
    }

    .claim-meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-bottom: 5px;
    }

    .claim-text {
        font-size: 13px;
        color: var(--text-primary);
        line-height: 1.5;
        margin-bottom: 7px;
    }

    .label-badge {
        display: inline-block;
        font-family: var(--mono);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.04em;
        padding: 2px 8px;
        border-radius: 3px;
    }

    /* ---- Footer ---- */
    footer {
        background: #0F172A;
        color: #475569;
        padding: 36px 0;
        text-align: center;
    }

    .aigc-label {
        font-size: 13px;
        color: #94A3B8;
        letter-spacing: 0.01em;
        margin-bottom: 10px;
    }

    .footer-meta {
        font-family: var(--mono);
        font-size: 11px;
        color: #334155;
    }
    """


# ---------------------------------------------------------------------------
# Top-level render function
# ---------------------------------------------------------------------------

def render(out_path: "str | Path" = "docs/demo/index.html") -> Path:
    """Render the cached run canvas to a self-contained HTML file.

    Args:
        out_path: Destination path. Relative paths are resolved from the repo root.
                  Default: docs/demo/index.html.

    Returns:
        The resolved absolute Path of the written file.
    """
    p = Path(out_path)
    if not p.is_absolute():
        p = _REPO_ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)

    # --- Eval results (the authoritative data source) ---
    clean_rep = evaluate_run(_REPO_ROOT / "runs" / "demo_clean")
    drift_rep = evaluate_run(_REPO_ROOT / "runs" / "demo_drift")

    # --- Fixture data ---
    adapt = _load_yaml(_REPO_ROOT / "runs" / "demo_clean" / "adaptation.yaml")
    clean_claims_doc = _load_yaml(_REPO_ROOT / "runs" / "demo_clean" / "structured_claims.yaml")
    drift_claims_doc = _load_yaml(_REPO_ROOT / "runs" / "demo_drift" / "structured_claims.yaml")
    gold_doc = _load_yaml(_REPO_ROOT / "data" / "gold" / "canon_gold.yaml")

    # --- Extract G01 scene from gold ---
    scenes = gold_doc.get("scenes", [])
    scene_g01 = next(s for s in scenes if s["scene_id"] == "G01")
    source_chunks: list[dict] = scene_g01["source_chunks"]
    required_beats: dict[str, dict] = {
        b["beat_id"]: b for b in scene_g01["required_beats"]
    }

    # --- Storyboard + AIGC label ---
    panels: list[dict] = adapt["storyboard"]["panels"]
    cultural_note: str = adapt.get("cultural_decoder", {}).get("note_en", "")
    aigc_label: str = adapt.get(
        "aigc_label",
        "AI-generated adaptation. No existing English translation was provided to the generator.",
    )

    # --- Labeled claims ---
    clean_labeled = _zip_labels(
        clean_claims_doc.get("claims", []), clean_rep["labels"]
    )
    drift_labeled = _zip_labels(
        drift_claims_doc.get("claims", []), drift_rep["labels"]
    )

    # --- Build HTML fragments ---

    # Source chunks
    chunks_html = "".join(_source_chunk_html(c) for c in source_chunks)

    # Storyboard — grouped by beat, in order B01 → B02 → B03
    storyboard_parts: list[str] = []
    for bid in ("B01", "B02", "B03"):
        beat_panels = [p for p in panels if p.get("beat_id") == bid]
        if not beat_panels:
            continue
        bc = _BEAT_COLORS.get(bid, {"bg": "#F9FAFB", "border": "#9CA3AF", "text": "#6B7280"})
        desc = required_beats.get(bid, {}).get("description", "")
        panels_html = "".join(_panel_html(p) for p in beat_panels)
        storyboard_parts.append(f"""
        <div class="beat-group">
            <div class="beat-group-header">
                <span class="beat-group-id" style="color:{bc['text']};">{_esc(bid)}</span>
                <span class="beat-group-desc">{_esc(desc)}</span>
            </div>
            <div class="panels-grid">{panels_html}</div>
        </div>""")

    cultural_html = ""
    if cultural_note:
        cultural_html = f"""
        <div class="cultural-note">
            <span class="cultural-note-label">Cultural decoder (advisory)</span>
            <p class="cultural-note-text">{_esc(cultural_note)}</p>
        </div>"""

    storyboard_html = "".join(storyboard_parts) + cultural_html

    # Gate comparison cards
    clean_card = _run_card_html("demo_clean", "faithful adaptation", clean_rep, clean_labeled)
    drift_card = _run_card_html("demo_drift", "planted fabrication", drift_rep, drift_labeled)

    # --- Assemble full page ---
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Guwen Reactor &mdash; Gate Demo: 管寧割席 (Guan Ning Cuts the Mat)</title>
<style>
{_css()}
</style>
</head>
<body>

<header>
<div class="container">
    <div class="project-label">Guwen Reactor &nbsp;&middot;&nbsp; Faithfulness Gate Demo</div>
    <h1 class="scene-zh">管寧割席</h1>
    <p class="scene-en">Guan Ning Cuts the Mat</p>
    <p class="source-ref">
        Source: 《世說新語&middot;德行》 &mdash; <em>Shishuo Xinyu: Virtuous Conduct</em>
        &nbsp;&middot;&nbsp; Scene G01
    </p>
</div>
</header>

<section class="section">
<div class="container">
    <div class="section-eyebrow">Source text</div>
    <h2 class="section-title">Original Classical Chinese &mdash; Three Source Chunks</h2>
    <div class="source-chunks">
{chunks_html}
    </div>
</div>
</section>

<section class="section">
<div class="container">
    <div class="section-eyebrow">English storyboard &nbsp;&middot;&nbsp; run: demo_clean</div>
    <h2 class="section-title">Adaptation Panels &mdash; Beat by Beat</h2>
    {storyboard_html}
</div>
</section>

<section class="section">
<div class="container">
    <div class="section-eyebrow">The wow</div>
    <h2 class="section-title">Faithfulness Gate &mdash; Faithful vs. Fabricated, Side by Side</h2>

    <div class="gate-explanation">
        <strong>This gate is deterministic &mdash; not an LLM vibe-check.</strong>
        It audits the declared structure of every StructuredClaim (assertion_type, hedging field,
        source_fact_ids, beat alignment) against the locked canon gold. No keyword matching.
        No semantic similarity. Semantic entailment is advisory only and never blocks export.
        <br><br>
        <strong>Accepts:</strong> the clean run, where every plot claim is structurally grounded
        and the one interpretive claim is properly hedged &rarr;
        <strong>READY_FOR_APPROVAL</strong>, coverage 3/3, all claims green.
        &nbsp;&nbsp;
        <strong>Rejects:</strong> the drift run, which plants a motive claim asserted as fact
        (assertion_type=motive, hedging=asserted) &rarr;
        <strong>BLOCKED</strong>, content gate failed, export prevented.
    </div>

    <div class="gate-columns">
        {clean_card}
        {drift_card}
    </div>
</div>
</section>

<footer>
<div class="container">
    <p class="aigc-label">{_esc(aigc_label)}</p>
    <p class="footer-meta">
        Guwen Reactor &nbsp;&middot;&nbsp; Kaggle Vibe-Coding Capstone 2026
        &nbsp;&middot;&nbsp; Gate defined in specs/eval_plan.yaml (Contract F)
    </p>
</div>
</footer>

</body>
</html>"""

    p.write_text(html, encoding="utf-8")
    return p
