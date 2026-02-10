import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "X-Request-ID" in response.headers


def test_create_and_fetch_migration():
    payload = {
        "repo_url": "https://github.com/example/legacy-app",
        "language": "python",
        "target_architecture": "cloud-run-microservices",
    }

    create_response = client.post("/migrations", json=payload)
    assert create_response.status_code == 201
    body = create_response.json()
    assert body["status"] == "completed"
    assert len(body["results"]) == 4

    migration_id = body["migration_id"]
    get_response = client.get(f"/migrations/{migration_id}")
    assert get_response.status_code == 200
    assert get_response.json()["migration_id"] == migration_id


def test_missing_migration_returns_404():
    response = client.get("/migrations/does-not-exist")
    assert response.status_code == 404
