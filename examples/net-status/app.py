"""
Network & server status + poll-log-console.
Run:
  cd examples/net-status && PYTHONPATH=../../src/python python3 app.py
  open http://127.0.0.1:8772/
"""
from __future__ import annotations

import os
import platform
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "python"))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from dos_audit import static_dir
from dos_audit.buffer import LogBuffer
from dos_audit.fastapi_router import build_router
from dos_audit.middleware_asgi import make_asgi_middleware

PORT = 8772
buf = LogBuffer(80)
app = FastAPI(title="net-status")
app.middleware("http")(make_asgi_middleware(buf, skip_prefixes=("/static", "/api/v1/logs", "/api/v1/status")))
app.include_router(build_router(buf, prefix="/api/v1"))
app.mount("/static/dos", StaticFiles(directory=str(static_dir())), name="dos")


def gather_status() -> dict:
    host = socket.gethostname()
    addrs: list[str] = []
    try:
        for info in socket.getaddrinfo(host, None):
            a = info[4][0]
            if a not in addrs:
                addrs.append(a)
    except OSError:
        addrs = ["(unavailable)"]
    return {
        "hostname": host,
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "addresses": addrs,
        "port": PORT,
        "ok": True,
    }


@app.get("/api/v1/status")
def status() -> JSONResponse:
    return JSONResponse(gather_status())


PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><title>Net / server status</title>
<link rel="stylesheet" href="/static/dos/dos-audit-console.css">
<style>
  body{font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0;margin:2rem}
  pre{background:#020617;padding:1rem;border-radius:8px;overflow:auto}
  button{padding:.5rem 1rem;cursor:pointer}
</style></head><body>
<h1>Network &amp; server status</h1>
<p>Refresh probes host identity; each click is audited in the corner console.</p>
<button id="refresh">Refresh status</button>
<pre id="out">Loading…</pre>
<div id="dos-root"></div>
<script src="/static/dos/dos-audit-console.iife.js"></script>
<script>
  const ui = DosAuditConsole.mount('#dos-root', {
    logsUrl: '/api/v1/logs', infoUrl: '/api/v1/info', pollMs: 2000,
    title: 'C:\\\\NET\\\\STATUS.LOG'
  });
  async function load() {
    const res = await fetch('/api/v1/status');
    const data = await res.json();
    document.getElementById('out').textContent = JSON.stringify(data, null, 2);
    ui.toast('status refreshed', 'sys');
  }
  document.getElementById('refresh').onclick = load;
  load();
</script></body></html>
"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return PAGE


if __name__ == "__main__":
    import uvicorn
    print(f"Net status → http://127.0.0.1:{PORT}/")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
