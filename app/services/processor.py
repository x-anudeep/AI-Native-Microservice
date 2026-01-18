from app.models.schemas import ProcessingRequest, ProcessingResponse, UploadJob, WorkloadType
from app.services.provider_router import ProviderRouter
from app.telemetry.metrics import record_provider_selection


class DocumentProcessor:
    def __init__(self, router: ProviderRouter | None = None) -> None:
        self.router = router or ProviderRouter()
        self.jobs: dict[str, UploadJob] = {}

    async def process(self, request: ProcessingRequest) -> ProcessingResponse:
        decision = self.router.choose(request)
        record_provider_selection(
            decision.provider.value,
            decision.model,
            decision.estimated_cost_usd,
        )
        return ProcessingResponse(
            provider=decision,
            output={
                "summary": "Document processed successfully",
                "entities": ["invoice_id", "customer", "total"],
                "confidence": 0.94,
                "format": request.expected_output,
            },
        )

    async def queue_upload(self, filename: str, content_type: str | None) -> UploadJob:
        workload = self._infer_workload(filename, content_type)
        job = UploadJob(filename=filename, workload_type=workload)
        self.jobs[job.job_id] = job
        return job

    def get_job(self, job_id: str) -> UploadJob | None:
        return self.jobs.get(job_id)

    def complete_job(self, job_id: str) -> None:
        if job := self.jobs.get(job_id):
            job.status = "completed"

    @staticmethod
    def _infer_workload(filename: str, content_type: str | None) -> WorkloadType:
        lower = filename.lower()
        if lower.endswith(".pdf") or content_type == "application/pdf":
            return WorkloadType.PDF
        if lower.endswith((".png", ".jpg", ".jpeg", ".webp")) or (content_type or "").startswith(
            "image/"
        ):
            return WorkloadType.IMAGE
        return WorkloadType.TEXT
