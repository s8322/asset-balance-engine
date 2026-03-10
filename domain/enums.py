from __future__ import annotations

from enum import Enum, auto


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


class AssetType(Enum):
    PENSION = auto()
    STUDY_FUND = auto()
    PROVIDENT_FUND = auto()
    EXECUTIVE_INSURANCE = auto()
    BUDGETARY_PENSION = auto()
    RSU = auto()
    STOCK_OPTIONS = auto()
    INVESTMENT_ACCOUNT = auto()
    BANK_ACCOUNT = auto()
    LIABILITY = auto()
    EMPLOYMENT_RIGHTS = auto()
    LEGAL_DOCUMENT = auto()
    OTHER = auto()


__all__ = [
    "Currency",
    "CalculationStatus",
    "AccumulatingSavingsCalculationBasis",
    "AssetType",
]

