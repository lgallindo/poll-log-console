# HTMX poll partial example notes

Serve a route that returns HTML log lines and wire:

```html
<div id="hardcopy-body" class="hardcopy-body"
     hx-get="/audit/logs.html" hx-trigger="every 3s" hx-swap="innerHTML"></div>
```

See `adapters/htmx/README.md`.
