from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Test Actions API", description="Простой тестовый бэкенд")


@app.get("/")
def root() -> JSONResponse:
    return JSONResponse({"message": "Сервер работает"})


@app.get("/time")
def server_time() -> JSONResponse:
    now = datetime.now()
    return JSONResponse(
        {
            "utc": now.astimezone(timezone.utc).isoformat(),
            "local": now.astimezone().isoformat(),
            "timezone": str(now.astimezone().tzinfo or "unknown"),
        }
    )