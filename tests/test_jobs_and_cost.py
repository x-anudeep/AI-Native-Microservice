from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_upload_creates_background_job() -> None:
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("invoice.pdf", b"%PDF-1.4 fake", "application/pdf")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filename"] == "invoice.pdf"
    assert payload["workload_type"] == "pdf"
    assert payload["status"] in {"queued", "completed"}


def test_cost_estimate_for_gemini() -> None:
    response = client.get(
        "/api/v1/cost/estimate",
        params={"tokens": 2000, "provider_name": "gemini"},
    )

    assert response.status_code == 200
    assert response.json()["estimated_cost_usd"] == 0.0025


def test_runtime_config_exposes_12_factor_settings() -> None:
    response = client.get("/api/v1/ops/config")

    assert response.status_code == 200
    assert response.json()["daily_request_target"] == 4000
