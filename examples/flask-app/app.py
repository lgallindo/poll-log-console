"""Minimal Flask example — run: PYTHONPATH=../../src/python flask --app app run"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "python"))

from flask import Flask
from dos_audit.middleware_wsgi import init_audit
from dos_audit.flask_blueprint import create_blueprint

app = Flask(__name__)
buf = init_audit(app, skip_prefixes=("/static", "/audit/logs", "/audit/static"))
app.register_blueprint(create_blueprint(buf), url_prefix="/audit")


@app.get("/")
def index():
    return f"""<!doctype html><html><head>
<link rel="stylesheet" href="/audit/static/dos-audit-console.css">
</head><body style="background:#111;color:#ccc;padding:2rem">
<h1>Flask + dos-audit-console</h1>
<div id="dos-root"></div>
<script src="/audit/static/dos-audit-console.iife.js"></script>
<script>
DosAuditConsole.mount('#dos-root', {{ logsUrl: '/audit/logs', infoUrl: '/audit/info' }});
</script></body></html>"""
