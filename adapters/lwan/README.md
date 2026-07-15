# lwan adapter

[lwan](https://lwan.ws/) serves static files efficiently (`serve_files`) and offers
optional Mustache templates / C–Lua handlers. Use the **Vanilla** client + JSON CGI
(or in-process handler) — no Alpine/npm required.

## Layout

```text
www/
  index.html
  static/dos/dos-audit-console.css
  static/dos/dos-audit-console.iife.js
cgi-bin/
  logs.cgi     # Content-Type: application/json ; body = LogEntry[]
```

## `index.html`

```html
<!doctype html>
<html><head>
  <link rel="stylesheet" href="/static/dos/dos-audit-console.css">
</head><body>
  <div id="dos-root"></div>
  <script src="/static/dos/dos-audit-console.iife.js"></script>
  <script>
    DosAuditConsole.mount('#dos-root', {
      logsUrl: '/cgi-bin/logs.cgi',
      pollMs: 3000,
      sound: true
    });
  </script>
</body></html>
```

## Minimal `logs.cgi` (shell)

```sh
#!/bin/sh
printf 'Content-Type: application/json\r\n\r\n'
tail -n 50 /var/log/app/audit.jsonl 2>/dev/null | python3 -c '
import sys, json
rows=[]
for line in sys.stdin:
    line=line.strip()
    if line: rows.append(json.loads(line))
print(json.dumps(rows))
' || echo '[]'
```

See `examples/lwan/`.
