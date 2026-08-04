# FastAPI adapter

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from hardcopy_console.buffer import LogBuffer
from hardcopy_console.middleware_asgi import make_asgi_middleware
from hardcopy_console.fastapi_router import build_router
from hardcopy_console import static_dir

app = FastAPI()
buf = LogBuffer(50)
app.middleware("http")(make_asgi_middleware(buf))
app.include_router(build_router(buf, prefix="/api/v1"))
app.mount("/static/hardcopy", StaticFiles(directory=static_dir()), name="hardcopy")
```

Use Alpine or Vanilla in Jinja templates; see `examples/fastapi-app/`.
