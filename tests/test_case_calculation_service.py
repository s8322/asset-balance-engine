from datetime import date

import pytest

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
    assert results.total_gross_shared_value == pytest.approx(
        results.results[0].gross_shared_value
    )
    assert results.metrics.gross_shared_value_by_asset_type == {
        AssetType.PENSION: pytest.approx(results.results[0].gross_shared_value)
    }
    assert results.metrics.gross_shared_value_by_track_type == {
        CalculationTrackType.ACCUMULATING_SAVINGS: pytest.approx(
            results.results[0].gross_shared_value
        )
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
    assert results.total_gross_shared_value == 0.0
    assert results.metrics.gross_shared_value_by_asset_type == {}
    assert results.metrics.gross_shared_value_by_track_type == {}


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
    assert results.total_gross_shared_value == pytest.approx(
        sum(r.gross_shared_value for r in results.results)
    )
    assert results.metrics.gross_shared_value_by_asset_type == {
        AssetType.PENSION: pytest.approx(
            sum(r.gross_shared_value for r in results.results)
        )
    }
    assert results.metrics.gross_shared_value_by_track_type == {
        CalculationTrackType.ACCUMULATING_SAVINGS: pytest.approx(
            sum(r.gross_shared_value for r in results.results)
        )
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
    assert results.total_gross_shared_value == 0.0
    assert results.metrics.gross_shared_value_by_asset_type == {
        AssetType.PENSION: 0.0
    }
    assert results.metrics.gross_shared_value_by_track_type == {
        CalculationTrackType.ACCUMULATING_SAVINGS: 0.0
    }


def test_multiple_assets_same_type_accumulate_metrics_and_gross_maps() -> None:
    source_dates_1 = AssetSourceDates(first_contribution_date=date(2020, 1, 1))
    source_dates_2 = AssetSourceDates(first_contribution_date=date(2021, 1, 1))
    asset_1 = Asset(
        id="pension-1",
        name="Pension 1",
        asset_type=AssetType.PENSION,
        currency=Currency.ILS,
        source_dates=source_dates_1,
    )
    asset_2 = Asset(
        id="pension-2",
        name="Pension 2",
        asset_type=AssetType.PENSION,
        currency=Currency.ILS,
        source_dates=source_dates_2,
    )
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2022, 12, 31))
    valuation_date = date(2022, 12, 31)
    balance_by_asset_id = {"pension-1": 1000.0, "pension-2": 2000.0}

    service = CaseCalculationService()
    results = service.calculate_case(
        assets=[asset_1, asset_2],
        marriage_period=marriage_period,
        valuation_date=valuation_date,
        balance_by_asset_id=balance_by_asset_id,
    )

    assert results.metrics.by_asset_type[AssetType.PENSION] == 2
    assert results.metrics.by_track_type[CalculationTrackType.ACCUMULATING_SAVINGS] == 2
    total_gross = sum(r.gross_shared_value for r in results.results)
    assert results.metrics.gross_shared_value_by_asset_type[AssetType.PENSION] == pytest.approx(
        total_gross
    )
    assert results.metrics.gross_shared_value_by_track_type[
        CalculationTrackType.ACCUMULATING_SAVINGS
    ] == pytest.approx(total_gross)
    assert results.total_gross_shared_value == pytest.approx(total_gross)


def test_multiple_assets_mixed_types_count_all_assets_but_sum_only_calculated() -> None:
    pension_source_1 = AssetSourceDates(first_contribution_date=date(2020, 1, 1))
    pension_source_2 = AssetSourceDates(first_contribution_date=date(2021, 1, 1))
    pension_asset_1 = Asset(
        id="pension-1",
        name="Pension 1",
        asset_type=AssetType.PENSION,
        currency=Currency.ILS,
        source_dates=pension_source_1,
    )
    pension_asset_2 = Asset(
        id="pension-2",
        name="Pension 2",
        asset_type=AssetType.PENSION,
        currency=Currency.ILS,
        source_dates=pension_source_2,
    )
    bank_asset = Asset(
        id="bank-1",
        name="Bank 1",
        asset_type=AssetType.BANK_ACCOUNT,
        currency=Currency.ILS,
        source_dates=AssetSourceDates(account_opened_date=date(2020, 1, 1)),
    )
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2022, 12, 31))
    valuation_date = date(2022, 12, 31)
    balance_by_asset_id = {
        "pension-1": 1000.0,
        "pension-2": 2000.0,
        "bank-1": 5000.0,
    }

    service = CaseCalculationService()
    results = service.calculate_case(
        assets=[pension_asset_1, bank_asset, pension_asset_2],
        marriage_period=marriage_period,
        valuation_date=valuation_date,
        balance_by_asset_id=balance_by_asset_id,
    )

    # all assets counted in metrics
    assert results.metrics.total_assets == 3
    assert results.metrics.by_asset_type[AssetType.PENSION] == 2
    assert results.metrics.by_asset_type[AssetType.BANK_ACCOUNT] == 1
    assert results.metrics.by_track_type[CalculationTrackType.ACCUMULATING_SAVINGS] == 2
    assert results.metrics.by_track_type[CalculationTrackType.INVESTMENT_OR_CASH] == 1

    # only calculable assets (pensions) contribute to gross maps and totals
    total_gross = sum(r.gross_shared_value for r in results.results)
    assert results.metrics.gross_shared_value_by_asset_type[AssetType.PENSION] == pytest.approx(
        total_gross
    )
    assert AssetType.BANK_ACCOUNT not in results.metrics.gross_shared_value_by_asset_type
    assert results.metrics.gross_shared_value_by_track_type[
        CalculationTrackType.ACCUMULATING_SAVINGS
    ] == pytest.approx(total_gross)
    assert (
        CalculationTrackType.INVESTMENT_OR_CASH
        not in results.metrics.gross_shared_value_by_track_type
    )
    assert results.total_gross_shared_value == pytest.approx(total_gross)
