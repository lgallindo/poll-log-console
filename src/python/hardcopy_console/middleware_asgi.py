from __future__ import annotations

import time
from datetime import datetime
from typing import Callable, Iterable

from .buffer import LogBuffer


def _now() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def should_skip(path: str, skip_prefixes: Iterable[str]) -> bool:
    for p in skip_prefixes:
        if path.startswith(p):
            return True
    return False


def make_asgi_middleware(
    buffer: LogBuffer,
    skip_prefixes: Iterable[str] = ("/static", "/api/v1/logs", "/audit/logs"),
):
    """Starlette/FastAPI-compatible HTTP middleware factory."""

    async def audit_log_middleware(request, call_next):
        path = request.url.path
        if should_skip(path, skip_prefixes):
            return await call_next(request)
        start = time.time()
        now = _now()
        buffer.append({
            "time": now,
            "msg": f"[REQ] {request.method} {path}",
            "type": "req",
        })
        response = await call_next(request)
        elapsed_ms = (time.time() - start) * 1000
        buffer.append({
            "time": now,
            "msg": f"[RES] {response.status_code} | {elapsed_ms:.2f}ms",
            "type": "res",
        })
        return response

    return audit_log_middleware
