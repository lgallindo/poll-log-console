# hardcopy-console

![hardcopy-console — C:\>](docs/media/brand/banner-dos-hero.png)

**Idiomas:** [English (en_US)](README.md) · [Português (pt_BR)](README.pt-BR.md) · [toki pona](README.tok.md)

**Licença:** [GPL-3.0-or-later](LICENSE) · **GitHub:** `git@github.com:lgallindo/hardcopy-console.git`

## O que é isto?

Um console na página que observa um log JSON via HTTP. Sua aplicação mantém uma lista curta de linhas; este widget faz polling dessa lista e mostra tudo num painel estilo terminal, com timestamps.

Não é um emulador de DOS ou CP/M — só o visual e a UI de polling. O projeto é **hardcopy-console** (API JS `HardcopyConsole`).

![](docs/media/demo/pipeline-dag.gif)

### Casos de uso

- Acompanhar atividade de API e da página enquanto desenvolve
- Colocar um painel de auditoria compartilhado numa página Flask, FastAPI ou estática
- Demos de workshop do fluxo de requisições sem uma stack completa de observabilidade
- Temas de laboratório que reutilizam o mesmo console (CP/M-ish, Simple.css, Water.css, …)

**Enterprise** (secundário):

- **Mesa de release / deploy** — promote, health check e rollback como linhas com horário numa página interna de ops:

  ![Auditoria de deploy enterprise](docs/media/demo/enterprise-deploy-audit.png)

- **Back-office / ações de CRM** — quem mudou flags de risco, overrides e campos de conta, com horários que dá para reler:

  ![Auditoria de back-office enterprise](docs/media/demo/enterprise-backoffice-audit.png)

**Chat / e-mail:**

- Mensagens de entrada como linhas (`mail from…`, `chat #general: …`) para a história rolar num só lugar em vez de popups:

  ![Monitor de e-mail e chat](docs/media/demo/funny-mail-chat-monitor.png)

## Por que existe

Eu fiz isto porque odeio toasts. Preciso de notificações com horário para entender minhas apps. Pode ser trauma da época em que uma ferramenta de pipeline do meu empregador tinha toasts verde-lima como único “log”. A única coisa que eu odeio mais que toast são frameworks JS pesados — então Vanilla JS.

---

## Exemplo de monitor

Sua app acrescenta linhas a um ring buffer. O widget chama `GET /api/v1/logs`, recebe um array JSON e pinta.

```json
{"time": "14:32:01.423", "msg": "[REQ] GET /health", "type": "req"}
```

(`type` costuma ser `req`, `res`, `sys` ou `err` — ver [SPEC.pt-BR.md](SPEC.pt-BR.md) · [en](SPEC.md) · [tok](SPEC.tok.md).)

**Cliente:** entregue CSS + IIFE de `dist/`, monte num `div`, defina `logsUrl`:

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

**Servidor:** devolva esse array JSON. Python: [adapters/](adapters/) (`LogBuffer`, Flask, FastAPI). Não audite cada poll de `/logs`, ou o console se afoga.

---

## Veja funcionando

READMEs do GitHub não executam JavaScript. Estes são registros dos apps de exemplo; rode os ao vivo com o harness abaixo.

**Echo lab** — uma mensagem cai no log polled:

![Demo do monitor echo lab](docs/media/demo/monitor-echo.gif)

[`examples/echo-lab/`](examples/echo-lab/) → http://127.0.0.1:8773/ (depois de `./harness/run.sh`)

**Net status** — atualiza info do host; cada refresh vai para o log:

![Demo do monitor net status](docs/media/demo/monitor-net-status.gif)

[`examples/net-status/`](examples/net-status/) → http://127.0.0.1:8772/

### Truques do console

Minimizar / expandir pelo cabeçalho (`:q` também minimiza). Eventos novos podem piscar a luz do header e acrescentar uma linha com horário (o anti-toast). O painel é `position: fixed` — mova com CSS (`left` / `right` / `bottom`) se quiser outro canto.

![Minimizar, luz de toast e reposicionar](docs/media/demo/console-tricks.gif)

---

## Como ligar

1. Use `dist/hardcopy-console.css` e `dist/hardcopy-console.iife.js`.
2. Coloque um `div` de montagem (qualquer seletor).
3. Chame `HardcopyConsole.mount` com pelo menos `logsUrl` (e em geral `pollMs`).
4. Sirva JSON `LogEntry[]` — helpers Python em `src/python/hardcopy_console/` e [adapters/](adapters/).
5. Exclua `/logs` e caminhos estáticos do middleware de auditoria.
6. Rode `./harness/run.sh` para os cinco demos locais (portas 8771–8775).

Depois use o início rápido e o índice de exemplos abaixo.

---

## Objetivos

- CSS puro + IIFE JS (sem Alpine, Tailwind ou npm obrigatórios em runtime)
- Encaixe em Flask, FastAPI (Jinja), Alpine.js, JS puro, HTMX e [lwan](https://lwan.ws/)
- Contrato JSON `LogEntry` compartilhado + `LogBuffer` / middleware Python opcional

## Início rápido (vanilla)

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

Veja [SPEC.pt-BR.md](SPEC.pt-BR.md) ([en](SPEC.md) · [tok](SPEC.tok.md)) e [adapters/](adapters/).

---

## Aplicativos de exemplo (índice)

| Preview | App | Caminho | Porta | Função |
|---------|-----|---------|-------|--------|
| ![CP/M term](docs/media/apps/thumbs/cpm-term.png) | **CP/M term** | [`examples/cpm-term/`](examples/cpm-term/) | **8771** | Prompt CP/M de brincadeira (`DIR`, `TYPE`, `HELP`); comandos vão para o log |
| ![Net status](docs/media/apps/thumbs/net-status.png) | **Net status** | [`examples/net-status/`](examples/net-status/) | **8772** | Hostname, endereços, plataforma, PID; refresh entra no log |
| ![Echo lab](docs/media/apps/thumbs/echo-lab.png) | **Echo lab** | [`examples/echo-lab/`](examples/echo-lab/) | **8773** | POST de mensagem no ring buffer + toast/LED local |
| ![Simple.css](docs/media/apps/thumbs/simple-css.png) | **Simple.css** | [`examples/simple-css/`](examples/simple-css/) | **8774** | Console numa página [Simple.css](https://simplecss.org/) |
| ![Water.css](docs/media/apps/thumbs/water-css.png) | **Water.css** | [`examples/water-css/`](examples/water-css/) | **8775** | Console numa página [Water.css](https://watercss.kognise.dev/) |

Também existem stubs: `examples/vanilla-standalone/`, `alpine-standalone/`, `flask-app/`, `fastapi-app/`, `htmx-poll/`, `lwan/`.

### Subir os exemplos

```bash
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn
chmod +x harness/run.sh
./harness/run.sh
```

- http://127.0.0.1:8771/ — CP/M  
- http://127.0.0.1:8772/ — Status de rede  
- http://127.0.0.1:8773/ — Echo lab  
- http://127.0.0.1:8774/ — Simple.css  
- http://127.0.0.1:8775/ — Water.css  

Ou um de cada vez:

```bash
cd examples/cpm-term && PYTHONPATH=../../src/python python3 app.py
cd examples/net-status && PYTHONPATH=../../src/python python3 app.py
cd examples/echo-lab && PYTHONPATH=../../src/python python3 app.py
cd examples/simple-css && PYTHONPATH=../../src/python python3 app.py
cd examples/water-css && PYTHONPATH=../../src/python python3 app.py
```

Detalhes: [harness/README.md](harness/README.md).

---

## Estrutura

| Caminho | Papel |
|---------|--------|
| `src/` | CSS, JS core + adapters, fragmentos HTML, pacote Python |
| `dist/` | CSS + IIFE prontos offline |
| `adapters/` | Notas por host (Flask, FastAPI, Alpine, Vanilla, HTMX, lwan) |
| `examples/` | Aplicativos de exemplo |
| `harness/` | Subir e verificar os exemplos |
| `tests/` | Unitários + notas e2e |
| `docs/media/brand/` | Banner GitHub + mark + shorts sociais |
| `docs/media/demo/` | Demos do README e stills de casos de uso |

## Licença

[GPL-3.0-or-later](LICENSE) — ver também [COPYING.short](COPYING.short).
