from core.enums import OptimizationMode, ResultPriority, ForwardMode, get_enum_label
from core.session import cache_ini_file, has_cached_ini, get_cached_ini_file
from ini_utils.loader import parse_ini_file, parse_tester_inputs_section
from tkinter import filedialog
from pathlib import Path
import tkinter as tk


def load_ini_ui(
    expert_var,
    symbol_var,
    deposit_var,
    currency_var,
    leverage_var,
    optimization_var,
    result_priority_var,
    forward_mode_var,
    from_picker,
    to_picker,
    forward_picker,
    parsed_inputs_holder,
    status_var,
):
    file_path = filedialog.askopenfilename(filetypes=[("INI Files", "*.ini")])
    if not file_path:
        return

    ini_path = Path(file_path)
    cache_ini_file(ini_path)
    _load_ini_to_ui(
        ini_path,
        expert_var,
        symbol_var,
        deposit_var,
        currency_var,
        leverage_var,
        optimization_var,
        result_priority_var,
        forward_mode_var,
        from_picker,
        to_picker,
        forward_picker,
        parsed_inputs_holder,
        status_var,
    )


def try_load_cached_ini(
    expert_var,
    symbol_var,
    deposit_var,
    currency_var,
    leverage_var,
    optimization_var,
    result_priority_var,
    forward_mode_var,
    from_picker,
    to_picker,
    forward_picker,
    parsed_inputs_holder,
    status_var,
):
    if has_cached_ini():
        ini_path = get_cached_ini_file()
        _load_ini_to_ui(
            ini_path,
            expert_var,
            symbol_var,
            deposit_var,
            currency_var,
            leverage_var,
            optimization_var,
            result_priority_var,
            forward_mode_var,
            from_picker,
            to_picker,
            forward_picker,
            parsed_inputs_holder,
            status_var,
        )


def _load_ini_to_ui(
    ini_path,
    expert_var,
    symbol_var,
    deposit_var,
    currency_var,
    leverage_var,
    optimization_var,
    result_priority_var,
    forward_mode_var,
    from_picker,
    to_picker,
    forward_picker,
    parsed_inputs_holder,
    status_var,
):
    data = parse_ini_file(str(ini_path))

    expert_var.set(data.get("Expert", ""))
    symbol_var.set(data.get("Symbol", "EURUSD"))
    deposit_var.set(data.get("Deposit", "10000"))
    currency_var.set(data.get("Currency", "USD"))
    leverage_var.set(data.get("Leverage", "100"))

    def enum_to_label(enum_class, val, fallback):
        try:
            return get_enum_label(enum_class, int(val))
        except Exception:
            return fallback

    optimization_var.set(
        enum_to_label(OptimizationMode, data.get("Optimization", 2), "Fast")
    )
    result_priority_var.set(
        enum_to_label(
            ResultPriority, data.get("OptimizationCriterion", 0), "Balance Max"
        )
    )
    forward_mode_var.set(enum_to_label(ForwardMode, data.get("ForwardMode", 0), "NO"))

    def set_date(picker: dict[str, tk.StringVar], raw: str) -> None:
        try:
            y, m, d = raw.split(".")
            picker["year"].set(y)
            picker["month"].set(m.zfill(2))
            picker["day"].set(d.zfill(2))
        except Exception:
            for part in picker.values():
                part.set("")

    set_date(from_picker, data.get("FromDate", ""))
    set_date(to_picker, data.get("ToDate", ""))

    if forward_mode_var.get().lower() == "custom":
        set_date(forward_picker, data.get("ForwardDate", ""))
    else:
        for part in forward_picker.values():
            part.set("")

    parsed_inputs_holder.clear()
    parsed_inputs_holder.extend(parse_tester_inputs_section(data.get("inputs", {})))

    status_var.set(f"Loaded: {ini_path.name}")
