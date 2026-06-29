"""Task 5.2 — TDD: D5 automated no-network check for the static demo page.

Two test classes:
  TestNoExternalRefs  — zero external references in the rendered HTML (the D5 gate).
  TestContent         — key content present (scene title, gate verdicts, AIGC label).

Render is module-scoped so the file is produced once per pytest session.
"""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

import pytest

from app.render_canvas import render


# ---------------------------------------------------------------------------
# Shared fixture — render once, share across all tests
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def rendered_html() -> str:
    """Render the canvas to a temp file and return the full HTML string."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir) / "test_index.html"
        render(out_path=out)
        return out.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# D5: No external references
# ---------------------------------------------------------------------------

class TestNoExternalRefs:
    """Every test in this class is a D5 gate check.

    The rendered page MUST be fully self-contained: a browser with no network
    access must render it identically to one with full access.
    """

    def test_no_http_urls(self, rendered_html: str) -> None:
        assert "http://" not in rendered_html, (
            "Found http:// reference — page is not self-contained."
        )

    def test_no_https_urls(self, rendered_html: str) -> None:
        assert "https://" not in rendered_html, (
            "Found https:// reference — page is not self-contained."
        )

    def test_no_src_attribute(self, rendered_html: str) -> None:
        """No src= attributes of any kind (<img src=, <script src=, etc.)."""
        assert "src=" not in rendered_html, (
            "Found src= attribute — remove all <img>, <iframe>, and external <script> tags."
        )

    def test_no_cdn_reference(self, rendered_html: str) -> None:
        assert "cdn" not in rendered_html.lower(), (
            "Found 'cdn' in output — no CDN references allowed."
        )

    def test_no_fetch_call(self, rendered_html: str) -> None:
        assert "fetch(" not in rendered_html, (
            "Found fetch() — no runtime network calls allowed."
        )

    def test_no_external_script_src_tag(self, rendered_html: str) -> None:
        assert "<script src" not in rendered_html, (
            "Found <script src — all scripts must be inline."
        )

    def test_no_at_import_url(self, rendered_html: str) -> None:
        assert "@import url(" not in rendered_html, (
            "Found @import url() — no external stylesheet imports allowed."
        )

    def test_no_external_link_href(self, rendered_html: str) -> None:
        """No <link href=...> tags that would pull external assets."""
        matches = re.findall(r"<link\b[^>]+\bhref\s*=", rendered_html, re.IGNORECASE)
        assert len(matches) == 0, (
            f"Found <link href= tag(s): {matches} — use inline <style> only."
        )

    def test_css_is_inline(self, rendered_html: str) -> None:
        """All styling must live in an inline <style> block."""
        has_style = bool(
            re.search(r"<style[\s>]", rendered_html, re.IGNORECASE)
        )
        assert has_style, "No inline <style> block found — CSS must be inline."


# ---------------------------------------------------------------------------
# Content: the page tells the story
# ---------------------------------------------------------------------------

class TestContent:
    """Key content must be present so the demo page actually tells the story."""

    def test_scene_title_chinese(self, rendered_html: str) -> None:
        assert "管寧割席" in rendered_html, "Chinese scene title missing."

    def test_scene_title_english(self, rendered_html: str) -> None:
        assert "Guan Ning" in rendered_html, "English scene title missing."

    def test_source_chunk_c01_chinese(self, rendered_html: str) -> None:
        # C01 text starts with 管寧、華歆
        assert "管寧" in rendered_html, "C01 source chunk (Chinese) missing."

    def test_source_chunk_c03_chinese(self, rendered_html: str) -> None:
        # C03 text contains 割席
        assert "割席" in rendered_html, "C03 source chunk (Chinese) missing."

    def test_ready_for_approval_verdict(self, rendered_html: str) -> None:
        assert "READY_FOR_APPROVAL" in rendered_html, (
            "READY_FOR_APPROVAL export status missing — clean run verdict not shown."
        )

    def test_blocked_verdict(self, rendered_html: str) -> None:
        assert "BLOCKED" in rendered_html, (
            "BLOCKED export status missing — drift run verdict not shown."
        )

    def test_aigc_label(self, rendered_html: str) -> None:
        assert (
            "No existing English translation was provided to the generator"
            in rendered_html
        ), "AIGC label missing from page."

    def test_deterministic_gate_caption(self, rendered_html: str) -> None:
        assert "deterministic" in rendered_html.lower(), (
            "Gate explanation caption missing 'deterministic' — must clarify this is not an LLM vibe-check."
        )

    def test_both_run_ids_shown(self, rendered_html: str) -> None:
        assert "demo_clean" in rendered_html, "demo_clean run label missing."
        assert "demo_drift" in rendered_html, "demo_drift run label missing."

    def test_beat_ids_shown(self, rendered_html: str) -> None:
        for bid in ("B01", "B02", "B03"):
            assert bid in rendered_html, f"Beat {bid} not shown in page."
