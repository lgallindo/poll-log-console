#!/usr/bin/env python3
"""Smoke checks for the three showcase apps + log JSON contract."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

APPS = [
    ("cpm-term", "http://127.0.0.1:8771", ["/api/v1/logs", "/"]),
    ("net-status", "http://127.0.0.1:8772", ["/api/v1/logs", "/api/v1/status", "/"]),
    ("echo-lab", "http://127.0.0.1:8773", ["/api/v1/logs", "/"]),
]


def get(url: str) -> tuple[int, bytes]:
    with urllib.request.urlopen(url, timeout=5) as r:
        return r.status, r.read()


def main() -> int:
    failed = 0
    for name, base, paths in APPS:
        for path in paths:
            url = base + path
            try:
                status, body = get(url)
            except urllib.error.URLError as e:
                print(f"FAIL {name} {url}: {e}")
                failed += 1
                continue
            if status != 200:
                print(f"FAIL {name} {url}: HTTP {status}")
                failed += 1
                continue
            if path.endswith("/logs"):
                data = json.loads(body.decode())
                if not isinstance(data, list):
                    print(f"FAIL {name} logs not a list")
                    failed += 1
                    continue
            print(f"ok   {name} {path}")

    # exercise echo + cpm write paths
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8773/api/v1/echo",
            data=json.dumps({"message": "harness", "type": "sys"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            assert r.status == 200
        print("ok   echo-lab POST /api/v1/echo")
        req = urllib.request.Request(
            "http://127.0.0.1:8771/api/v1/cpm",
            data=json.dumps({"cmd": "DIR"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            assert r.status == 200
        print("ok   cpm-term POST /api/v1/cpm")
    except Exception as e:
        print(f"FAIL write paths: {e}")
        failed += 1

    if failed:
        print(f"{failed} failure(s)")
        return 1
    print("smoke: all green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
