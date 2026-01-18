from app.models.schemas import ProcessingRequest, ProviderDecision, ProviderName, WorkloadType


class ProviderRouter:
    """Selects the most appropriate AI provider for each workload."""

    def choose(self, request: ProcessingRequest) -> ProviderDecision:
        content_length = len(request.content)

        if request.needs_vision or request.workload_type == WorkloadType.IMAGE:
            return ProviderDecision(
                provider=ProviderName.OPENAI,
                model="gpt-4o",
                reason="vision workload requires strong multimodal extraction",
                estimated_cost_usd=0.018,
                latency_budget_ms=650,
            )

        if content_length > 32_000 or request.workload_type == WorkloadType.PDF:
            return ProviderDecision(
                provider=ProviderName.GEMINI,
                model="gemini-1.5-pro",
                reason="long-context document requires large context window",
                estimated_cost_usd=0.012,
                latency_budget_ms=900,
            )

        if request.needs_reasoning or request.priority == "premium":
            return ProviderDecision(
                provider=ProviderName.CLAUDE,
                model="claude-3-5-sonnet",
                reason="reasoning-heavy task benefits from deliberative model",
                estimated_cost_usd=0.02,
                latency_budget_ms=750,
            )

        if request.priority == "economy":
            return ProviderDecision(
                provider=ProviderName.LOCAL,
                model="llama-3.1-8b-instruct",
                reason="economy request can run on local inference",
                estimated_cost_usd=0.001,
                latency_budget_ms=1200,
            )

        return ProviderDecision(
            provider=ProviderName.OPENAI,
            model="gpt-4o-mini",
            reason="balanced default route optimizes latency and cost",
            estimated_cost_usd=0.004,
            latency_budget_ms=500,
        )
