"""
Water.css demo site + hardcopy-console.
Run: PYTHONPATH=../../src/python python3 app.py  →  http://127.0.0.1:8775/
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

from hardcopy_console import static_dir
from hardcopy_console.buffer import LogBuffer
from hardcopy_console.fastapi_router import build_router
from hardcopy_console.middleware_asgi import make_asgi_middleware

PORT = 8775
buf = LogBuffer(60)
app = FastAPI(title="water-css-demo")
app.middleware("http")(
    make_asgi_middleware(buf, skip_prefixes=("/static", "/api/v1/logs"))
)
app.include_router(build_router(buf, prefix="/api/v1"))
app.mount("/static/hardcopy", StaticFiles(directory=str(static_dir())), name="hardcopy")


@app.post("/api/v1/note")
async def note(request: Request) -> JSONResponse:
    body = await request.json()
    text = str(body.get("text", "note"))
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    buf.append({"time": now, "msg": f"[NOTE] {text}", "type": "res"})
    return JSONResponse({"ok": True})


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>hardcopy-console on Water.css</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css">
  <link rel="stylesheet" href="/static/hardcopy/hardcopy-console.css">
</head>
<body>
  <h1>Water.css + audit console</h1>
  <p>
    Same widget on
    <a href="https://watercss.kognise.dev/">Water.css</a>:
    soft classless styling, dark-friendly defaults, console still fixed bottom-right.
  </p>
  <blockquote>
    Soft classless styling with the audit console fixed bottom-right.
  </blockquote>
  <form id="f">
    <label for="t">Leave a note (audited)</label>
    <input id="t" name="t" placeholder="short note…" required>
    <button type="submit">Save note</button>
  </form>
  <hr>
  <p><button type="button" id="err">Simulate error toast</button></p>
  <div id="hardcopy-root"></div>
  <script src="/static/hardcopy/hardcopy-console.iife.js"></script>
  <script>
    const ui = HardcopyConsole.mount('#hardcopy-root', {
      logsUrl: '/api/v1/logs',
      infoUrl: '/api/v1/info',
      pollMs: 2000,
      title: 'C:\\\\WATER\\\\AUDIT.LOG',
      sound: true
    });
    document.getElementById('f').onsubmit = async (e) => {
      e.preventDefault();
      const text = document.getElementById('t').value;
      await fetch('/api/v1/note', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text})
      });
      ui.toast('note saved', 'sys');
      document.getElementById('t').value = '';
    };
    document.getElementById('err').onclick = () => {
      ui.toast('something went wrong', 'err');
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

    print(f"Water.css demo → http://127.0.0.1:{PORT}/")
    uvicorn.run(app, host="127.0.0.1", port=PORT)
