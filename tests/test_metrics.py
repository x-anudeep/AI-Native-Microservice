from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_prometheus_metrics_endpoint() -> None:
    client.get("/api/v1/health")

    response = client.get("/api/v1/metrics")

    assert response.status_code == 200
    assert "ai_native_requests_total" in response.text


def test_provider_selection_metric_is_recorded() -> None:
    client.post(
        "/api/v1/documents/process",
        json={"content": "read a receipt image", "workload_type": "image", "needs_vision": True},
    )

    response = client.get("/api/v1/metrics")

    assert "ai_native_provider_selections_total" in response.text
