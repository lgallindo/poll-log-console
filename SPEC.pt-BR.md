# SPEC — hardcopy-console v1

**Idiomas:** [English (en_US)](SPEC.md) · [Português (pt_BR)](SPEC.pt-BR.md) · [toki pona](SPEC.tok.md)

**Público:** integradores (app host + montagem da UI). Não é para usuários finais.

**Objetivo deste doc:** passos miúdos e exemplos copy-paste para ligar um console funcional sem ler o README inteiro antes. Demos mais profundas em [`examples/`](examples/) e [`adapters/`](adapters/).

---

## Passos miúdos (ponta a ponta)

Faça nesta ordem. Depois do passo 5 você deve ver linhas no painel estilo DOS.

### 1. Servir os assets estáticos

Publique (ou monte) os arquivos buildados de `dist/`:

| Arquivo | Papel |
|------|------|
| `hardcopy-console.css` | Estilos |
| `hardcopy-console.iife.js` | Global do browser `HardcopyConsole` |

**Helper Python** (caminho desse diretório):

```python
from hardcopy_console import static_dir
# ex. FastAPI: app.mount("/static/hardcopy", StaticFiles(directory=static_dir()), …)
```

### 2. Manter um anel de objetos `LogEntry` no servidor

Formato mínimo (JSON):

```json
{
  "time": "14:32:01.423",
  "msg": "[REQ] GET /api/v1/vault/executions",
  "type": "req"
}
```

`type` deve ser um de: `req` | `res` | `sys` | `err`.

**Python:**

```python
from hardcopy_console.buffer import LogBuffer

buf = LogBuffer(50)  # janela maxlen devolvida por GET /logs
buf.append({
    "time": "14:32:01.423",
    "msg": "[SYS] boot",
    "type": "sys",
})
```

**Qualquer linguagem:** uma lista/deque desses objetos basta. Campos opcionais `id`, `seq`, `level` são ignorados pelos clientes v1.

### 3. Expor `GET …/logs` (e opcionalmente `GET …/info`)

| Método | Caminho | Resposta |
|--------|------|----------|
| `GET` | `{prefix}/logs` | `LogEntry[]` (janela atual do anel) |
| `GET` | `{prefix}/info` | Objeto opcional de metadados de boot (qualquer objeto JSON) |

**Na mão (qualquer stack)** — exemplo de corpo para `/api/v1/logs`:

```json
[
  {"time": "14:32:01.423", "msg": "[SYS] boot", "type": "sys"},
  {"time": "14:32:02.100", "msg": "[REQ] GET /health", "type": "req"}
]
```

**FastAPI (router da biblioteca):**

```python
from hardcopy_console.fastapi_router import build_router

app.include_router(build_router(buf, prefix="/api/v1"))
# → GET /api/v1/logs , GET /api/v1/info
```

**Flask:** ver [`adapters/flask/`](adapters/flask/) (`create_blueprint`).

**Crítico:** **não** faça audit/`append` em `GET …/logs` nem em caminhos de assets estáticos, senão o poller inundará o buffer. Pule esses prefixos no middleware.

```python
from hardcopy_console.middleware_asgi import make_asgi_middleware

app.middleware("http")(
    make_asgi_middleware(buf, skip_prefixes=("/static", "/api/v1/logs"))
)
```

### 4. Colocar um nó de mount no HTML e carregar CSS/JS

```html
<link rel="stylesheet" href="/static/hardcopy/hardcopy-console.css">
<div id="hardcopy-root"></div>
<script src="/static/hardcopy/hardcopy-console.iife.js"></script>
```

Os caminhos devem bater com o mount de `static_dir()` / `dist/`.

### 5. Chamar `HardcopyConsole.mount`

```html
<script>
  const ui = HardcopyConsole.mount('#hardcopy-root', {
    logsUrl: '/api/v1/logs',   // obrigatório para polling
    infoUrl: '/api/v1/info',   // opcional
    pollMs: 3000,
    title: 'C:\\> MONITOR'
  });

  // Opcional: linha só local (não vai ao servidor)
  ui.toast('olá do host', 'sys');
</script>
```

Abra a página, expanda o console se estiver minimizado, espere um `pollMs` — as linhas do servidor devem aparecer.

### 6. Provar com um sample local (opcional)

```bash
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn
./harness/run.sh
# http://127.0.0.1:8773/ — Echo lab posta no anel + monta o console
```

Ou um app só: `cd examples/echo-lab && PYTHONPATH=../../src/python python3 app.py`

---

## Servidor mínimo sem o pacote Python

Qualquer stack HTTP serve se devolver `LogEntry[]` no seu `logsUrl`.

**Node (esboço):**

```js
const logs = [];
app.get('/api/v1/logs', (_req, res) => res.json(logs));

// em outro lugar, quando algo acontece:
logs.push({
  time: new Date().toISOString().slice(11, 23),
  msg: '[REQ] GET /x',
  type: 'req',
});
if (logs.length > 50) logs.shift();
```

Combine com o mesmo mount HTML dos passos 4–5.

---

## Opções do cliente

Todas as chaves são opcionais, mas quase sempre você define `logsUrl` (e em geral `pollMs`).

```js
{
  logsUrl: '/api/v1/logs',
  infoUrl: '/api/v1/info',   // opcional; omita se não houver /info
  pollMs: 3000,
  storageKey: 'hardcopy_logs',
  maxLocalLogs: 500,
  sound: true,
  title: 'C:\\> MONITOR',
  bootLines: null,           // string[] opcional para texto de boot
  actions: ['copy', 'clear'] // 'kg' é específico do host; omitido por padrão
}
```

O default de `title` no IIFE ainda é `C:\SYSTEM\AUDIT_LOG.EXE`; prefira sobrescrever com um título estilo prompt (ex. `C:\> MONITOR`) para a face de marca atual.

---

## Transporte

v1 = **polling HTTP** de `logsUrl`. SSE pode vir depois sem mudar `LogEntry`.

---

## Comandos da UI (entrada do console)

| Entrada | Ação |
|-------|--------|
| `:w` | Copiar logs para a área de transferência |
| `:q` | Minimizar |
| `cls` | Limpar logs + storage |

---

## LogEntry (referência)

| Campo | Tipo | Notas |
|-------|------|--------|
| `time` | string | Relógio de exibição (`HH:MM:SS.mmm` ou hora local) |
| `msg` | string | Texto livre |
| `type` | string | `req` \| `res` \| `sys` \| `err` |

Opcionais (ignorados pelos clientes v1 se ausentes): `id`, `seq`, `level`.

---

## Próximos adapters

| Stack | Onde |
|-------|--------|
| Vanilla / IIFE | [`adapters/vanilla/`](adapters/vanilla/) |
| Alpine | [`adapters/alpine/`](adapters/alpine/) |
| HTMX | [`adapters/htmx/`](adapters/htmx/) |
| FastAPI | [`adapters/fastapi/`](adapters/fastapi/) |
| Flask | [`adapters/flask/`](adapters/flask/) |
| lwan | [`adapters/lwan/`](adapters/lwan/) |
