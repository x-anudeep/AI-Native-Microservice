from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_dashboard_homepage_serves_dark_console() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "AI-Native Microservice Platform" in response.text
    assert "/static/styles.css" in response.text


def test_dashboard_alias_serves_frontend() -> None:
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "Provider Router" in response.text
