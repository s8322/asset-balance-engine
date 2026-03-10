from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .calculators.accumulating_savings import AccumulatingSavingsCalculator
from .calculation_input import AccumulatingSavingsCalculationInput
from .calculation_result import CalculationResult
from .enums import CalculationStatus, AccumulatingSavingsCalculationBasis
from .shared_period import SharedPeriod


@dataclass
class CalculationRun:
    id: str
    track_id: str
    status: CalculationStatus
    period: SharedPeriod
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    inputs_snapshot: AccumulatingSavingsCalculationInput | None = None
    outputs_snapshot: CalculationResult | None = None

    def execute_accumulating_savings(
        self,
        current_balance: float,
        asset_period: SharedPeriod,
        marriage_period: SharedPeriod,
    ) -> None:
        self.status = CalculationStatus.RUNNING
        self.started_at = datetime.utcnow()

        self.inputs_snapshot = AccumulatingSavingsCalculationInput(
            current_balance=current_balance,
            asset_period_start=asset_period.start,
            asset_period_end=asset_period.end,
            marriage_period_start=marriage_period.start,
            marriage_period_end=marriage_period.end,
            calculation_basis=AccumulatingSavingsCalculationBasis.TIME_PRORATED,
        )

        calculator = AccumulatingSavingsCalculator()
        self.outputs_snapshot = calculator.calculate(
            current_balance=current_balance,
            asset_period=asset_period,
            marriage_period=marriage_period,
        )

        self.status = CalculationStatus.COMPLETED
        self.completed_at = datetime.utcnow()


__all__ = ["CalculationRun"]

