#!/usr/bin/env bash
# KISS harness — start sample apps and smoke-check /api/v1/logs
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT/src/python${PYTHONPATH:+:$PYTHONPATH}"
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
else
  PY="python3"
fi
PIDS=()

cleanup() {
  for p in "${PIDS[@]:-}"; do kill "$p" 2>/dev/null || true; done
}
trap cleanup EXIT

need_py() {
  "$PY" -c "import fastapi, uvicorn" 2>/dev/null || {
    echo "Install deps: $PY -m pip install fastapi uvicorn"
    echo "Or: python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn"
    exit 1
  }
}

start_app() {
  local name="$1" port="$2" script="$3"
  echo "→ starting $name on :$port"
  "$PY" "$script" >/tmp/plc-"$name".log 2>&1 &
  PIDS+=($!)
}

wait_http() {
  local url="$1" n=0
  until curl -fsS "$url" >/dev/null 2>&1; do
    n=$((n + 1))
    if [[ $n -gt 40 ]]; then
      echo "timeout waiting for $url"
      cat /tmp/plc-*.log 2>/dev/null | tail -40 || true
      return 1
    fi
    sleep 0.25
  done
}

need_py

start_app cpm-term 8771 "$ROOT/examples/cpm-term/app.py"
start_app net-status 8772 "$ROOT/examples/net-status/app.py"
start_app echo-lab 8773 "$ROOT/examples/echo-lab/app.py"

wait_http "http://127.0.0.1:8771/api/v1/logs"
wait_http "http://127.0.0.1:8772/api/v1/status"
wait_http "http://127.0.0.1:8773/"

"$PY" "$ROOT/harness/smoke_test.py"

echo
echo "OK — apps running (Ctrl+C to stop):"
echo "  CP/M term     http://127.0.0.1:8771/"
echo "  Net status    http://127.0.0.1:8772/"
echo "  Echo lab      http://127.0.0.1:8773/"
echo
if [[ "${HARNESS_HOLD:-1}" == "1" ]]; then
  wait
fi
