# hardcopy-console

![hardcopy-console — C:\>](docs/media/brand/banner-dos-hero.png)

**toki:** [English (en_US)](README.md) · [Português (pt_BR)](README.pt-BR.md) · [toki pona](README.tok.md)

**lipu lawa:** [GPL-3.0-or-later](LICENSE) · **ma GitHub:** `git@github.com:lgallindo/hardcopy-console.git`

## ni li seme?

ni li **ilo lukin** lon lipu. ona li lukin e lipu JSON kepeken nasin HTTP. ilo sina li jo e linja lili pi toki pali; ni li kama jo e ona lon tenpo mute (poll) li sitelen e ona lon poki sama ilo toki pi tenpo pini, kepeken tenpo.

ni li **ala** ilo sama DOS anu CP/M. sitelen en nasin lukin taso. nimi pi ni li **hardcopy-console** (API JS `HardcopyConsole`).

![](docs/media/demo/pipeline-dag.gif)

### kepeken

- o lukin e pali pi API en lipu lon tenpo pi pali sina
- o pana e poki lukin lon lipu Flask, FastAPI anu lipu wawa ala
- o pana e lukin pi nasin toki tawa kulupu pi kama sona (workshop), kepeken ala ilo suli pi lukin
- sitelen ante li ken kepeken e poki sama (CP/M, Simple.css, Water.css, …)

**pali suli pi kulupu** (nanpa tu):

- **pali pi pana sin / deploy** — linja pi tenpo kepeken promote, health check, rollback:

  ![Enterprise deploy audit](docs/media/demo/enterprise-deploy-audit.png)

- **pali pi lipu jan / CRM** — jan seme li ante e sona, kepeken tenpo lukin:

  ![Enterprise back-office audit](docs/media/demo/enterprise-backoffice-audit.png)

**toki / lipu toki:**

- toki kama li kama linja (`mail from…`, `chat #general: …`) — historia li lon poki wan, ala popup:

  ![Mail and chat monitor](docs/media/demo/funny-mail-chat-monitor.png)

## tan seme

mi pali e ni tan ni: mi ike e toast. mi wile e toki pi tenpo tawa sona e ilo mi. ken la ni li tan tenpo pi ilo pipeline pi jan pali mi: ona li jo e toast laso jelo taso tawa lukin. mi ike mute e framework JS suli — tan ni la Vanilla JS.

---

## lukin pi monitor

ilo sina li pana e linja tawa poki sike (ring buffer). ilo ni li toki `GET /api/v1/logs`, li kama jo e JSON, li sitelen.

```json
{"time": "14:32:01.423", "msg": "[REQ] GET /health", "type": "req"}
```

(`type` li ken `req`, `res`, `sys`, anu `err` — o lukin e [SPEC.md](SPEC.md).)

**ilo toki:** o kepeken CSS en IIFE tan `dist/`, o open e `div`, o pana e `logsUrl`:

```html
<link rel="stylesheet" href="dist/hardcopy-console.css">
<div id="hardcopy-root"></div>
<script src="dist/hardcopy-console.iife.js"></script>
<script>
  HardcopyConsole.mount('#hardcopy-root', {
    logsUrl: '/api/v1/logs',
    pollMs: 3000,
    title: 'C:\\> MONITOR'
  });
</script>
```

**ilo server:** o pana e JSON ni. toki Python: [adapters/](adapters/) (`LogBuffer`, Flask, FastAPI). o ala lukin e poll ale pi `/logs` — ante la poki li kama mute ike.

---

## o lukin e pali

lipu README pi GitHub li ken ala open e JavaScript. ni li sitelen tawa pi ilo ante; o open e ilo lon ma sina kepeken harness.

**Echo lab** — toki li kama lon log:

![Echo lab monitor demo](docs/media/demo/monitor-echo.gif)

[`examples/echo-lab/`](examples/echo-lab/) → http://127.0.0.1:8773/ (lon tenpo pi `./harness/run.sh`)

**Net status** — sin e sona pi ilo; refresh ale li kama log:

![Net status monitor demo](docs/media/demo/monitor-net-status.gif)

[`examples/net-status/`](examples/net-status/) → http://127.0.0.1:8772/

### nasin musi pi poki

o lili e / o suli e kepeken lawa (`:q` li lili kin). toki sin li ken suno e sike lon lawa li pana e linja pi tenpo (anti-toast). poki li `position: fixed` — o tawa e ona kepeken CSS (`left` / `right` / `bottom`).

![Minimize, toast light, and reposition](docs/media/demo/console-tricks.gif)

---

## nasin open

1. o kepeken `dist/hardcopy-console.css` en `dist/hardcopy-console.iife.js`.
2. o pali e `div` (nimi ale).
3. o kepeken `HardcopyConsole.mount` kepeken `logsUrl` (en `pollMs` mute).
4. o pana e JSON `LogEntry[]` — Python lon `src/python/hardcopy_console/` en [adapters/](adapters/).
5. o weka e `/logs` en nasin static tan middleware pi lukin.
6. o open e `./harness/run.sh` tawa ilo ante luka (port 8771–8775).

poka la o kepeken open lili en nanpa pi ilo ante.

---

## wile

- CSS en IIFE taso (ala Alpine, Tailwind, npm lon tenpo open)
- ken lon Flask, FastAPI (Jinja), Alpine.js, JS, HTMX, [lwan](https://lwan.ws/)
- nasin JSON `LogEntry` · ken kepeken e `LogBuffer` / middleware pi toki Python

## open lili (JS)

```html
<link rel="stylesheet" href="dist/hardcopy-console.css">
<div id="hardcopy-root"></div>
<script src="dist/hardcopy-console.iife.js"></script>
<script>
  HardcopyConsole.mount('#hardcopy-root', {
    logsUrl: '/api/v1/logs',
    infoUrl: '/api/v1/info',
    pollMs: 3000,
    title: 'C:\\> MONITOR'
  });
</script>
```

o lukin e [SPEC.md](SPEC.md) e [adapters/](adapters/).

---

## ilo ante (nanpa)

| lukin | ilo | nasin | nanpa port | seme |
|-------|-----|-------|------------|------|
| ![CP/M term](docs/media/apps/thumbs/cpm-term.png) | **CP/M term** | [`examples/cpm-term/`](examples/cpm-term/) | **8771** | musi CP/M (`DIR`, `TYPE`, `HELP`); toki li kama log |
| ![Net status](docs/media/apps/thumbs/net-status.png) | **Net status** | [`examples/net-status/`](examples/net-status/) | **8772** | nimi ilo, nasin, platform, PID; refresh li log |
| ![Echo lab](docs/media/apps/thumbs/echo-lab.png) | **Echo lab** | [`examples/echo-lab/`](examples/echo-lab/) | **8773** | POST e toki tawa poki · toast/LED |
| ![Simple.css](docs/media/apps/thumbs/simple-css.png) | **Simple.css** | [`examples/simple-css/`](examples/simple-css/) | **8774** | poki lon [Simple.css](https://simplecss.org/) |
| ![Water.css](docs/media/apps/thumbs/water-css.png) | **Water.css** | [`examples/water-css/`](examples/water-css/) | **8775** | poki lon [Water.css](https://watercss.kognise.dev/) |

kin la stubs: `examples/vanilla-standalone/`, `alpine-standalone/`, `flask-app/`, `fastapi-app/`, `htmx-poll/`, `lwan/`.

### o open e ilo ante

```bash
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn
chmod +x harness/run.sh
./harness/run.sh
```

- http://127.0.0.1:8771/ — CP/M  
- http://127.0.0.1:8772/ — sona pi linja  
- http://127.0.0.1:8773/ — Echo lab  
- http://127.0.0.1:8774/ — Simple.css  
- http://127.0.0.1:8775/ — Water.css  

anu wan:

```bash
cd examples/cpm-term && PYTHONPATH=../../src/python python3 app.py
cd examples/net-status && PYTHONPATH=../../src/python python3 app.py
cd examples/echo-lab && PYTHONPATH=../../src/python python3 app.py
cd examples/simple-css && PYTHONPATH=../../src/python python3 app.py
cd examples/water-css && PYTHONPATH=../../src/python python3 app.py
```

sona mute: [harness/README.md](harness/README.md).

---

## lipu

| nasin | seme |
|-------|------|
| `src/` | CSS, JS, HTML, Python |
| `dist/` | CSS en IIFE tawa kepeken |
| `adapters/` | sona pi nasin ante |
| `examples/` | ilo ante |
| `harness/` | open e lukin e ilo ante |
| `tests/` | test |
| `docs/media/brand/` | banner GitHub · mark · sitelen lili |
| `docs/media/demo/` | sitelen tawa README |

## lipu lawa

[GPL-3.0-or-later](LICENSE) — kin [COPYING.short](COPYING.short).
