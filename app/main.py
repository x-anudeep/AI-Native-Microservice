from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import get_settings
from app.telemetry.metrics import PrometheusMiddleware

STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.add_middleware(PrometheusMiddleware)
    app.include_router(router, prefix=settings.api_prefix)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", include_in_schema=False)
    async def dashboard() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/dashboard", include_in_schema=False)
    async def dashboard_alias() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    return app


app = create_app()
