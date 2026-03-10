from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from domain.enums import AccumulatingSavingsCalculationBasis


@dataclass(frozen=True)
class AccumulatingSavingsCalculationInput:
    current_balance: float
    asset_period_start: date
    asset_period_end: date
    marriage_period_start: date
    marriage_period_end: date
    calculation_basis: AccumulatingSavingsCalculationBasis


__all__ = ["AccumulatingSavingsCalculationInput"]
