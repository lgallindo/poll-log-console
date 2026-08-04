# Vanilla JS adapter

Lowest common denominator — works with lwan, Flask static, CDN-free pages.

```html
<link rel="stylesheet" href="hardcopy-console.css">
<div id="hardcopy-root"></div>
<script src="hardcopy-console.iife.js"></script>
<script>
  const ui = HardcopyConsole.mount('#hardcopy-root', { logsUrl: '/logs', pollMs: 3000 });
  ui.toast('hello', 'sys');
</script>
```
