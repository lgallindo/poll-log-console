"""
Simple.css demo site + poll-log-console (screenshot-friendly).
KISS: PYTHONPATH=../../src/python python3 app.py  →  http://127.0.0.1:8774/
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

PORT = 8774
buf = LogBuffer(60)
app = FastAPI(title="simple-css-demo")
app.middleware("http")(
    make_asgi_middleware(buf, skip_prefixes=("/static", "/api/v1/logs"))
)
app.include_router(build_router(buf, prefix="/api/v1"))
app.mount("/static/dos", StaticFiles(directory=str(static_dir())), name="dos")


@app.post("/api/v1/ping")
async def ping(request: Request) -> JSONResponse:
    body = await request.json()
    note = str(body.get("note", "ping"))
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    buf.append({"time": now, "msg": f"[PING] {note}", "type": "sys"})
    return JSONResponse({"ok": True})


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>poll-log-console on Simple.css</title>
  <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
  <link rel="stylesheet" href="/static/dos/dos-audit-console.css">
</head>
<body>
  <header>
    <h1>Notes on Simple.css</h1>
    <p>Classless layout + floating audit console in the corner.</p>
    <nav>
      <a href="#main">Article</a>
      <a href="#actions">Actions</a>
    </nav>
  </header>
  <main id="main">
    <article>
      <h2>Why this page exists</h2>
      <p>
        This sample shows <strong>poll-log-console</strong> sitting on a
        <a href="https://simplecss.org/">Simple.css</a> document: readable
        typography, no custom design system, console still readable.
      </p>
      <aside>
        Tip: expand the console, click Ping, then screenshot the full viewport.
      </aside>
      <h3 id="actions">Trigger traffic</h3>
      <p>
        <button type="button" id="ping">Ping (audited)</button>
        <button type="button" id="toast">Local toast</button>
      </p>
      <pre>GET /api/v1/logs · POST /api/v1/ping</pre>
    </article>
  </main>
  <footer>
    <p>poll-log-console · Simple.css demo · GPL-3.0-or-later</p>
  </footer>
  <div id="dos-root"></div>
  <script src="/static/dos/dos-audit-console.iife.js"></script>
  <script>
    const ui = DosAuditConsole.mount('#dos-root', {
      logsUrl: '/api/v1/logs',
      infoUrl: '/api/v1/info',
      pollMs: 2000,
      title: 'C:\\\\SIMPLE\\\\AUDIT.LOG',
      sound: true
    });
    document.getElementById('ping').onclick = async () => {
      await fetch('/api/v1/ping', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({note: 'from Simple.css page'})
      });
    };
    document.getElementById('toast').onclick = () => {
      ui.toast('Hello from Simple.css', 'sys');
    };
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return PAGE


if __name__ == "__main__":
    import uvicorn

    print(f"Simple.css demo → http://127.0.0.1:{PORT}/")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
