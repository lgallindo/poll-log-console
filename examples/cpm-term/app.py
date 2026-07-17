"""
CP/M terminal simulator + poll-log-console.
Run:
  cd examples/cpm-term && PYTHONPATH=../../src/python python3 app.py
  open http://127.0.0.1:8771/
"""
from __future__ import annotations

import sys
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

PORT = 8771
buf = LogBuffer(80)
app = FastAPI(title="cpm-term")
app.middleware("http")(make_asgi_middleware(buf, skip_prefixes=("/static", "/api/v1/logs")))
app.include_router(build_router(buf, prefix="/api/v1"))
app.mount("/static/dos", StaticFiles(directory=str(static_dir())), name="dos")

DISK = {
    "README.TXT": "POLL-LOG-CONSOLE CPM DEMO\r\nTYPE README.TXT\r\nDIR\r\n",
    "HELLO.COM": "(binary stub)",
    "STAT.COM": "(binary stub)",
}


@app.post("/api/v1/cpm")
async def cpm_cmd(request: Request) -> JSONResponse:
    body = await request.json()
    line = str(body.get("cmd", "")).strip().upper()
    now = __import__("datetime").datetime.now().strftime("%H:%M:%S.%f")[:-3]
    out = ""
    if not line:
        out = ""
    elif line in {"DIR", "ERA *.*"} or line.startswith("DIR"):
        out = "\n".join(f"A: {name}" for name in sorted(DISK)) + "\n"
    elif line.startswith("TYPE "):
        name = line.split(None, 1)[1].strip()
        out = DISK.get(name, f"{name}?") + ("\n" if name in DISK else "\n")
    elif line in {"HELP", "?"}:
        out = "Commands: DIR  TYPE <file>  HELP  CLS\n"
    elif line == "CLS":
        out = ""
    else:
        out = f"{line.split()[0]}?\n"
    buf.append({"time": now, "msg": f"[CPM] {line or '(empty)'}", "type": "sys"})
    return JSONResponse({"ok": True, "output": out})


PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><title>A&gt; CP/M demo</title>
<link rel="stylesheet" href="/static/dos/dos-audit-console.css">
<style>
  body{margin:0;background:#001800;color:#33ff66;font-family:"Courier New",monospace}
  #term{padding:1rem;min-height:60vh;white-space:pre-wrap}
  #line{width:90%;background:#001800;border:none;color:#33ff66;font:inherit;outline:none}
</style></head><body>
<div id="term">CP/M DEMO 2.2 — type HELP\n\n</div>
<div style="padding:0 1rem">A&gt; <input id="line" autofocus autocomplete="off"></div>
<div id="dos-root"></div>
<script src="/static/dos/dos-audit-console.iife.js"></script>
<script>
  const ui = DosAuditConsole.mount('#dos-root', {
    logsUrl: '/api/v1/logs', infoUrl: '/api/v1/info', pollMs: 2000,
    title: 'A:\\\\AUDIT.LOG'
  });
  const term = document.getElementById('term');
  const input = document.getElementById('line');
  input.addEventListener('keydown', async (e) => {
    if (e.key !== 'Enter') return;
    const cmd = input.value;
    term.textContent += 'A> ' + cmd + '\\n';
    input.value = '';
    const res = await fetch('/api/v1/cpm', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({cmd})
    });
    const data = await res.json();
    if (cmd.trim().toUpperCase() === 'CLS') term.textContent = '';
    else if (data.output) term.textContent += data.output;
    ui.toast('CP/M: ' + (cmd || '(empty)'), 'sys');
  });
</script></body></html>
"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return PAGE


if __name__ == "__main__":
    import uvicorn
    print(f"CP/M demo → http://127.0.0.1:{PORT}/")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
