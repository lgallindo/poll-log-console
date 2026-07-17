# Screenshot harness

**Purpose:** keep demo pages running so you can take **pretty screenshots** of
poll-log-console on real layouts. It is **not** meant for CI badges, repo
header widgets, or “funny” automated marketing hooks.

## KISS

```bash
python3 -m venv .venv
.venv/bin/pip install fastapi uvicorn
chmod +x harness/run.sh
./harness/run.sh
```

Leaves five apps up until Ctrl+C. Open each URL, expand the console, trigger
an action, then capture the viewport (browser or OS screenshot tool).

| App | Port | URL |
|-----|------|-----|
| CP/M term | 8771 | http://127.0.0.1:8771/ |
| Net status | 8772 | http://127.0.0.1:8772/ |
| Echo lab | 8773 | http://127.0.0.1:8773/ |
| Simple.css | 8774 | http://127.0.0.1:8774/ |
| Water.css | 8775 | http://127.0.0.1:8775/ |

Optional local dump folder (ignored by git): `screenshots/`

Exit after health check only: `HARNESS_HOLD=0 ./harness/run.sh`
