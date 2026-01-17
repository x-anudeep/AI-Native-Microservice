from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.telemetry.metrics import PrometheusMiddleware


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.add_middleware(PrometheusMiddleware)
    app.include_router(router, prefix=settings.api_prefix)
    return app


app = create_app()
