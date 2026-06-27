from guwen_core.source_sanitizer import sanitize


def test_strips_zero_width_and_preserves_hashes():
    dirty = "管寧​割席﻿"          # zero-width space + BOM
    r = sanitize(dirty)
    assert "​" not in r.clean_text and "﻿" not in r.clean_text
    assert r.zero_width_stripped is True
    assert r.original_sha256 != r.clean_sha256


def test_rejects_control_chars_except_newline_tab():
    r = sanitize("ok\x07bad")              # bell char
    assert "\x07" not in r.clean_text
    assert r.rejected_control_chars is True
