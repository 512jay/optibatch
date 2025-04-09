import pytest
from unittest.mock import MagicMock
from pathlib import Path
from core.loader import load_ini_file
from ui.updaters import populate_ui_from_ini_data


@pytest.fixture
def context_mocks():
    fields = [
        "expert",
        "symbol",
        "deposit",
        "currency",
        "leverage",
        "modeling",
        "optimization",
        "result",
        "forward",
    ]
    ctx = {k: MagicMock() for k in fields}
    ctx["update_dates"] = MagicMock()
    return ctx


def test_populate_ui_from_example_ini(context_mocks):
    ini_path = Path("tests/example.ini")
    assert ini_path.exists(), "example.ini must be placed at tests/example.ini"

    data = load_ini_file(ini_path)
    populate_ui_from_ini_data(data, context_mocks)

    assert context_mocks["expert"].set.called
    assert context_mocks["symbol"].set.call_args[0][0] == "EURUSD"
    assert context_mocks["deposit"].set.call_args[0][0] == "10000"
    assert context_mocks["currency"].set.call_args[0][0] == "USD"
    assert context_mocks["leverage"].set.call_args[0][0] == "100"
    assert context_mocks["forward"].set.call_args[0][0] == "No"

    update_dates_args = context_mocks["update_dates"].call_args[0]
    assert update_dates_args == ("2025.01.01", "2025.04.08")
