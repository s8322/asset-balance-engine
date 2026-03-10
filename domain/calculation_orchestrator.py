from __future__ import annotations

from datetime import date

from .asset_period_builder import build_asset_period
from .asset_source_dates import AssetSourceDates
from .asset_track_mapping import map_asset_type_to_track_type
from .calculators.accumulating_savings import AccumulatingSavingsCalculator
from .calculation_result import CalculationResult
from .enums import AssetType, CalculationTrackType
from .shared_period import SharedPeriod


def get_track_type_for_asset_type(asset_type: AssetType) -> CalculationTrackType:
    return map_asset_type_to_track_type(asset_type)


def run_supported_calculation_for_asset_type(
    asset_type: AssetType,
    current_balance: float,
    asset_period: SharedPeriod,
    marriage_period: SharedPeriod,
) -> CalculationResult:
    track_type = get_track_type_for_asset_type(asset_type)

    if track_type is not CalculationTrackType.ACCUMULATING_SAVINGS:
        raise ValueError(
            f"Track type {track_type!r} is not supported for execution yet"
        )

    calculator = AccumulatingSavingsCalculator()
    return calculator.calculate(
        current_balance=current_balance,
        asset_period=asset_period,
        marriage_period=marriage_period,
    )


def run_calculation_for_asset(
    asset_type: AssetType,
    source_dates: AssetSourceDates | None,
    current_balance: float,
    valuation_date: date,
    marriage_period: SharedPeriod,
) -> CalculationResult | None:
    asset_period = build_asset_period(
        asset_type=asset_type,
        source_dates=source_dates,
        valuation_date=valuation_date,
    )

    if asset_period is None:
        return None

    return run_supported_calculation_for_asset_type(
        asset_type=asset_type,
        current_balance=current_balance,
        asset_period=asset_period,
        marriage_period=marriage_period,
    )


__all__ = [
    "get_track_type_for_asset_type",
    "run_supported_calculation_for_asset_type",
    "run_calculation_for_asset",
]

