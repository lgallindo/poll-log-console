# dos-audit-console

Reusable **PC-DOS audit / notification console** extracted from
[philological-agents](https://bitbucket.org/hustles/philological-agents) `lab/index.html`.

## Goals

- Static-first: pure CSS + IIFE JS (no mandatory Alpine, Tailwind, or npm at runtime)
- Importable into Flask, FastAPI (Jinja), Alpine.js, Vanilla JS, HTMX, and [lwan](https://lwan.ws/)
- Shared `LogEntry` JSON contract + optional Python `LogBuffer` / middleware

## Quick start (Vanilla)

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

See `SPEC.md` and `adapters/*/README.md`.

## Layout

- `src/` — source CSS, JS core + adapters, HTML fragments, Python package
- `dist/` — offline-ready build artifacts (committed for research use)
- `adapters/` — drop-in notes per host framework
- `examples/` — minimal apps
- `tests/` — unit + e2e (Playwright Group D port)

## License

Same as the originating research context unless otherwise stated.
