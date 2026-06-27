"""
guwen_core/artifact_store.py — Low-level artifact writer with sha256 integrity.

write_artifact writes text data to a path (creating parent dirs as needed) and
returns the sha256 hex digest of the written content.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


def write_artifact(path: Path, data: str) -> str:
    """
    Write data to path, creating parent directories as needed.
    Returns the sha256 hex digest of the UTF-8-encoded content.

    Path must already be validated (safe_path) before calling this.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
