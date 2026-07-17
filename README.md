# poll-log-console

**Languages:** [English (en_US)](README.md) · [Português (pt_BR)](README.pt-BR.md) · [toki pona](README.tok.md)

Reusable **HTTP poll-log / audit console** widget (static-first CSS + IIFE).  
Theme nods to classic terminal chrome; the package does **not** emulate DOS/CP/M by itself.

**License:** [GPL-3.0-or-later](LICENSE)

**GitHub:** `git@github.com:lgallindo/poll-log-console.git`

---

## Goals

- Pure CSS + IIFE JS (no mandatory Alpine, Tailwind, or npm at runtime)
- Drop into Flask, FastAPI (Jinja), Alpine.js, vanilla JS, HTMX, and [lwan](https://lwan.ws/)
- Shared `LogEntry` JSON contract + optional Python `LogBuffer` / middleware

## Quick start (vanilla)

```html
<link rel="stylesheet" href="dist/dos-audit-console.css">
<div id="dos-root"></div>
<script src="dist/dos-audit-console.iife.js"></script>
<script>
  DosAuditConsole.mount('#dos-root', {
    logsUrl: '/api/v1/logs',
    infoUrl: '/api/v1/info',
    pollMs: 3000,
    title: 'C:\\SYSTEM\\AUDIT_LOG.EXE'
  });
</script>
```

See [SPEC.md](SPEC.md) and [adapters/](adapters/).

---

## Sample apps (index)

| App | Path | Port | What it does |
|-----|------|------|----------------|
| **CP/M term** | [`examples/cpm-term/`](examples/cpm-term/) | **8771** | Toy CP/M prompt (`DIR`, `TYPE`, `HELP`); commands are audited |
| **Net status** | [`examples/net-status/`](examples/net-status/) | **8772** | Hostname, addresses, platform, PID; refresh hits the log |
| **Echo lab** | [`examples/echo-lab/`](examples/echo-lab/) | **8773** | POST a message into the ring buffer + local toast/LED |
| **Simple.css** | [`examples/simple-css/`](examples/simple-css/) | **8774** | Console on a [Simple.css](https://simplecss.org/) page |
| **Water.css** | [`examples/water-css/`](examples/water-css/) | **8775** | Console on a [Water.css](https://watercss.kognise.dev/) page |

Also present (stubs): `examples/vanilla-standalone/`, `alpine-standalone/`, `flask-app/`, `fastapi-app/`, `htmx-poll/`, `lwan/`.

### Run the sample apps

```bash
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn
chmod +x harness/run.sh
./harness/run.sh
```

- http://127.0.0.1:8771/ — CP/M  
- http://127.0.0.1:8772/ — Net status  
- http://127.0.0.1:8773/ — Echo lab  
- http://127.0.0.1:8774/ — Simple.css  
- http://127.0.0.1:8775/ — Water.css  

Or one at a time:

```bash
cd examples/cpm-term && PYTHONPATH=../../src/python python3 app.py
cd examples/net-status && PYTHONPATH=../../src/python python3 app.py
cd examples/echo-lab && PYTHONPATH=../../src/python python3 app.py
cd examples/simple-css && PYTHONPATH=../../src/python python3 app.py
cd examples/water-css && PYTHONPATH=../../src/python python3 app.py
```

Details: [harness/README.md](harness/README.md).

---

## Layout

| Path | Role |
|------|------|
| `src/` | CSS, JS core + adapters, HTML fragments, Python package |
| `dist/` | Offline-ready CSS + IIFE |
| `adapters/` | Notes per host (Flask, FastAPI, Alpine, Vanilla, HTMX, lwan) |
| `examples/` | Sample applications |
| `harness/` | Start and check sample apps |
| `tests/` | Unit + e2e notes |

## License

[GPL-3.0-or-later](LICENSE) — see also [COPYING.short](COPYING.short).
