# Harness

## KISS

```bash
# once (venv recommended)
python3 -m venv .venv
.venv/bin/pip install fastapi uvicorn

# from repo root
chmod +x harness/run.sh
./harness/run.sh
```

Starts three showcase apps, smoke-tests `/api/v1/logs` (+ status/echo/cpm), then holds until Ctrl+C.

| App | Port | URL |
|-----|------|-----|
| CP/M term | 8771 | http://127.0.0.1:8771/ |
| Net status | 8772 | http://127.0.0.1:8772/ |
| Echo lab | 8773 | http://127.0.0.1:8773/ |

Smoke only (apps already up):

```bash
PYTHONPATH=src/python python3 harness/smoke_test.py
```

Set `HARNESS_HOLD=0` to exit after smoke (CI-friendly).
