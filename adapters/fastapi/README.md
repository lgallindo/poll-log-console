# FastAPI adapter

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dos_audit.buffer import LogBuffer
from dos_audit.middleware_asgi import make_asgi_middleware
from dos_audit.fastapi_router import build_router
from dos_audit import static_dir

app = FastAPI()
buf = LogBuffer(50)
app.middleware("http")(make_asgi_middleware(buf))
app.include_router(build_router(buf, prefix="/api/v1"))
app.mount("/static/dos", StaticFiles(directory=static_dir()), name="dos")
```

Use Alpine or Vanilla in Jinja templates; see `examples/fastapi-app/`.
