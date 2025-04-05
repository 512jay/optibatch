from dataclasses import dataclass, field
from tkinter import StringVar
from typing import Any


@dataclass
class AppState:
    expert_path_var: StringVar = field(default_factory=StringVar)
    symbol_var: StringVar = field(default_factory=StringVar)
    deposit_var: StringVar = field(default_factory=StringVar)
    currency_var: StringVar = field(default_factory=StringVar)
    leverage_var: StringVar = field(default_factory=StringVar)
    report_var: StringVar = field(default_factory=lambda: StringVar(value="csv,html"))
    optimization_mode_var: StringVar = field(default_factory=StringVar)
    result_priority_var: StringVar = field(default_factory=StringVar)
    forward_mode_var: StringVar = field(default_factory=StringVar)
    fromdate_var: dict[str, StringVar] = field(default_factory=dict)
    todate_var: dict[str, StringVar] = field(default_factory=dict)
    forwarddate_var: dict[str, StringVar] = field(default_factory=dict)
    status_var: StringVar = field(default_factory=StringVar)
    parsed_strategy_inputs: dict[str, dict[str, Any]] = field(default_factory=dict)
