# Harness

Start the sample apps and run a short health check.

```bash
python3 -m venv .venv
.venv/bin/pip install fastapi uvicorn
chmod +x harness/run.sh
./harness/run.sh
```

| App | Port | URL |
|-----|------|-----|
| CP/M term | 8771 | http://127.0.0.1:8771/ |
| Net status | 8772 | http://127.0.0.1:8772/ |
| Echo lab | 8773 | http://127.0.0.1:8773/ |
| Simple.css | 8774 | http://127.0.0.1:8774/ |
| Water.css | 8775 | http://127.0.0.1:8775/ |

Exit after the health check: `HARNESS_HOLD=0 ./harness/run.sh`

### Regenerate media

Optional. Needs Playwright Chromium and ImageMagick (`convert`).

```bash
.venv/bin/pip install playwright
.venv/bin/playwright install chromium
# system: imagemagick
HARNESS_HOLD=1 ./harness/run.sh   # or let capture_media start apps
.venv/bin/python harness/capture_media.py
```

Writes `docs/media/hero.png` and `docs/media/apps/` (full + thumbs).
