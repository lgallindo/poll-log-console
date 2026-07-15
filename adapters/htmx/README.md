# HTMX adapter

Server renders log lines; HTMX polls an HTML partial.

```html
<link rel="stylesheet" href="dos-audit-console.css">
<div class="dos-console">
  <div class="dos-header"><div class="notif-light"></div><span>C:\SYSTEM\AUDIT_LOG.EXE</span></div>
  <div id="dos-body" class="dos-body"
       hx-get="/audit/logs.html"
       hx-trigger="every 3s"
       hx-swap="innerHTML"></div>
</div>
<script src="dos-audit-console.iife.js"></script>
<script>DosAuditConsole.bindHtmxBeep('#dos-body');</script>
```

Partial example:

```html
{% for log in logs %}
<div class="dos-line"><span class="dos-line-time">{{ log.time }}</span>
<span class="dos-msg-{{ log.type }}">{{ log.msg }}</span></div>
{% endfor %}
```
