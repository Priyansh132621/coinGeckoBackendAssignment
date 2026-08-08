import os
os.environ.setdefault("CACHE_TTL_SECONDS", "60")

from fastapi.testclient import TestClient

from app.main import app
from app.routers import crypto


def test_health_endpoint_healthy(monkeypatch):
    async def fake_check_health():
        return {"status": "reachable", "coin_gecko_version": "V3"}

    monkeypatch.setattr(crypto, "check_health", fake_check_health)

    client = TestClient(app)
    response = client.get("/crypto/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_coins_list_endpoint(monkeypatch):
    async def fake_coins_list(page_num=1, per_page=10):
        return [{"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"}]

    monkeypatch.setattr(crypto, "API_AUTH_KEY", "test-key")
    monkeypatch.setattr(crypto, "coins_list", fake_coins_list)

    client = TestClient(app)
    response = client.get("/crypto/coins", headers={"x-api-key": "test-key"})

    assert response.status_code == 200
    assert response.json()["status"] == "available"
    assert response.json()["coins"][0]["id"] == "bitcoin"