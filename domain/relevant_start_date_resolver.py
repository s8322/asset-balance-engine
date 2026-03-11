from __future__ import annotations

from datetime import date

from .asset_source_dates import AssetSourceDates
from .enums import AssetType


def resolve_relevant_start_date(
    asset_type: AssetType,
    source_dates: AssetSourceDates | None,
) -> date | None:
    if source_dates is None:
        return None

    if asset_type in {
        AssetType.PENSION,
        AssetType.STUDY_FUND,
        AssetType.PROVIDENT_FUND,
        AssetType.EXECUTIVE_INSURANCE,
    }:
        if source_dates.first_contribution_date is not None:
            return source_dates.first_contribution_date
        if source_dates.account_opened_date is not None:
            return source_dates.account_opened_date
        return None

    if asset_type is AssetType.BUDGETARY_PENSION:
        return source_dates.service_start_date

    if asset_type in {AssetType.RSU, AssetType.STOCK_OPTIONS}:
        return source_dates.grant_date

    if asset_type in {AssetType.BANK_ACCOUNT, AssetType.INVESTMENT_ACCOUNT}:
        return source_dates.account_opened_date

    return None


__all__ = ["resolve_relevant_start_date"]

