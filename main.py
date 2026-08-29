from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

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


@app.get("/datetime")
def server_datetime() -> JSONResponse:
    now = datetime.now()
    return JSONResponse(
        {
            "utc": now.astimezone(timezone.utc).isoformat(),
            "local": now.astimezone().isoformat(),
            "timezone": str(now.astimezone().tzinfo or "unknown"),
        }
    )


@app.get("/convert-time")
def convert_time(to_tz: str, from_tz: str = "UTC", time: datetime | None = None) -> JSONResponse:
    try:
        source = ZoneInfo(from_tz)
        target = ZoneInfo(to_tz)
    except ZoneInfoNotFoundError as exc:
        return JSONResponse(
            {"error": f"Неизвестный часовой пояс: {exc.args[0]}"},
            status_code=400,
        )

    if time is None:
        time = datetime.now()
    if time.tzinfo is None:
        time = time.replace(tzinfo=source)

    converted = time.astimezone(target)
    offset = converted.strftime("%z")
    if offset:
        offset = f"{offset[:3]}:{offset[3:]}"
    return JSONResponse(
        {
            "time": converted.isoformat(),
            "from": from_tz,
            "to": to_tz,
            "offset": offset or None,
        }
    )