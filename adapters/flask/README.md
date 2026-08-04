# Flask adapter

```python
from flask import Flask, render_template
from hardcopy_console.middleware_wsgi import init_audit
from hardcopy_console.flask_blueprint import create_blueprint

app = Flask(__name__)
buf = init_audit(app, maxlen=50, skip_prefixes=("/static", "/audit/logs", "/audit/static"))
app.register_blueprint(create_blueprint(buf), url_prefix="/audit")
```

```html
<link rel="stylesheet" href="{{ url_for('dos.static', filename='hardcopy-console.css') }}">
<div id="hardcopy-root"></div>
<script src="{{ url_for('dos.static', filename='hardcopy-console.iife.js') }}"></script>
<script>
  HardcopyConsole.mount('#hardcopy-root', { logsUrl: '{{ url_for("dos.logs") }}', infoUrl: '{{ url_for("dos.info") }}' });
</script>
```

See `examples/flask-app/`.
