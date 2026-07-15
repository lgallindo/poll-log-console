from __future__ import annotations

from typing import Any, TypedDict


class LogEntry(TypedDict, total=False):
    time: str
    msg: str
    type: str  # req | res | sys | err
    id: str
    seq: int
    level: str


def make_entry(time: str, msg: str, type: str = "sys", **extra: Any) -> dict[str, Any]:
    entry: dict[str, Any] = {"time": time, "msg": msg, "type": type}
    entry.update(extra)
    return entry
