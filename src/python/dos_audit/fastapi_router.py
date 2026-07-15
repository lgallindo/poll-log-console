from __future__ import annotations

from .buffer import LogBuffer


def build_router(buffer: LogBuffer, prefix: str = "/api/v1"):
    """Return a FastAPI APIRouter exposing GET {prefix}/logs (+ optional /info stub)."""
    from fastapi import APIRouter

    router = APIRouter(prefix=prefix, tags=["dos-audit"])

    @router.get("/logs")
    def get_logs() -> list:
        return buffer.list()

    @router.get("/info")
    def get_info() -> dict:
        import datetime
        import os
        import time

        return {
            "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": time.strftime("%Z"),
            "api_key_status": "UNKNOWN",
            "port": 0,
            "os": os.name.upper(),
            "kernel": "dos-audit-console",
        }

    return router
