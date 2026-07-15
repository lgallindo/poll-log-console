"""Minimal FastAPI example — run: PYTHONPATH=../../src/python uvicorn app:app --reload"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "python"))

from dos_audit.buffer import LogBuffer
from dos_audit.middleware_asgi import make_asgi_middleware
from dos_audit.fastapi_router import build_router
from dos_audit import static_dir

app = FastAPI()
buf = LogBuffer(50)
app.middleware("http")(make_asgi_middleware(buf, skip_prefixes=("/static", "/api/v1/logs")))
app.include_router(build_router(buf, prefix="/api/v1"))
app.mount("/static/dos", StaticFiles(directory=str(static_dir())), name="dos")

PAGE = """<!doctype html><html><head>
<link rel="stylesheet" href="/static/dos/dos-audit-console.css">
</head><body style="background:#111;color:#ccc;padding:2rem">
<h1>FastAPI + dos-audit-console</h1>
<div id="dos-root"></div>
<script src="/static/dos/dos-audit-console.iife.js"></script>
<script>
DosAuditConsole.mount('#dos-root', { logsUrl: '/api/v1/logs', infoUrl: '/api/v1/info' });
</script></body></html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return PAGE
