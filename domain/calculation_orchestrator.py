from __future__ import annotations

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


__all__ = [
    "get_track_type_for_asset_type",
    "run_supported_calculation_for_asset_type",
]

