from app.models.schemas import ProviderName, ProviderStatus


def list_provider_statuses() -> list[ProviderStatus]:
    return [
        ProviderStatus(
            name=ProviderName.CLAUDE,
            healthy=True,
            active_model="claude-3-5-sonnet",
            avg_latency_ms=430,
            cost_per_1k_tokens=0.003,
        ),
        ProviderStatus(
            name=ProviderName.OPENAI,
            healthy=True,
            active_model="gpt-4o",
            avg_latency_ms=310,
            cost_per_1k_tokens=0.0025,
        ),
        ProviderStatus(
            name=ProviderName.GEMINI,
            healthy=True,
            active_model="gemini-1.5-pro",
            avg_latency_ms=520,
            cost_per_1k_tokens=0.00125,
        ),
        ProviderStatus(
            name=ProviderName.LOCAL,
            healthy=True,
            active_model="llama-3.1-8b-instruct",
            avg_latency_ms=820,
            cost_per_1k_tokens=0.0,
        ),
    ]
