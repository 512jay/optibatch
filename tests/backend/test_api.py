from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_get_runs():
    response = client.get("/runs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_stats_summary():
    response = client.get("/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert "top_symbol" in data
    assert "average_profit" in data
