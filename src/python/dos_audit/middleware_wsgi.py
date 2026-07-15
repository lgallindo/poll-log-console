from __future__ import annotations

import time
from datetime import datetime
from typing import Iterable

from .buffer import LogBuffer
from .middleware_asgi import should_skip


def _now() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def init_audit(
    app,
    maxlen: int = 50,
    skip_prefixes: Iterable[str] = ("/static", "/audit/logs"),
) -> LogBuffer:
    """Attach a simple before/after request auditor to a Flask app."""
    buffer = LogBuffer(maxlen=maxlen)
    app.extensions = getattr(app, "extensions", {})
    app.extensions["dos_audit_buffer"] = buffer

    @app.before_request
    def _dos_before():
        from flask import g, request
        if should_skip(request.path, skip_prefixes):
            g._dos_skip = True
            return
        g._dos_skip = False
        g._dos_start = time.time()
        g._dos_now = _now()
        buffer.append({
            "time": g._dos_now,
            "msg": f"[REQ] {request.method} {request.path}",
            "type": "req",
        })

    @app.after_request
    def _dos_after(response):
        from flask import g
        if getattr(g, "_dos_skip", True):
            return response
        elapsed_ms = (time.time() - g._dos_start) * 1000
        buffer.append({
            "time": g._dos_now,
            "msg": f"[RES] {response.status_code} | {elapsed_ms:.2f}ms",
            "type": "res",
        })
        return response

    return buffer
