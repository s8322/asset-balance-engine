from datetime import date

import pytest

from application.case_full_calculation_service import CaseFullCalculationService
from application.liability_input import LiabilityInput
from domain.asset import Asset
from domain.asset_source_dates import AssetSourceDates
from domain.enums import AssetType, BorrowerScope, Currency, PurposeScope
from domain.liability_metadata import LiabilityMetadata
from domain.shared_period import SharedPeriod


def _build_pension_asset() -> Asset:
    source_dates = AssetSourceDates(first_contribution_date=date(2020, 1, 1))
    return Asset(
        id="asset-1",
        name="Pension",
        asset_type=AssetType.PENSION,
        currency=Currency.ILS,
        source_dates=source_dates,
    )


def _default_marriage_period_and_valuation() -> tuple[SharedPeriod, date]:
    marriage_period = SharedPeriod(start=date(2019, 1, 1), end=date(2020, 12, 31))
    valuation_date = date(2020, 12, 31)
    return marriage_period, valuation_date


def test_full_case_with_shared_liability() -> None:
    asset = _build_pension_asset()
    marriage_period, valuation_date = _default_marriage_period_and_valuation()
    balance_by_asset_id = {asset.id: 1000.0}

    total_liability_amount = 500.0
    metadata = LiabilityMetadata(
        borrower_scope=BorrowerScope.JOINT,
        purpose_scope=PurposeScope.FAMILY_ASSET,
    )
    liabilities = [
        LiabilityInput(
            total_amount=total_liability_amount,
            asset_type=AssetType.LIABILITY,
            metadata=metadata,
        )
    ]

    service = CaseFullCalculationService()
    result = service.calculate_full_case(
        assets=[asset],
        liabilities=liabilities,
        marriage_period=marriage_period,
        valuation_date=valuation_date,
        balance_by_asset_id=balance_by_asset_id,
    )

    assert len(result.asset_calculation.results) == 1
    assert len(result.liability_results) == 1
    assert result.liability_results[0].is_candidate_for_sharing is True
    assert result.liability_results[0].shared_amount == total_liability_amount
    assert result.total_assets_shared_value == pytest.approx(
        sum(r.gross_shared_value for r in result.asset_calculation.results)
    )
    assert result.asset_calculation.total_gross_shared_value == pytest.approx(
        result.total_assets_shared_value
    )
    assert result.total_liabilities_shared_value == total_liability_amount
    assert result.net_shared_value == pytest.approx(
        result.total_assets_shared_value - result.total_liabilities_shared_value
    )


def test_full_case_with_non_shared_liability() -> None:
    asset = _build_pension_asset()
    marriage_period, valuation_date = _default_marriage_period_and_valuation()
    balance_by_asset_id = {asset.id: 1000.0}

    total_liability_amount = 500.0
    metadata = LiabilityMetadata(
        borrower_scope=BorrowerScope.PARTY_A,
        purpose_scope=PurposeScope.PERSONAL_A,
    )
    liabilities = [
        LiabilityInput(
            total_amount=total_liability_amount,
            asset_type=AssetType.LIABILITY,
            metadata=metadata,
        )
    ]

    service = CaseFullCalculationService()
    result = service.calculate_full_case(
        assets=[asset],
        liabilities=liabilities,
        marriage_period=marriage_period,
        valuation_date=valuation_date,
        balance_by_asset_id=balance_by_asset_id,
    )

    assert len(result.liability_results) == 1
    assert result.liability_results[0].is_candidate_for_sharing is False
    assert result.liability_results[0].shared_amount == 0.0
    assert result.total_liabilities_shared_value == 0.0
    assert result.asset_calculation.total_gross_shared_value == pytest.approx(
        result.total_assets_shared_value
    )
    assert result.net_shared_value == pytest.approx(
        result.total_assets_shared_value
    )


def test_full_case_with_no_liabilities() -> None:
    asset = _build_pension_asset()
    marriage_period, valuation_date = _default_marriage_period_and_valuation()
    balance_by_asset_id = {asset.id: 1000.0}

    service = CaseFullCalculationService()
    result = service.calculate_full_case(
        assets=[asset],
        liabilities=[],
        marriage_period=marriage_period,
        valuation_date=valuation_date,
        balance_by_asset_id=balance_by_asset_id,
    )

    assert result.liability_results == []
    assert result.total_liabilities_shared_value == 0.0
    assert result.total_assets_shared_value == pytest.approx(
        sum(r.gross_shared_value for r in result.asset_calculation.results)
    )
    assert result.asset_calculation.total_gross_shared_value == pytest.approx(
        result.total_assets_shared_value
    )
    assert result.net_shared_value == pytest.approx(
        result.total_assets_shared_value
    )

