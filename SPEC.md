# SPEC — hardcopy-console v1

**Languages:** [English (en_US)](SPEC.md) · [Português (pt_BR)](SPEC.pt-BR.md) · [toki pona](SPEC.tok.md)

**Audience:** integrators (host app + UI mount). Not end users.

**Goal of this doc:** enough baby steps and copy-paste examples to wire a working console without reading the whole README first. Deeper demos live under [`examples/`](examples/) and [`adapters/`](adapters/).

---

## Baby steps (end-to-end)

Do these in order. After step 5 you should see lines appear in the DOS-style panel.

### 1. Serve the static assets

Ship (or mount) the built files from `dist/`:

| File | Role |
|------|------|
| `hardcopy-console.css` | Styles |
| `hardcopy-console.iife.js` | Browser global `HardcopyConsole` |

**Python helper** (path to that directory):

```python
from hardcopy_console import static_dir
# e.g. FastAPI: app.mount("/static/hardcopy", StaticFiles(directory=static_dir()), …)
```

### 2. Keep a ring of `LogEntry` objects on the server

Minimum shape (JSON):

```json
{
  "time": "14:32:01.423",
  "msg": "[REQ] GET /api/v1/vault/executions",
  "type": "req"
}
```

`type` must be one of: `req` | `res` | `sys` | `err`.

**Python:**

```python
from hardcopy_console.buffer import LogBuffer

buf = LogBuffer(50)  # maxlen window returned by GET /logs
buf.append({
    "time": "14:32:01.423",
    "msg": "[SYS] boot",
    "type": "sys",
})
```

**Any language:** a list/deque of those objects is enough. Optional fields `id`, `seq`, `level` are ignored by v1 clients.

### 3. Expose `GET …/logs` (and optionally `GET …/info`)

| Method | Path | Response |
|--------|------|----------|
| `GET` | `{prefix}/logs` | `LogEntry[]` (current ring window) |
| `GET` | `{prefix}/info` | Optional boot metadata object (any JSON object) |

**Hand-rolled (any stack)** — response body example for `/api/v1/logs`:

```json
[
  {"time": "14:32:01.423", "msg": "[SYS] boot", "type": "sys"},
  {"time": "14:32:02.100", "msg": "[REQ] GET /health", "type": "req"}
]
```

**FastAPI (library router):**

```python
from hardcopy_console.fastapi_router import build_router

app.include_router(build_router(buf, prefix="/api/v1"))
# → GET /api/v1/logs , GET /api/v1/info
```

**Flask:** see [`adapters/flask/`](adapters/flask/) (`create_blueprint`).

**Critical:** do **not** audit/`append` on `GET …/logs` or static asset paths, or the poller floods the buffer. Skip those prefixes in middleware.

```python
from hardcopy_console.middleware_asgi import make_asgi_middleware

app.middleware("http")(
    make_asgi_middleware(buf, skip_prefixes=("/static", "/api/v1/logs"))
)
```

### 4. Put a mount node in HTML and load CSS/JS

```html
<link rel="stylesheet" href="/static/hardcopy/hardcopy-console.css">
<div id="hardcopy-root"></div>
<script src="/static/hardcopy/hardcopy-console.iife.js"></script>
```

Paths must match how you mounted `static_dir()` / `dist/`.

### 5. Call `HardcopyConsole.mount`

```html
<script>
  const ui = HardcopyConsole.mount('#hardcopy-root', {
    logsUrl: '/api/v1/logs',   // required for polling
    infoUrl: '/api/v1/info',   // optional
    pollMs: 3000,
    title: 'C:\\> MONITOR'
  });

  // Optional: local-only line (does not hit the server)
  ui.toast('hello from host', 'sys');
</script>
```

Open the page, expand the console if minimized, wait one `pollMs` — server lines should appear.

### 6. Prove it with a local sample (optional)

```bash
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn
./harness/run.sh
# http://127.0.0.1:8773/ — Echo lab posts into the ring + mounts the console
```

Or one app: `cd examples/echo-lab && PYTHONPATH=../../src/python python3 app.py`

---

## Minimal server without the Python package

Any HTTP stack works if it returns `LogEntry[]` from your `logsUrl`.

**Node (sketch):**

```js
const logs = [];
app.get('/api/v1/logs', (_req, res) => res.json(logs));

// elsewhere, when something happens:
logs.push({
  time: new Date().toISOString().slice(11, 23),
  msg: '[REQ] GET /x',
  type: 'req',
});
if (logs.length > 50) logs.shift();
```

Pair with the same HTML mount from steps 4–5.

---

## Client options

All keys are optional except you almost always set `logsUrl` (and usually `pollMs`).

```js
{
  logsUrl: '/api/v1/logs',
  infoUrl: '/api/v1/info',   // optional; omit if you have no /info
  pollMs: 3000,
  storageKey: 'hardcopy_logs',
  maxLocalLogs: 500,
  sound: true,
  title: 'C:\\> MONITOR',
  bootLines: null,           // optional string[] override for boot text
  actions: ['copy', 'clear'] // 'kg' is host-specific; omitted by default
}
```

Library default for `title` in the IIFE is still `C:\SYSTEM\AUDIT_LOG.EXE`; prefer overriding to a prompt-style title (e.g. `C:\> MONITOR`) for the current brand face.

---

## Transport

v1 = **HTTP polling** of `logsUrl`. SSE may be added later without changing `LogEntry`.

---

## UI commands (console input)

| Input | Action |
|-------|--------|
| `:w` | Copy logs to clipboard |
| `:q` | Minimize |
| `cls` | Clear logs + storage |

---

## LogEntry (reference)

| Field | Type | Notes |
|-------|------|--------|
| `time` | string | Display clock (`HH:MM:SS.mmm` or locale time) |
| `msg` | string | Free text |
| `type` | string | `req` \| `res` \| `sys` \| `err` |

Optional (ignored by v1 clients if absent): `id`, `seq`, `level`.

---

## Next adapters

| Stack | Where |
|-------|--------|
| Vanilla / IIFE | [`adapters/vanilla/`](adapters/vanilla/) |
| Alpine | [`adapters/alpine/`](adapters/alpine/) |
| HTMX | [`adapters/htmx/`](adapters/htmx/) |
| FastAPI | [`adapters/fastapi/`](adapters/fastapi/) |
| Flask | [`adapters/flask/`](adapters/flask/) |
| lwan | [`adapters/lwan/`](adapters/lwan/) |
