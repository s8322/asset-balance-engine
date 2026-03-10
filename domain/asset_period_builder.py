from __future__ import annotations

from datetime import date

from .asset_source_dates import AssetSourceDates
from .enums import AssetType
from .relevant_start_date_resolver import resolve_relevant_start_date
from .shared_period import SharedPeriod


def build_asset_period(
    asset_type: AssetType,
    source_dates: AssetSourceDates | None,
    valuation_date: date,
) -> SharedPeriod | None:
    start_date = resolve_relevant_start_date(
        asset_type=asset_type,
        source_dates=source_dates,
    )

    if start_date is None:
        return None

    if start_date > valuation_date:
        return None

    return SharedPeriod(start=start_date, end=valuation_date)


__all__ = ["build_asset_period"]

