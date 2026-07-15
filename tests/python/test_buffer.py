"""Unit tests for LogBuffer."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "python"))

from dos_audit.buffer import LogBuffer


def test_ring_maxlen():
    b = LogBuffer(maxlen=3)
    for i in range(5):
        b.append({"time": str(i), "msg": f"m{i}", "type": "sys"})
    assert len(b) == 3
    assert b.list()[0]["msg"] == "m2"


def test_clear():
    b = LogBuffer()
    b.append({"time": "1", "msg": "x", "type": "sys"})
    b.clear()
    assert b.list() == []
