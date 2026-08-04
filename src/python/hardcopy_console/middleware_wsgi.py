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
    app.extensions["hardcopy_console_buffer"] = buffer

    @app.before_request
    def _hardcopy_before():
        from flask import g, request
        if should_skip(request.path, skip_prefixes):
            g._hardcopy_skip = True
            return
        g._hardcopy_skip = False
        g._hardcopy_start = time.time()
        g._hardcopy_now = _now()
        buffer.append({
            "time": g._hardcopy_now,
            "msg": f"[REQ] {request.method} {request.path}",
            "type": "req",
        })

    @app.after_request
    def _hardcopy_after(response):
        from flask import g
        if getattr(g, "_hardcopy_skip", True):
            return response
        elapsed_ms = (time.time() - g._hardcopy_start) * 1000
        buffer.append({
            "time": g._hardcopy_now,
            "msg": f"[RES] {response.status_code} | {elapsed_ms:.2f}ms",
            "type": "res",
        })
        return response

    return buffer
