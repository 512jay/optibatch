from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_get_runs_extended():
    response = client.get("/runs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        run = data[0]
        # Confirm all expected keys exist
        expected_keys = {
            "id",  # ← was "run_id"
            "job_id", "symbol", "profit", "drawdown", "custom_score",
            "sharpe_ratio", "trades", "expected_payoff", "recovery_factor",
            "profit_factor", "run_month", "start_date", "end_date", "pass_number",
            "result", "is_full_month", "params_json", "result_hash", "created_at",
            "updated_at", "tags", "notes", "run_label", "status", "is_archived"
        }
        assert expected_keys.issubset(run.keys())