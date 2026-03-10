from __future__ import annotations

from .enums import AssetType, CalculationTrackType


def map_asset_type_to_track_type(asset_type: AssetType) -> CalculationTrackType:
    if asset_type in {
        AssetType.PENSION,
        AssetType.STUDY_FUND,
        AssetType.PROVIDENT_FUND,
        AssetType.EXECUTIVE_INSURANCE,
    }:
        return CalculationTrackType.ACCUMULATING_SAVINGS

    if asset_type is AssetType.BUDGETARY_PENSION:
        return CalculationTrackType.BUDGETARY_PENSION

    if asset_type in {AssetType.RSU, AssetType.STOCK_OPTIONS}:
        return CalculationTrackType.EQUITY_COMPENSATION

    if asset_type in {AssetType.INVESTMENT_ACCOUNT, AssetType.BANK_ACCOUNT}:
        return CalculationTrackType.INVESTMENT_OR_CASH

    if asset_type is AssetType.LIABILITY:
        return CalculationTrackType.LIABILITY

    if asset_type is AssetType.EMPLOYMENT_RIGHTS:
        return CalculationTrackType.EMPLOYMENT_RIGHTS

    if asset_type in {AssetType.LEGAL_DOCUMENT, AssetType.OTHER}:
        return CalculationTrackType.LEGAL_REFERENCE

    raise ValueError(f"Unsupported AssetType for track mapping: {asset_type!r}")


__all__ = ["map_asset_type_to_track_type"]

