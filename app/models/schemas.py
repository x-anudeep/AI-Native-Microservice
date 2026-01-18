from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class WorkloadType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    PDF = "pdf"
    MIXED = "mixed"


class ProviderName(StrEnum):
    CLAUDE = "claude"
    OPENAI = "openai"
    GEMINI = "gemini"
    LOCAL = "local"


class ProcessingRequest(BaseModel):
    content: str = Field(min_length=1, max_length=120_000)
    workload_type: WorkloadType = WorkloadType.TEXT
    priority: str = Field(default="balanced", pattern="^(economy|balanced|premium)$")
    needs_reasoning: bool = False
    needs_vision: bool = False
    expected_output: str = "structured_json"


class ProviderDecision(BaseModel):
    provider: ProviderName
    model: str
    reason: str
    estimated_cost_usd: float
    latency_budget_ms: int


class ProcessingResponse(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    provider: ProviderDecision
    status: str = "completed"
    output: dict[str, Any]


class UploadJob(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid4()))
    filename: str
    workload_type: WorkloadType
    status: str = "queued"
    provider_hint: ProviderName | None = None


class ProviderStatus(BaseModel):
    name: ProviderName
    healthy: bool
    active_model: str
    avg_latency_ms: int
    cost_per_1k_tokens: float


class MetricSnapshot(BaseModel):
    requests_total: int
    p95_latency_ms: int
    providers_active: int
    estimated_daily_cost_usd: float
