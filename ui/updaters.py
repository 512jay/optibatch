from pathlib import Path
from core.enums import OptimizationMode, ResultPriority, ModelingMode
from core.session import get_field, update_date_fields


def populate_ui_from_ini_data(data: dict, context: dict) -> None:
    ctx = context  # just to shorten
    tester = data.get("tester", {})
    ini_path = Path(data["path"])

    # Resolve expert path
    expert_raw = tester.get("Expert", "")
    expert_resolved = (
        str((ini_path.parent / expert_raw).resolve())
        if not Path(expert_raw).is_absolute()
        else expert_raw
    )
    ctx["expert"].set(expert_resolved)

    ctx["symbol"].set(tester.get("Symbol", ""))
    ctx["deposit"].set(str(tester.get("Deposit", 10000)))
    ctx["currency"].set(tester.get("Currency", "USD"))
    ctx["leverage"].set(str(tester.get("Leverage", 100)))

    ctx["modeling"].set(ModelingMode.from_value(str(tester.get("Model", 1))).label)
    ctx["optimization"].set(
        OptimizationMode.from_value(str(tester.get("Optimization", 1))).label
    )
    ctx["result"].set(
        ResultPriority.from_value(str(tester.get("OptimizationCriterion", 0))).label
    )

    ctx["forward"].set("No")

    from_date = tester.get("FromDate", "")
    to_date = tester.get("ToDate", "")
    ctx["update_dates"](from_date, to_date)
