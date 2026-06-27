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


def test_strips_variation_selectors():
    # VS16 (U+FE0F, Mn) and VS-257 (U+E0100, Mn) survive the Cf strip;
    # they must be explicitly stripped to block steganographic payloads.
    r = sanitize("A️\U000E0100")
    assert "️" not in r.clean_text
    assert "\U000E0100" not in r.clean_text
    assert r.variation_selectors_stripped is True


def test_homoglyph_flags_mixed_latin_cyrillic():
    # Cyrillic CAPITAL LETTER A (U+0410) alongside Latin letters → mixed-script → True
    r = sanitize("Аdmin")  # Cyrillic А + Latin 'dmin'
    assert r.homoglyph_suspected is True


def test_homoglyph_pure_latin_false():
    r = sanitize("Guan Ning")
    assert r.homoglyph_suspected is False


def test_homoglyph_han_plus_latin_false():
    # Han script not in the {Latin, Greek, Cyrillic} trio → no false positive
    r = sanitize("管寧 Guan")
    assert r.homoglyph_suspected is False
