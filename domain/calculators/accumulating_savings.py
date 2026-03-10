from __future__ import annotations

from domain.calculation_result import CalculationResult
from domain.ratio_engine import calculate_shared_ratio
from domain.shared_period import SharedPeriod


class AccumulatingSavingsCalculator:
    def calculate(
        self,
        current_balance: float,
        asset_period: SharedPeriod,
        marriage_period: SharedPeriod,
    ) -> CalculationResult:
        shared_ratio = calculate_shared_ratio(
            asset_period=asset_period,
            marriage_period=marriage_period,
        )
        total_days = asset_period.days()
        shared_days = asset_period.overlap_days(marriage_period)
        gross_shared_value = round(current_balance * shared_ratio, 2)

        return CalculationResult(
            total_days=total_days,
            shared_days=shared_days,
            shared_ratio=shared_ratio,
            gross_shared_value=gross_shared_value,
        )


__all__ = ["AccumulatingSavingsCalculator"]

