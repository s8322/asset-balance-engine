from __future__ import annotations

from .shared_period import SharedPeriod


def calculate_shared_ratio(
    asset_period: SharedPeriod,
    marriage_period: SharedPeriod,
) -> float:
    total_period_days = asset_period.days()
    if total_period_days <= 0:
        raise ValueError("asset_period must contain at least one day")

    shared_days = asset_period.overlap_days(marriage_period)
    if shared_days == 0:
        return 0.0

    ratio = shared_days / total_period_days
    if ratio < 0:
        raise ValueError("shared ratio cannot be negative")
    if ratio > 1:
        return 1.0

    return round(ratio, 10)


__all__ = ["calculate_shared_ratio"]

