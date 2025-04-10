from pathlib import Path, PureWindowsPath
from core.enums import OptimizationMode, ResultPriority, ModelingMode, ForwardMode
from core.session import get_field, update_date_fields


def populate_ui_from_ini_data(data: dict, context: dict) -> None:
    ctx = context  # just to shorten
    tester = data.get("tester", {})
    ini_path = Path(data["path"])

    expert_path = tester.get("Expert", "")
    # Just display the path as-is from the INI file (already relative)
    ctx["expert"].set(str(PureWindowsPath(expert_path)))
    ctx["symbol"].set(tester.get("Symbol", ""))
    ctx["deposit"].set(str(tester.get("Deposit", 10000)))
    ctx["currency"].set(tester.get("Currency", "USD"))
    ctx["leverage"].set(str(tester.get("Leverage", 100)))
    ctx["modeling"].set(ModelingMode.from_value(tester.get("Model", 1)).label)
    ctx["optimization"].set(OptimizationMode.from_value(tester.get("Optimization", 1)).label)
    ctx["result"].set(ResultPriority.from_value(tester.get("OptimizationCriterion", 0)).label)
    ctx["forward"].set(ForwardMode.from_value(tester.get("ForwardMode", 0)).label)
    from_date = tester.get("FromDate", "")
    to_date = tester.get("ToDate", "")
    ctx["update_dates"](from_date, to_date)
