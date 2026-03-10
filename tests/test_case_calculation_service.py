from datetime import date

from application.case_calculation_service import CaseCalculationService
from domain.asset import Asset
from domain.asset_source_dates import AssetSourceDates
from domain.enums import AssetType, CalculationTrackType, Currency
from domain.shared_period import SharedPeriod


def test_single_asset_with_balance_returns_one_result() -> None:
    source_dates = AssetSourceDates(first_contribution_date=date(2020, 1, 1))
    asset = Asset(
        id="asset-1",
        name="Pension",
        asset_type=AssetType.PENSION,
        currency=Currency.ILS,
        source_dates=source_dates,
    )
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2020, 12, 31))
    valuation_date = date(2020, 12, 31)
    balance_by_asset_id = {"asset-1": 1000.0}

    service = CaseCalculationService()
    results = service.calculate_case(
        assets=[asset],
        marriage_period=marriage_period,
        valuation_date=valuation_date,
        balance_by_asset_id=balance_by_asset_id,
    )

    assert len(results.results) == 1
    assert results.results[0].total_days > 0
    assert 0.0 <= results.results[0].shared_ratio <= 1.0
    assert results.calculated_asset_ids == ["asset-1"]
    assert results.skipped_asset_ids == []
    assert results.metrics.total_assets == 1
    assert results.metrics.calculated_count == 1
    assert results.metrics.skipped_count == 0
    assert results.metrics.by_asset_type == {AssetType.PENSION: 1}
    assert results.metrics.by_track_type == {
        CalculationTrackType.ACCUMULATING_SAVINGS: 1,
    }


def test_asset_with_no_calculation_track_returns_empty_list() -> None:
    asset = Asset(
        id="asset-bank",
        name="Bank",
        asset_type=AssetType.BANK_ACCOUNT,
        currency=Currency.ILS,
        source_dates=AssetSourceDates(account_opened_date=date(2020, 1, 1)),
    )
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2020, 12, 31))
    valuation_date = date(2020, 12, 31)

    service = CaseCalculationService()
    results = service.calculate_case(
        assets=[asset],
        marriage_period=marriage_period,
        valuation_date=valuation_date,
        balance_by_asset_id={"asset-bank": 500.0},
    )

    assert results.results == []
    assert results.calculated_asset_ids == []
    assert results.skipped_asset_ids == ["asset-bank"]
    assert results.metrics.total_assets == 1
    assert results.metrics.calculated_count == 0
    assert results.metrics.skipped_count == 1
    assert results.metrics.by_asset_type == {AssetType.BANK_ACCOUNT: 1}
    assert results.metrics.by_track_type == {
        CalculationTrackType.INVESTMENT_OR_CASH: 1,
    }


def test_mixed_assets_returns_only_calculable_results() -> None:
    pension_source = AssetSourceDates(first_contribution_date=date(2020, 1, 1))
    pension_asset = Asset(
        id="pension-1",
        name="Pension",
        asset_type=AssetType.PENSION,
        currency=Currency.ILS,
        source_dates=pension_source,
    )
    bank_asset = Asset(
        id="bank-1",
        name="Bank",
        asset_type=AssetType.BANK_ACCOUNT,
        currency=Currency.ILS,
    )
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2020, 12, 31))
    valuation_date = date(2020, 12, 31)
    balance_by_asset_id = {"pension-1": 1000.0}

    service = CaseCalculationService()
    results = service.calculate_case(
        assets=[pension_asset, bank_asset],
        marriage_period=marriage_period,
        valuation_date=valuation_date,
        balance_by_asset_id=balance_by_asset_id,
    )

    assert len(results.results) == 1
    assert results.results[0].total_days > 0
    assert results.calculated_asset_ids == ["pension-1"]
    assert results.skipped_asset_ids == ["bank-1"]
    assert results.metrics.total_assets == 2
    assert results.metrics.calculated_count == 1
    assert results.metrics.skipped_count == 1
    assert results.metrics.by_asset_type == {
        AssetType.PENSION: 1,
        AssetType.BANK_ACCOUNT: 1,
    }
    assert results.metrics.by_track_type == {
        CalculationTrackType.ACCUMULATING_SAVINGS: 1,
        CalculationTrackType.INVESTMENT_OR_CASH: 1,
    }


def test_balance_by_asset_id_none_uses_zero_and_does_not_raise() -> None:
    source_dates = AssetSourceDates(first_contribution_date=date(2020, 1, 1))
    asset = Asset(
        id="asset-1",
        name="Pension",
        asset_type=AssetType.PENSION,
        currency=Currency.ILS,
        source_dates=source_dates,
    )
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2020, 12, 31))
    valuation_date = date(2020, 12, 31)

    service = CaseCalculationService()
    results = service.calculate_case(
        assets=[asset],
        marriage_period=marriage_period,
        valuation_date=valuation_date,
        balance_by_asset_id=None,
    )

    assert len(results.results) == 1
    assert results.results[0].gross_shared_value == 0.0
    assert results.metrics.total_assets == 1
    assert results.metrics.calculated_count == 1
    assert results.metrics.skipped_count == 0
    assert results.metrics.by_asset_type == {AssetType.PENSION: 1}
    assert results.metrics.by_track_type == {
        CalculationTrackType.ACCUMULATING_SAVINGS: 1,
    }
