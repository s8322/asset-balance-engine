from datetime import date

from domain.asset_source_dates import AssetSourceDates
from domain.calculation_orchestrator import run_calculation_for_asset
from domain.enums import AssetType
from domain.shared_period import SharedPeriod


def test_run_calculation_for_asset_pension_happy_path() -> None:
    source_dates = AssetSourceDates(first_contribution_date=date(2020, 1, 1))
    valuation_date = date(2020, 12, 31)
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2020, 12, 31))
    current_balance = 1000.0

    result = run_calculation_for_asset(
        asset_type=AssetType.PENSION,
        source_dates=source_dates,
        current_balance=current_balance,
        valuation_date=valuation_date,
        marriage_period=marriage_period,
    )

    assert result is not None
    assert result.total_days > 0
    assert result.shared_days >= 0
    assert 0.0 <= result.shared_ratio <= 1.0
    assert result.gross_shared_value == round(
        current_balance * result.shared_ratio, 2
    )


def test_run_calculation_for_asset_returns_none_when_no_asset_period() -> None:
    # For BANK_ACCOUNT, relevant_start_date resolver returns None,
    # so build_asset_period returns None and the orchestrator should return None.
    source_dates = AssetSourceDates(
        account_opened_date=date(2020, 1, 1),
        first_contribution_date=date(2020, 2, 1),
    )
    valuation_date = date(2020, 12, 31)
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2020, 12, 31))

    result = run_calculation_for_asset(
        asset_type=AssetType.BANK_ACCOUNT,
        source_dates=source_dates,
        current_balance=1000.0,
        valuation_date=valuation_date,
        marriage_period=marriage_period,
    )

    assert result is None


def test_run_calculation_for_asset_unsupported_track_type_returns_none() -> None:
    # LEGAL_DOCUMENT is mapped to a non-calculating track, and resolver returns None,
    # so no asset period is built and the orchestrator should return None.
    source_dates = AssetSourceDates(
        account_opened_date=date(2020, 1, 1),
        first_contribution_date=date(2020, 2, 1),
        service_start_date=date(2010, 5, 1),
        grant_date=date(2021, 7, 1),
    )
    valuation_date = date(2020, 12, 31)
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2020, 12, 31))

    result = run_calculation_for_asset(
        asset_type=AssetType.LEGAL_DOCUMENT,
        source_dates=source_dates,
        current_balance=1000.0,
        valuation_date=valuation_date,
        marriage_period=marriage_period,
    )

    assert result is None


