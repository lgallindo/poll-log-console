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
| **CP/M term** | [`examples/cpm-term/`](examples/cpm-term/) | **8771** | Prompt CP/M de brincadeira (`DIR`, `TYPE`, `HELP`); comandos vão para o log |
| **Net status** | [`examples/net-status/`](examples/net-status/) | **8772** | Hostname, endereços, plataforma, PID; atualizar gera auditoria |
| **Echo lab** | [`examples/echo-lab/`](examples/echo-lab/) | **8773** | POST de mensagem no buffer + toast/LED local |

Também existem stubs: `vanilla-standalone/`, `alpine-standalone/`, `flask-app/`, `fastapi-app/`, `htmx-poll/`, `lwan/`.

### KISS — subir os três apps de vitrine

```bash
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn
chmod +x harness/run.sh
./harness/run.sh
```

Abra:

- http://127.0.0.1:8771/ — CP/M  
- http://127.0.0.1:8772/ — Status de rede  
- http://127.0.0.1:8773/ — Echo lab  

Um por vez:

```bash
cd examples/cpm-term && PYTHONPATH=../../src/python python3 app.py
cd examples/net-status && PYTHONPATH=../../src/python python3 app.py
cd examples/echo-lab && PYTHONPATH=../../src/python python3 app.py
```

Detalhes: [harness/README.md](harness/README.md).  
Só smoke e sair: `HARNESS_HOLD=0 ./harness/run.sh`

---

## Estrutura

| Caminho | Papel |
|---------|--------|
| `src/` | CSS, JS, HTML, pacote Python |
| `dist/` | Artefatos offline |
| `adapters/` | Notas por framework |
| `examples/` | Aplicativos de exemplo |
| `harness/` | Subir + smoke-test |
| `tests/` | Testes |

## Licença

[GPL-3.0-or-later](LICENSE).
