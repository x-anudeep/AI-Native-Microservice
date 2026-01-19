from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_routes_reasoning_to_claude() -> None:
    response = client.post(
        "/api/v1/documents/process",
        json={"content": "Analyze this contract", "needs_reasoning": True, "priority": "premium"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"]["provider"] == "claude"
    assert payload["output"]["confidence"] >= 0.9


def test_route_vision_to_openai() -> None:
    response = client.post(
        "/api/v1/providers/route",
        json={"content": "extract image fields", "workload_type": "image", "needs_vision": True},
    )

    assert response.status_code == 200
    assert response.json()["provider"] == "openai"
