# SPEC — hardcopy-console v1

**toki:** [English (en_US)](SPEC.md) · [Português (pt_BR)](SPEC.pt-BR.md) · [toki pona](SPEC.tok.md)

**jan pi lipu ni:** jan pi wan e ilo (ilo suli + sitelen UI). ni li **ala** tawa jan kepeken.

**wile pi lipu ni:** nasin lili en toki sama kepeken open, tawa wan e console kepeken ala lukin e README ale. lukin suli li lon [`examples/`](examples/) en [`adapters/`](adapters/).

---

## nasin lili (open tawa pini)

o pali kepeken nanpa ni. pini pi nasin 5 la sina lukin e linja lon poki sama DOS.

### 1. o pana e lipu wawa ala (static)

o pana (anu o open e nasin) e lipu tan `dist/`:

| lipu | pali |
|------|------|
| `hardcopy-console.css` | sitelen |
| `hardcopy-console.iife.js` | nimi suli `HardcopyConsole` lon ilo lukin |

**ilo Python** (nasin pi poki ni):

```python
from hardcopy_console import static_dir
# e.g. FastAPI: app.mount("/static/hardcopy", StaticFiles(directory=static_dir()), …)
```

### 2. o awen e sike pi `LogEntry` lon ilo suli

nena lili (JSON):

```json
{
  "time": "14:32:01.423",
  "msg": "[REQ] GET /api/v1/vault/executions",
  "type": "req"
}
```

`type` li ken ni taso: `req` | `res` | `sys` | `err`.

**Python:**

```python
from hardcopy_console.buffer import LogBuffer

buf = LogBuffer(50)  # nanpa suli pi linja tan GET /logs
buf.append({
    "time": "14:32:01.423",
    "msg": "[SYS] boot",
    "type": "sys",
})
```

**toki ante ale:** lipu anu deque pi ijo ni li pona. nimi `id`, `seq`, `level` li ken; ilo v1 li lukin ala e ona.

### 3. o open e `GET …/logs` (en ken la `GET …/info`)

| nasin | nasin lipu | toki tawa |
|--------|------|----------|
| `GET` | `{prefix}/logs` | `LogEntry[]` (sike pi tenpo ni) |
| `GET` | `{prefix}/info` | ijo pi sona open (ken; ijo JSON ante) |

**kepeken luka** — toki sama tawa `/api/v1/logs`:

```json
[
  {"time": "14:32:01.423", "msg": "[SYS] boot", "type": "sys"},
  {"time": "14:32:02.100", "msg": "[REQ] GET /health", "type": "req"}
]
```

**FastAPI (ilo pi lipu ni):**

```python
from hardcopy_console.fastapi_router import build_router

app.include_router(build_router(buf, prefix="/api/v1"))
# → GET /api/v1/logs , GET /api/v1/info
```

**Flask:** o lukin e [`adapters/flask/`](adapters/flask/) (`create_blueprint`).

**suli a:** o **ala** pali e audit/`append` lon `GET …/logs` anu nasin pi lipu wawa ala. ante la poller li pana e linja mute mute. o weka e nasin ni lon middleware.

```python
from hardcopy_console.middleware_asgi import make_asgi_middleware

app.middleware("http")(
    make_asgi_middleware(buf, skip_prefixes=("/static", "/api/v1/logs"))
)
```

### 4. o pana e poki mount lon HTML, o kama jo e CSS/JS

```html
<link rel="stylesheet" href="/static/hardcopy/hardcopy-console.css">
<div id="hardcopy-root"></div>
<script src="/static/hardcopy/hardcopy-console.iife.js"></script>
```

nasin li wile sama mount pi `static_dir()` / `dist/`.

### 5. o kepeken e `HardcopyConsole.mount`

```html
<script>
  const ui = HardcopyConsole.mount('#hardcopy-root', {
    logsUrl: '/api/v1/logs',   // wile tawa poll
    infoUrl: '/api/v1/info',   // ken
    pollMs: 3000,
    title: 'C:\\> MONITOR'
  });

  // ken: linja lon lipu taso (li tawa ala ilo suli)
  ui.toast('toki tan host', 'sys');
</script>
```

o open e lipu, o suli e console (lon lili la), o awen e tenpo `pollMs` — linja tan ilo suli li kama.

### 6. o lukin kepeken sample lon ma sina (ken)

```bash
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn
./harness/run.sh
# http://127.0.0.1:8773/ — Echo lab li pana e linja lon sike + li mount e console
```

anu ilo wan: `cd examples/echo-lab && PYTHONPATH=../../src/python python3 app.py`

---

## ilo suli lili kepeken ala poki Python

nasin HTTP ante li pona, lon tenpo ni: ona li pana e `LogEntry[]` tan `logsUrl` sina.

**Node (sitelen lili):**

```js
const logs = [];
app.get('/api/v1/logs', (_req, res) => res.json(logs));

// ante la, lon tenpo pi ijo:
logs.push({
  time: new Date().toISOString().slice(11, 23),
  msg: '[REQ] GET /x',
  type: 'req',
});
if (logs.length > 50) logs.shift();
```

o kepeken e mount HTML sama tan nasin 4–5.

---

## wile pi ilo lukin (client)

nimi ale li ken. taso tenpo mute la sina pana e `logsUrl` (en `pollMs`).

```js
{
  logsUrl: '/api/v1/logs',
  infoUrl: '/api/v1/info',   // ken; o weka e ona lon tenpo pi /info ala
  pollMs: 3000,
  storageKey: 'hardcopy_logs',
  maxLocalLogs: 500,
  sound: true,
  title: 'C:\\> MONITOR',
  bootLines: null,           // string[] ken tawa toki open
  actions: ['copy', 'clear'] // 'kg' li tan host; weka lon open
}
```

nimi open pi `title` lon IIFE li `C:\SYSTEM\AUDIT_LOG.EXE` lon tenpo ni; o ante e ona tawa nimi sama prompt (e.g. `C:\> MONITOR`) tawa sitelen pi nimi suli.

---

## nasin toki (transport)

v1 = **poll HTTP** pi `logsUrl`. SSE li ken kama lon tenpo kama kepeken ante ala e `LogEntry`.

---

## toki pi UI (sitelen lon console)

| sitelen | pali |
|-------|--------|
| `:w` | o kama jo e linja tawa poki pi lipu (clipboard) |
| `:q` | o lili |
| `cls` | o weka e linja + storage |

---

## LogEntry (sona)

| nimi | nasin | toki |
|-------|------|--------|
| `time` | string | tenpo lukin (`HH:MM:SS.mmm` anu tenpo pi ma) |
| `msg` | string | toki ante |
| `type` | string | `req` \| `res` \| `sys` \| `err` |

ken (ilo v1 li lukin ala): `id`, `seq`, `level`.

---

## adapters kama

| nasin | lon |
|-------|--------|
| Vanilla / IIFE | [`adapters/vanilla/`](adapters/vanilla/) |
| Alpine | [`adapters/alpine/`](adapters/alpine/) |
| HTMX | [`adapters/htmx/`](adapters/htmx/) |
| FastAPI | [`adapters/fastapi/`](adapters/fastapi/) |
| Flask | [`adapters/flask/`](adapters/flask/) |
| lwan | [`adapters/lwan/`](adapters/lwan/) |
