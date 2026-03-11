from datetime import date

from domain.asset_source_dates import AssetSourceDates
from domain.asset_period_builder import build_asset_period
from domain.enums import AssetType


def test_build_asset_period_returns_shared_period_when_valid() -> None:
    source_dates = AssetSourceDates(first_contribution_date=date(2020, 1, 1))
    valuation_date = date(2020, 12, 31)

    period = build_asset_period(
        asset_type=AssetType.PENSION,
        source_dates=source_dates,
        valuation_date=valuation_date,
    )

    assert period is not None
    assert period.start == date(2020, 1, 1)
    assert period.end == valuation_date


def test_build_asset_period_returns_none_when_no_relevant_start_date() -> None:
    # For LEGAL_DOCUMENT, resolver returns None, so no asset period is built
    source_dates = AssetSourceDates(
        account_opened_date=date(2020, 1, 1),
        first_contribution_date=date(2020, 2, 1),
    )
    valuation_date = date(2020, 12, 31)

    period = build_asset_period(
        asset_type=AssetType.LEGAL_DOCUMENT,
        source_dates=source_dates,
        valuation_date=valuation_date,
    )

    assert period is None


def test_build_asset_period_returns_none_when_start_after_valuation_date() -> None:
    source_dates = AssetSourceDates(first_contribution_date=date(2021, 1, 1))
    valuation_date = date(2020, 12, 31)

    period = build_asset_period(
        asset_type=AssetType.PENSION,
        source_dates=source_dates,
        valuation_date=valuation_date,
    )

    assert period is None


