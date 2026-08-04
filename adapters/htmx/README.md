# HTMX adapter

Server renders log lines; HTMX polls an HTML partial.

```html
<link rel="stylesheet" href="hardcopy-console.css">
<div class="hardcopy-console-ui">
  <div class="hardcopy-header"><div class="notif-light"></div><span>C:\SYSTEM\AUDIT_LOG.EXE</span></div>
  <div id="hardcopy-body" class="hardcopy-body"
       hx-get="/audit/logs.html"
       hx-trigger="every 3s"
       hx-swap="innerHTML"></div>
</div>
<script src="hardcopy-console.iife.js"></script>
<script>HardcopyConsole.bindHtmxBeep('#hardcopy-body');</script>
```

Partial example:

```html
{% for log in logs %}
<div class="hardcopy-line"><span class="hardcopy-line-time">{{ log.time }}</span>
<span class="hardcopy-msg-{{ log.type }}">{{ log.msg }}</span></div>
{% endfor %}
```
