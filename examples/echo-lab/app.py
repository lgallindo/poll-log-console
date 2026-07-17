"""
Echo Lab — post messages into the audit ring + poll-log-console.
(Chosen third sample: demonstrates host toast + middleware together.)
KISS run:
  cd examples/echo-lab && PYTHONPATH=../../src/python python3 app.py
  open http://127.0.0.1:8773/
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "python"))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from dos_audit import static_dir
from dos_audit.buffer import LogBuffer
from dos_audit.fastapi_router import build_router
from dos_audit.middleware_asgi import make_asgi_middleware

PORT = 8773
buf = LogBuffer(100)
app = FastAPI(title="echo-lab")
app.middleware("http")(make_asgi_middleware(buf, skip_prefixes=("/static", "/api/v1/logs")))
app.include_router(build_router(buf, prefix="/api/v1"))
app.mount("/static/dos", StaticFiles(directory=str(static_dir())), name="dos")


@app.post("/api/v1/echo")
async def echo(request: Request) -> JSONResponse:
    body = await request.json()
    msg = str(body.get("message", "")).strip() or "(empty)"
    kind = str(body.get("type", "sys"))
    if kind not in {"sys", "err", "req", "res"}:
        kind = "sys"
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    buf.append({"time": now, "msg": f"[ECHO] {msg}", "type": kind})
    return JSONResponse({"ok": True, "echoed": msg, "type": kind})


PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><title>Echo Lab</title>
<link rel="stylesheet" href="/static/dos/dos-audit-console.css">
<style>
  body{font-family:system-ui,sans-serif;background:#1a1025;color:#f5e8ff;margin:2rem;max-width:40rem}
  textarea,select,button{width:100%;margin:.4rem 0;padding:.5rem;box-sizing:border-box}
</style></head><body>
<h1>Echo Lab</h1>
<p>Push a line into the server ring buffer; the console polls it and can also toast locally.</p>
<textarea id="msg" rows="4" placeholder="Type a message…"></textarea>
<select id="type">
  <option value="sys">sys</option>
  <option value="err">err</option>
  <option value="req">req</option>
  <option value="res">res</option>
</select>
<button id="send">Echo</button>
<div id="dos-root"></div>
<script src="/static/dos/dos-audit-console.iife.js"></script>
<script>
  const ui = DosAuditConsole.mount('#dos-root', {
    logsUrl: '/api/v1/logs', infoUrl: '/api/v1/info', pollMs: 1500,
    title: 'C:\\\\ECHO\\\\LAB.LOG'
  });
  document.getElementById('send').onclick = async () => {
    const message = document.getElementById('msg').value;
    const type = document.getElementById('type').value;
    await fetch('/api/v1/echo', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message, type})
    });
    ui.toast(message || '(empty)', type === 'err' ? 'err' : 'sys');
  };
</script></body></html>
"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return PAGE


if __name__ == "__main__":
    import uvicorn
    print(f"Echo Lab → http://127.0.0.1:{PORT}/")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
