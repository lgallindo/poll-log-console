# Alpine.js adapter

```html
<link rel="stylesheet" href="/path/to/hardcopy-console.css">
<script defer src="/path/to/hardcopy-console.iife.js"></script>
<script defer src="/path/to/alpine.min.js"></script>
<script>
  document.addEventListener('alpine:init', () => {
    HardcopyConsole.registerAlpine(Alpine);
  });
</script>
<div x-data="hardcopyConsole({ logsUrl: '/api/v1/logs', infoUrl: '/api/v1/info' })" x-init="init()">
  <!-- paste dist/widget.alpine.html here -->
</div>
```

Host apps can emit `window.dispatchEvent(new CustomEvent('hardcopy:toast', { detail: { message, type } }))`.
