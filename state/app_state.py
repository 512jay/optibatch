# helpers/app_state.py

from dataclasses import dataclass, field
from tkinter import StringVar


@dataclass
class AppState:
    status_var: StringVar = field(default_factory=StringVar)
    selected_terminal: StringVar = field(default_factory=StringVar)
    symbol_var: StringVar = field(default_factory=StringVar)
    expert_path_var: StringVar = field(default_factory=StringVar)
    leverage_var: StringVar = field(default_factory=lambda: StringVar(value="100"))
    currency_var: StringVar = field(default_factory=lambda: StringVar(value="USD"))
    deposit_var: StringVar = field(default_factory=lambda: StringVar(value="10000"))
    report_var: StringVar = field(default_factory=lambda: StringVar(value="csv,html"))
    optimization_mode_var: StringVar = field(
        default_factory=lambda: StringVar(value="Slow (complete algorithm)")
    )
    result_priority_var: StringVar = field(
        default_factory=lambda: StringVar(value="Balance Max")
    )
    forward_mode_var: StringVar = field(default_factory=lambda: StringVar(value="NO"))
    forwarddate_var: StringVar = field(default_factory=StringVar)
    fromdate_var: StringVar = field(default_factory=StringVar)
    todate_var: StringVar = field(default_factory=StringVar)
