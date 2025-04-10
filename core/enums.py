# core/enums.py

from enum import Enum, IntEnum
from typing import Any, Type, TypeVar, Protocol, cast, Iterable
from loguru import logger

# --- Type Contracts for Enums with label/from_label ---
class HasLabel(Protocol):
    @property
    def label(self) -> str: ...

TEnum = TypeVar("TEnum", bound=HasLabel)


# --- Reusable classmethod for label matching ---
def from_label(enum_cls: Type[TEnum], label: str) -> TEnum:
    for member in cast(Iterable[TEnum], enum_cls):
        if getattr(member, "label", None) == label:
            return member
    raise ValueError(f"{label!r} is not a valid label for {enum_cls.__name__}")


class ModelingMode(str, Enum):
    EVERY_TICK = "0"
    OHLC_1MIN = "1"
    OPEN_PRICES = "2"
    MATH_CALCULATIONS = "3"
    REAL_TICKS = "4"

    @property
    def label(self) -> str:
        return {
            "0": "Every tick",
            "1": "1 minute OHLC",
            "2": "Open prices only",
            "3": "Math calculations",
            "4": "Every tick based on real ticks",
        }[self.value]

    @classmethod
    def from_value(cls, value: str | int) -> "ModelingMode":
        return cls(str(value))

    @classmethod
    def from_label(cls, label: str) -> "ModelingMode":
        return from_label(cls, label)


class OptimizationCriterion(IntEnum):
    BALANCE_MAX = 0
    PROFIT_FACTOR_MAX = 1
    EXPECTED_PAYOFF_MAX = 2
    DRAW_DOWN_MIN = 3
    SHARPE_RATIO_MAX = 4

    @property
    def label(self) -> str:
        return self.name.replace("_", " ").title()

    @classmethod
    def from_value(cls, value: str | int) -> "OptimizationCriterion":
        return cls(int(value))

    @classmethod
    def from_label(cls, label: str) -> "OptimizationCriterion":
        return from_label(cls, label)


class ExecutionMode(IntEnum):
    MARKET = 0
    EXCHANGE = 1

    @property
    def label(self) -> str:
        return self.name.replace("_", " ").title()

    @classmethod
    def from_value(cls, value: str | int) -> "ExecutionMode":
        return cls(int(value))

    @classmethod
    def from_label(cls, label: str) -> "ExecutionMode":
        return from_label(cls, label)


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

    @property
    def label(self) -> str:
        return self.value

    @classmethod
    def from_label(cls, label: str) -> "Timeframe":
        return from_label(cls, label)


class OptimizationMode(IntEnum):
    DISABLED = 0
    SLOW = 1
    FAST = 2
    MARKET_WATCH = 3

    @property
    def label(self) -> str:
        return {
            self.DISABLED: "Disabled",
            self.SLOW: "Slow complete algorithm",
            self.FAST: "Fast genetic based algorithm",
            self.MARKET_WATCH: "All symbols selected in MarketWatch",
        }[self]

    @classmethod
    def from_value(cls, value: str | int) -> "OptimizationMode":
        return cls(int(value))

    @classmethod
    def from_label(cls, label: str) -> "OptimizationMode":
        return from_label(cls, label)


class ResultPriority(IntEnum):
    BALANCE_MAX = 0
    PROFIT_FACTOR_MAX = 1
    EXPECTED_PAYOFF_MAX = 2
    DRAWDOWN_MIN = 3
    RECOVERY_FACTOR_MAX = 4
    SHARPE_RATIO_MAX = 5
    CUSTOM_MAX = 6
    COMPLEX_CRITERION_MAX = 7

    @property
    def label(self) -> str:
        return self.name.replace("_", " ").title()

    @classmethod
    def from_value(cls, value: str | int) -> "ResultPriority":
        return cls(int(value))

    @classmethod
    def from_label(cls, label: str) -> "ResultPriority":
        return from_label(cls, label)


class ForwardMode(IntEnum):
    NO = 0
    HALF = 1
    THIRD = 2
    QUARTER = 3
    CUSTOM_DATE = 4

    @property
    def label(self) -> str:
        return self.name.replace("_", " ").title()

    @classmethod
    def from_value(cls, value: str | int) -> "ForwardMode":
        return cls(int(value))

    @classmethod
    def from_label(cls, label: str) -> "ForwardMode":
        return from_label(cls, label)


class TestDateRange(IntEnum):
    ENTIRE_HISTORY = 0
    LAST_MONTH = 1
    LAST_YEAR = 2
    CUSTOM = 99

    @property
    def label(self) -> str:
        return self.name.replace("_", " ").title()

    @classmethod
    def from_label(cls, label: str) -> "TestDateRange":
        return from_label(cls, label)


class DepositCurrency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CHF = "CHF"
    JPY = "JPY"

    @property
    def label(self) -> str:
        return self.value

    @classmethod
    def from_label(cls, label: str) -> "DepositCurrency":
        return from_label(cls, label)


class ProfitMode(IntEnum):
    STANDARD = 0
    IN_PIPS = 1

    @property
    def label(self) -> str:
        return self.name.replace("_", " ").title()

    @classmethod
    def from_label(cls, label: str) -> "ProfitMode":
        return from_label(cls, label)


def get_enum_label(enum_class: Type[TEnum], value: int | str) -> str:
    try:
        enum_class_casted = cast(Any, enum_class)
        member = enum_class_casted(value)
        label = getattr(member, "label", None)
        return label if label is not None else member.name
    except (ValueError, TypeError) as e:
        logger.warning(f"Invalid enum value '{value}' for {enum_class.__name__}: {e}")
        return f"Unknown ({value})"


def detect_date_range_section(parsed_ini: dict[str, Any]) -> TestDateRange:
    tester = parsed_ini.get("Tester", {})
    if "Dates" in tester:
        return TestDateRange(int(tester["Dates"]))
    elif "FromDate" in tester and "ToDate" in tester:
        return TestDateRange.CUSTOM
    return TestDateRange.ENTIRE_HISTORY


def enum_label_map(enum_cls: Type[TEnum]) -> dict[str, str]:
    iterable_enum = cast(Iterable[TEnum], enum_cls)
    return {
        member.label: getattr(member, "value", str(member)) for member in iterable_enum
    }


def get_label_for_value(enum_cls: Type[TEnum], value: str | int) -> str:
    try:
        return enum_cls.from_value(value).label  # type: ignore[attr-defined]
    except Exception:
        return str(value)


def get_value_for_label(enum_cls: Type[TEnum], label: str) -> str:
    iterable_enum = cast(Iterable[TEnum], enum_cls)
    for member in iterable_enum:
        if member.label == label:
            return getattr(member, "value", str(member))
    return label
