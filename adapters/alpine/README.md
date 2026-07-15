# Alpine.js adapter

```html
<link rel="stylesheet" href="/path/to/dos-audit-console.css">
<script defer src="/path/to/dos-audit-console.iife.js"></script>
<script defer src="/path/to/alpine.min.js"></script>
<script>
  document.addEventListener('alpine:init', () => {
    DosAuditConsole.registerAlpine(Alpine);
  });
</script>
<div x-data="dosAuditConsole({ logsUrl: '/api/v1/logs', infoUrl: '/api/v1/info' })" x-init="init()">
  <!-- paste dist/widget.alpine.html here -->
</div>
```

Host apps can emit `window.dispatchEvent(new CustomEvent('dos:toast', { detail: { message, type } }))`.
