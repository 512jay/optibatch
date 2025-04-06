from dataclasses import dataclass, field
from tkinter import StringVar
from pathlib import Path

REPORT_CLICK_PATH = Path("state") / "report_click.json"


class AppState:
    def __init__(self):
        self.expert_path_var = StringVar()
        self.symbol_var = StringVar()
        self.deposit_var = StringVar()
        self.currency_var = StringVar()
        self.leverage_var = StringVar()
        self.report_var = StringVar(value="csv,html")
        self.optimization_mode_var = StringVar()
        self.result_priority_var = StringVar()
        self.forward_mode_var = StringVar()
        self.fromdate_var = {}
        self.todate_var = {}
        self.forwarddate_var = {}
        self.status_var = StringVar()
        self.parsed_strategy_inputs = {}
        self.report_click_set: StringVar | None = None
