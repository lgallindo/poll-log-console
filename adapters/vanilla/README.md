# Vanilla JS adapter

Lowest common denominator — works with lwan, Flask static, CDN-free pages.

```html
<link rel="stylesheet" href="dos-audit-console.css">
<div id="dos-root"></div>
<script src="dos-audit-console.iife.js"></script>
<script>
  const ui = DosAuditConsole.mount('#dos-root', { logsUrl: '/logs', pollMs: 3000 });
  ui.toast('hello', 'sys');
</script>
```
