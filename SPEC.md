# SPEC — dos-audit-console v1

## LogEntry

```json
{
  "time": "14:32:01.423",
  "msg": "[REQ] GET /api/v1/vault/executions",
  "type": "req"
}
```

| Field | Type | Notes |
|-------|------|--------|
| `time` | string | Display clock (`HH:MM:SS.mmm` or locale time) |
| `msg` | string | Free text |
| `type` | string | `req` \| `res` \| `sys` \| `err` |

Optional (ignored by v1 clients if absent): `id`, `seq`, `level`.

## Endpoints

| Method | Path | Response |
|--------|------|----------|
| `GET` | `{prefix}/logs` | `LogEntry[]` (ring window; default maxlen 50) |
| `GET` | `{prefix}/info` | Optional boot metadata object |

Recommended: **skip auditing** `GET …/logs` and static asset paths in middleware
so the poller does not flood the buffer.

## Client options

```js
{
  logsUrl: '/api/v1/logs',
  infoUrl: '/api/v1/info',   // optional
  pollMs: 3000,
  storageKey: 'dos_logs',
  maxLocalLogs: 500,
  sound: true,
  title: 'C:\\SYSTEM\\AUDIT_LOG.EXE',
  bootLines: null,           // optional string[] override
  actions: ['copy', 'clear'] // 'kg' is host-specific; omitted by default
}
```

## Transport

v1 = **HTTP polling**. SSE may be added later without changing `LogEntry`.

## UI commands

| Input | Action |
|-------|--------|
| `:w` | Copy logs to clipboard |
| `:q` | Minimize |
| `cls` | Clear logs + storage |
