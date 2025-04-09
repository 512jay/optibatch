from core.enums import OptimizationMode, ResultPriority, ModelingMode
from core.session import get_field, update_date_fields


def update_fields_from_ini(data: dict, context: dict) -> None:
    ctx = context  # just to shorten

    ctx["expert"].set(get_field(data, "expert_path"))
    ctx["symbol"].set(get_field(data, "symbol"))
    ctx["deposit"].set(str(get_field(data, "deposit", 10000)))
    ctx["currency"].set(get_field(data, "currency", "USD"))
    ctx["leverage"].set(str(get_field(data, "leverage", 100)))

    ctx["modeling"].set(ModelingMode.from_value(str(get_field(data, "model", 1))).label)
    ctx["optimization"].set(
        OptimizationMode.from_value(str(get_field(data, "optimization", 1))).name
    )
    ctx["result"].set(
        ResultPriority.from_value(str(get_field(data, "result", 0))).name
    )


    ctx["forward"].set("No")

    from_date = get_field(data, "from_date")
    to_date = get_field(data, "to_date")
    ctx["update_dates"](from_date, to_date)
