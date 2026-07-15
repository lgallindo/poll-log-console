from __future__ import annotations

from pathlib import Path

from .buffer import LogBuffer
from . import dist_dir


def create_blueprint(buffer: LogBuffer, name: str = "dos"):
    """Flask blueprint: GET /logs JSON + static files under /static."""
    from flask import Blueprint, jsonify, send_from_directory

    bp = Blueprint(name, __name__, static_folder=str(dist_dir()), static_url_path="/static")

    @bp.get("/logs")
    def logs():
        return jsonify(buffer.list())

    @bp.get("/info")
    def info():
        import datetime
        import os
        import time

        return jsonify({
            "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": time.strftime("%Z"),
            "api_key_status": "UNKNOWN",
            "port": 0,
            "os": os.name.upper(),
            "kernel": "dos-audit-console",
        })

    return bp
