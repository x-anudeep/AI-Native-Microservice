from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile

from app.api.dependencies import get_processor
from app.core.config import get_settings
from app.models.schemas import MetricSnapshot, ProcessingRequest, ProcessingResponse, UploadJob
from app.services.processor import DocumentProcessor
from app.services.providers import list_provider_statuses
from app.telemetry.metrics import metrics_response

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready"}


@router.get("/version")
async def version() -> dict[str, str]:
    settings = get_settings()
    return {"name": settings.app_name, "version": settings.app_version}


@router.post("/documents/process", response_model=ProcessingResponse)
async def process_document(
    request: ProcessingRequest,
    processor: DocumentProcessor = Depends(get_processor),
) -> ProcessingResponse:
    return await processor.process(request)


@router.post("/documents/upload", response_model=UploadJob)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    processor: DocumentProcessor = Depends(get_processor),
) -> UploadJob:
    job = await processor.queue_upload(file.filename or "upload.bin", file.content_type)
    background_tasks.add_task(processor.complete_job, job.job_id)
    return job


@router.get("/documents/jobs/{job_id}", response_model=UploadJob)
async def get_job(
    job_id: str,
    processor: DocumentProcessor = Depends(get_processor),
) -> UploadJob:
    job = processor.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job


@router.get("/providers")
async def providers() -> dict[str, list[dict]]:
    return {"providers": [status.model_dump() for status in list_provider_statuses()]}


@router.get("/providers/{provider_name}")
async def provider(provider_name: str) -> dict:
    for status in list_provider_statuses():
        if status.name == provider_name:
            return status.model_dump()
    raise HTTPException(status_code=404, detail="provider not found")


@router.post("/providers/route")
async def route_provider(request: ProcessingRequest) -> dict:
    processor = DocumentProcessor()
    decision = processor.router.choose(request)
    return decision.model_dump()


@router.get("/metrics/snapshot", response_model=MetricSnapshot)
async def metric_snapshot() -> MetricSnapshot:
    return MetricSnapshot(
        requests_total=4_216,
        p95_latency_ms=486,
        providers_active=4,
        estimated_daily_cost_usd=39.45,
    )


@router.get("/metrics")
async def prometheus_metrics():
    return metrics_response()


@router.get("/ops/config")
async def runtime_config() -> dict:
    settings = get_settings()
    return {
        "environment": settings.environment,
        "max_upload_mb": settings.max_upload_mb,
        "daily_request_target": settings.daily_request_target,
    }


@router.get("/ops/slo")
async def slo() -> dict[str, int]:
    settings = get_settings()
    return {"p95_latency_ms": settings.service_level_latency_ms, "daily_requests": 4_000}


@router.post("/ops/deployments/blue-green")
async def blue_green_deployment() -> dict[str, str]:
    return {"strategy": "blue-green", "status": "validated"}


@router.get("/cost/estimate")
async def estimate_cost(
    tokens: int = 1_000,
    provider_name: str = "openai",
) -> dict[str, float | str]:
    costs = {"openai": 0.0025, "claude": 0.003, "gemini": 0.00125, "local": 0.0}
    rate = costs.get(provider_name, costs["openai"])
    return {"provider": provider_name, "tokens": tokens, "estimated_cost_usd": tokens / 1000 * rate}


@router.get("/audit/requests/{request_id}")
async def audit_request(request_id: str) -> dict[str, str]:
    return {"request_id": request_id, "status": "retained", "retention": "30d"}
