# core/enums.py

from enum import IntEnum, Enum
from typing import Any, Type


class StrategyModel(IntEnum):
    EVERY_TICK = 0
    REAL_TICKS = 1
    OHLC_1MIN = 2
    OPEN_PRICES = 3
    MATH_CALC = 4


class OptimizationCriterion(IntEnum):
    BALANCE_MAX = 0
    PROFIT_FACTOR_MAX = 1
    EXPECTED_PAYOFF_MAX = 2
    DRAW_DOWN_MIN = 3
    SHARPE_RATIO_MAX = 4


class ExecutionMode(IntEnum):
    MARKET = 0
    EXCHANGE = 1


class Timeframe(str, Enum):
    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
    MN1 = "MN1"


class OptimizationMode(IntEnum):
    DISABLED = 0
    SLOW = 1
    FAST = 2
    MARKET_WATCH = 3


class ResultPriority(IntEnum):
    BALANCE_MAX = 0
    PROFIT_FACTOR_MAX = 1
    EXPECTED_PAYOFF_MAX = 2
    DRAWDOWN_MIN = 3
    RECOVERY_FACTOR_MAX = 4
    SHARPE_RATIO_MAX = 5
    CUSTOM_MAX = 6
    COMPLEX_CRITERION_MAX = 7


class ForwardMode(IntEnum):
    NO = 0
    HALF = 1
    THIRD = 2
    QUARTER = 3
    CUSTOM_DATE = 4


class TestDateRange(IntEnum):
    ENTIRE_HISTORY = 0
    LAST_MONTH = 1
    LAST_YEAR = 2
    CUSTOM = 99  # Used when FromDate/ToDate are explicitly defined


class DepositCurrency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CHF = "CHF"
    JPY = "JPY"


class ProfitMode(IntEnum):
    STANDARD = 0
    IN_PIPS = 1


# Optional: Helper to convert enum value to human-readable string


def get_enum_label(enum_class: Type[Enum], value: int | str) -> str:
    try:
        return enum_class(value).name.replace("_", " ").title()
    except ValueError:
        return f"Unknown ({value})"


def detect_date_range_section(parsed_ini: dict[str, Any]) -> TestDateRange:
    tester = parsed_ini.get("Tester", {})
    if "Dates" in tester:
        return TestDateRange(int(tester["Dates"]))
    elif "FromDate" in tester and "ToDate" in tester:
        return TestDateRange.CUSTOM
    return TestDateRange.ENTIRE_HISTORY
