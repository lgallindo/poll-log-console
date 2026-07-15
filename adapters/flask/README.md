# Flask adapter

```python
from flask import Flask, render_template
from dos_audit.middleware_wsgi import init_audit
from dos_audit.flask_blueprint import create_blueprint

app = Flask(__name__)
buf = init_audit(app, maxlen=50, skip_prefixes=("/static", "/audit/logs", "/audit/static"))
app.register_blueprint(create_blueprint(buf), url_prefix="/audit")
```

```html
<link rel="stylesheet" href="{{ url_for('dos.static', filename='dos-audit-console.css') }}">
<div id="dos-root"></div>
<script src="{{ url_for('dos.static', filename='dos-audit-console.iife.js') }}"></script>
<script>
  DosAuditConsole.mount('#dos-root', { logsUrl: '{{ url_for("dos.logs") }}', infoUrl: '{{ url_for("dos.info") }}' });
</script>
```

See `examples/flask-app/`.
