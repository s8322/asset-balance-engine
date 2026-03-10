from __future__ import annotations

from enum import Enum, auto


class AssetClass(Enum):
    EQUITY = auto()
    BOND = auto()
    CASH = auto()
    FUND = auto()
    OTHER = auto()


class Currency(Enum):
    USD = auto()
    EUR = auto()
    ILS = auto()


class CalculationStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


class AccumulatingSavingsCalculationBasis(Enum):
    TIME_PRORATED = auto()
    ACTUAL_CONTRIBUTIONS = auto()
    REPORT_BASED = auto()


__all__ = [
    "AssetClass",
    "Currency",
    "CalculationStatus",
    "AccumulatingSavingsCalculationBasis",
]

