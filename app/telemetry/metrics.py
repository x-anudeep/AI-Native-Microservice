import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_COUNT = Counter(
    "ai_native_requests_total",
    "Total HTTP requests processed by the service.",
    ["method", "path", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "ai_native_request_latency_seconds",
    "HTTP request latency by route.",
    ["method", "path"],
    buckets=(0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0),
)
PROVIDER_COST = Counter(
    "ai_native_provider_cost_usd_total",
    "Estimated provider cost in USD.",
    ["provider", "model"],
)
PROVIDER_SELECTION = Counter(
    "ai_native_provider_selections_total",
    "AI provider selections by provider and model.",
    ["provider", "model"],
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        path = request.url.path
        latency = time.perf_counter() - start
        REQUEST_COUNT.labels(request.method, path, str(response.status_code)).inc()
        REQUEST_LATENCY.labels(request.method, path).observe(latency)
        return response


def record_provider_selection(provider: str, model: str, estimated_cost_usd: float) -> None:
    PROVIDER_SELECTION.labels(provider, model).inc()
    PROVIDER_COST.labels(provider, model).inc(estimated_cost_usd)


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
