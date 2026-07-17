# poll-log-console

**Idiomas:** [English (en_US)](README.md) · [Português (pt_BR)](README.pt-BR.md) · [toki pona](README.tok.md)

Widget reutilizável de **console de auditoria via polling HTTP** (CSS puro + IIFE).  
O visual lembra um terminal clássico; o pacote **não** emula DOS/CP/M sozinho.

**Licença:** [GPL-3.0-or-later](LICENSE)

**GitHub:** `git@github.com:lgallindo/poll-log-console.git`

---

## Objetivos

- CSS + IIFE sem exigir Alpine, Tailwind ou npm em runtime
- Integração com Flask, FastAPI (Jinja), Alpine.js, JS puro, HTMX e [lwan](https://lwan.ws/)
- Contrato JSON `LogEntry` + `LogBuffer` / middleware Python opcional

## Início rápido (vanilla)

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

Veja [SPEC.md](SPEC.md) e [adapters/](adapters/).

---

## Aplicativos de exemplo (índice)

| App | Caminho | Porta | Função |
|-----|---------|-------|--------|
| **CP/M term** | [`examples/cpm-term/`](examples/cpm-term/) | **8771** | Prompt CP/M de brincadeira; comandos vão para o log |
| **Net status** | [`examples/net-status/`](examples/net-status/) | **8772** | Hostname, endereços, plataforma, PID |
| **Echo lab** | [`examples/echo-lab/`](examples/echo-lab/) | **8773** | POST no buffer + toast/LED |
| **Simple.css** | [`examples/simple-css/`](examples/simple-css/) | **8774** | Console numa página [Simple.css](https://simplecss.org/) (screenshot) |
| **Water.css** | [`examples/water-css/`](examples/water-css/) | **8775** | Console numa página [Water.css](https://watercss.kognise.dev/) (screenshot) |

Também existem stubs: `vanilla-standalone/`, `alpine-standalone/`, `flask-app/`, `fastapi-app/`, `htmx-poll/`, `lwan/`.

### KISS — harness de screenshots

O harness **mantém os demos no ar para você tirar screenshots bonitos**. Não é para
badges de CI nem gimmicks de cabeçalho de repositório.

```bash
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn
chmod +x harness/run.sh
./harness/run.sh
```

Abra (expanda o console → clique em algo → capture a viewport):

- http://127.0.0.1:8771/ — CP/M  
- http://127.0.0.1:8772/ — Status de rede  
- http://127.0.0.1:8773/ — Echo lab  
- http://127.0.0.1:8774/ — Simple.css  
- http://127.0.0.1:8775/ — Water.css  

Detalhes: [harness/README.md](harness/README.md).

---

## Estrutura

| Caminho | Papel |
|---------|--------|
| `src/` | CSS, JS, HTML, pacote Python |
| `dist/` | Artefatos offline |
| `adapters/` | Notas por framework |
| `examples/` | Aplicativos de exemplo |
| `harness/` | Demos abertos para screenshots |
| `tests/` | Testes |

## Licença

[GPL-3.0-or-later](LICENSE).
