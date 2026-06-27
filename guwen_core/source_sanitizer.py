from __future__ import annotations
import hashlib, unicodedata
from dataclasses import dataclass

ZERO_WIDTH = {"​", "‌", "‍", "﻿", "⁠"}
ALLOWED_CONTROL = {"\n", "\t"}


def _is_variation_selector(c: str) -> bool:
    """Return True for chars in Variation Selector ranges U+FE00-FE0F and
    U+E0100-E01EF (Mn category). These are not caught by the Cf/Cc strip and
    enable steganographic payloads invisible to the judge."""
    o = ord(c)
    return (0xFE00 <= o <= 0xFE0F) or (0xE0100 <= o <= 0xE01EF)


def _mixed_script_confusables(text: str) -> bool:
    """Advisory heuristic: return True iff the text's letters include characters
    from >=2 of {Latin, Greek, Cyrillic}. Han/Kana and other scripts are
    deliberately excluded so Chinese-source + Latin fact text does NOT trigger
    this flag. This is NOT exhaustive confusables detection — treat as an
    advisory signal only; the export gate does not consume it."""
    scripts: set[str] = set()
    for c in text:
        if not c.isalpha():
            continue
        o = ord(c)
        # Latin Basic (A-Z, a-z) + Latin-1 Supplement + Latin Extended-A/B
        if (0x0041 <= o <= 0x005A) or (0x0061 <= o <= 0x007A) or (0x00C0 <= o <= 0x024F):
            scripts.add("Latin")
        elif 0x0370 <= o <= 0x03FF:  # Greek and Coptic block
            scripts.add("Greek")
        elif 0x0400 <= o <= 0x04FF:  # Cyrillic block
            scripts.add("Cyrillic")
    return len(scripts & {"Latin", "Greek", "Cyrillic"}) >= 2


@dataclass
class SanitizeResult:
    clean_text: str
    original_sha256: str
    clean_sha256: str
    zero_width_stripped: bool
    homoglyph_suspected: bool
    rejected_control_chars: bool
    variation_selectors_stripped: bool


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sanitize(text: str) -> SanitizeResult:
    original = _sha(text)
    zw = any(c in text for c in ZERO_WIDTH)
    text2 = "".join(c for c in text if c not in ZERO_WIDTH)
    # Strip Mn variation selectors (U+FE00-FE0F, U+E0100-E01EF) — not caught
    # by the Cf/Cc category filter below; enable invisible-payload steganography.
    vs = any(_is_variation_selector(c) for c in text2)
    text2 = "".join(c for c in text2 if not _is_variation_selector(c))
    rejected = any(
        (unicodedata.category(c).startswith("C") and c not in ALLOWED_CONTROL)
        for c in text2
    )
    text3 = "".join(
        c for c in text2
        if not (unicodedata.category(c).startswith("C") and c not in ALLOWED_CONTROL)
    )
    clean = unicodedata.normalize("NFKC", text3)
    homoglyph = _mixed_script_confusables(clean)
    return SanitizeResult(clean, original, _sha(clean), zw, homoglyph, rejected, vs)
