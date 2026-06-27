from __future__ import annotations
import hashlib, unicodedata
from dataclasses import dataclass

ZERO_WIDTH = {"​", "‌", "‍", "﻿", "⁠"}
ALLOWED_CONTROL = {"\n", "\t"}


@dataclass
class SanitizeResult:
    clean_text: str
    original_sha256: str
    clean_sha256: str
    zero_width_stripped: bool
    homoglyph_suspected: bool
    rejected_control_chars: bool


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sanitize(text: str) -> SanitizeResult:
    original = _sha(text)
    zw = any(c in text for c in ZERO_WIDTH)
    text2 = "".join(c for c in text if c not in ZERO_WIDTH)
    rejected = any(
        (unicodedata.category(c).startswith("C") and c not in ALLOWED_CONTROL)
        for c in text2
    )
    text3 = "".join(
        c for c in text2
        if not (unicodedata.category(c).startswith("C") and c not in ALLOWED_CONTROL)
    )
    clean = unicodedata.normalize("NFKC", text3)
    homoglyph = any(unicodedata.normalize("NFKC", c) != c for c in text3)
    return SanitizeResult(clean, original, _sha(clean), zw, homoglyph, rejected)
