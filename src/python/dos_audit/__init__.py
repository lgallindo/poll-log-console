"""dos_audit — Python helpers for the DOS audit console log feed."""

from __future__ import annotations

from pathlib import Path

from .buffer import LogBuffer
from .schema import LogEntry

__all__ = ["LogBuffer", "LogEntry", "static_dir", "dist_dir"]


def package_root() -> Path:
    # dos_audit/ -> python/ -> src/ -> repo root
    return Path(__file__).resolve().parents[3]


def dist_dir() -> Path:
    """Prefer repo dist/; fall back to package-adjacent static if vendored."""
    d = package_root() / "dist"
    if d.is_dir():
        return d
    return Path(__file__).resolve().parent / "static"


def static_dir() -> Path:
    return dist_dir()
