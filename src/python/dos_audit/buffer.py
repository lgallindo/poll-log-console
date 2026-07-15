from __future__ import annotations

from collections import deque
from typing import Any, Iterable


class LogBuffer:
    """Thread-unsafe ring buffer (same shape as philological lab.state.LOG_BUFFER)."""

    def __init__(self, maxlen: int = 50) -> None:
        self._buf: deque[dict[str, Any]] = deque(maxlen=maxlen)

    def append(self, entry: dict[str, Any]) -> None:
        self._buf.append(entry)

    def extend(self, entries: Iterable[dict[str, Any]]) -> None:
        for e in entries:
            self.append(e)

    def list(self) -> list[dict[str, Any]]:
        return list(self._buf)

    def clear(self) -> None:
        self._buf.clear()

    def __len__(self) -> int:
        return len(self._buf)
